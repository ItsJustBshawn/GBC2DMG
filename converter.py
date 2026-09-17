"""Local, hash-locked ROM converter. No network access or ROM distribution."""
from pathlib import Path
import hashlib
import json
import struct
import zlib

ROOT = Path(__file__).resolve().parent
LIMIT = 16 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def catalog():
    return json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))['games']


def enabled(entry):
    return entry.get('approved') is True or entry.get('testing_enabled') is True


def identify(path):
    """Identify known source/output bytes; a filename or header is not proof."""
    path = Path(path)
    if not path.is_file() or not 0x150 <= path.stat().st_size <= LIMIT:
        raise ValueError('Choose a Game Boy ROM between 336 bytes and 16 MB.')
    data = path.read_bytes()
    sha = digest(data)
    games = catalog()
    entry = next((g for g in games if g['source_sha256'] == sha), None)
    converted = next((g for g in games if g['output_sha256'] == sha), None)
    result = dict(file=path.name, size_bytes=len(data), sha256=sha,
                  header_title=data[0x134:(0x13f if data[0x143] & 0x80 else 0x144)].split(b'\0')[0].decode('ascii', errors='replace'),
                  header_revision=data[0x14c],
                  header_checksum_valid=((-sum(data[0x134:0x14d])-25)&255)==data[0x14d],
                  global_checksum_valid=((sum(data[:0x14e])+sum(data[0x150:]))&65535)==int.from_bytes(data[0x14e:0x150], 'big'),
                  kind='source' if entry else ('converted' if converted else 'unknown'),
                  recognized=bool(entry or converted), can_convert=bool(entry and enabled(entry)))
    known = entry or converted
    if known:
        result.update(game=known['name'], version=known['version'], aliases=known.get('aliases', []),
                      release=known['release'], catalog_id=known['id'])
    return result


def apply_delta(source, patch):
    dec = zlib.decompressobj()
    try:
        stream = dec.decompress(patch, LIMIT + 1)
    except zlib.error as exc:
        raise ValueError("Invalid compressed recipe.") from exc
    if len(stream) > LIMIT or not dec.eof or dec.unused_data:
        raise ValueError('Invalid or oversized recipe.')
    if stream[:4] != b'D2M1':
        raise ValueError('Unrecognized recipe format.')
    out = bytearray()
    pos = 4
    while pos < len(stream):
        op = stream[pos:pos + 1]
        pos += 1
        if pos + 4 > len(stream):
            raise ValueError('Truncated recipe.')
        size = struct.unpack_from('<I', stream, pos)[0]
        pos += 4
        if not size or len(out) + size > LIMIT:
            raise ValueError('Invalid output size.')
        if op == b'C':
            if pos + 4 > len(stream):
                raise ValueError('Truncated source reference.')
            offset = struct.unpack_from('<I', stream, pos)[0]
            pos += 4
            if offset + size > len(source):
                raise ValueError('Source reference outside ROM.')
            out.extend(source[offset:offset + size])
        elif op == b'L':
            if pos + size > len(stream):
                raise ValueError('Truncated literal data.')
            out.extend(stream[pos:pos + size])
            pos += size
        else:
            raise ValueError('Unknown recipe operation.')
    return bytes(out)


def convert(source_path, destination, entry):
    source_path, destination = Path(source_path), Path(destination)
    if not enabled(entry):
        raise ValueError('This game is not approved or enabled for beta testing.')
    if source_path.stat().st_size > LIMIT:
        raise ValueError('ROM exceeds supported size.')
    source = source_path.read_bytes()
    if digest(source) != entry['source_sha256']:
        raise ValueError('This exact ROM version is not supported. The source was not changed.')
    recipe = (ROOT / entry['recipe']).resolve()
    if not recipe.is_relative_to(ROOT.resolve()):
        raise ValueError('Invalid recipe path.')
    patch = recipe.read_bytes()
    if digest(patch) != entry['recipe_sha256']:
        raise ValueError('Recipe integrity check failed.')
    result = apply_delta(source, patch)
    if digest(result) != entry['output_sha256']:
        raise ValueError('Converted ROM verification failed.')
    # Exclusive creation prevents overwriting a ROM, save, or an earlier result.
    with destination.open('xb') as f:
        try:
            f.write(result)
        except BaseException:
            f.close()
            destination.unlink(missing_ok=True)
            raise
    return digest(result)
