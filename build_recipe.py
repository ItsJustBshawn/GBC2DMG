"""Maintainer-only recipe builder. Takes local dumps; never bundles the dumps."""
import argparse
from collections import defaultdict
from pathlib import Path
import json
import struct
import zlib
from converter import digest, apply_delta

KNOWN_SOURCES = {
    'd6702e353dcbe2d2c69183046c878ef13a0dae4006e8cdff521cca83dd1582fe':
        ('crystal-en-v10', '1.0', ['Original', 'Rev 0']),
    'fdcc3c8c43813cf8731fc037d2a6d191bac75439c34b24ba1c27526e6acdc8a2':
        ('crystal-en-v11', '1.1', ['Rev 1', 'Rev A']),
}


def make_delta(source, target):
    # Source-copy operations retain relocated original bytes without embedding them.
    index = defaultdict(list)
    for p in range(0, len(source) - 15, 4):
        key = source[p:p + 16]
        if len(index[key]) < 12:
            index[key].append(p)
    stream = bytearray(b'D2M1')
    literal = bytearray()
    def flush():
        if literal:
            stream.extend(b'L' + struct.pack('<I', len(literal)) + literal)
            literal.clear()
    p = 0
    while p < len(target):
        best, offset = 0, 0
        for q in index.get(target[p:p + 16], ()):
            n = 16
            bound = min(len(source) - q, len(target) - p)
            while n + 128 <= bound and source[q + n:q + n + 128] == target[p + n:p + n + 128]:
                n += 128
            while n < bound and source[q + n] == target[p + n]:
                n += 1
            if n > best:
                best, offset = n, q
        if best >= 16:
            flush()
            stream.extend(b'C' + struct.pack('<II', best, offset))
            p += best
        else:
            literal.append(target[p])
            p += 1
    flush()
    result = zlib.compress(stream, 9)
    assert apply_delta(source, result) == target
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('--testing', action='store_true', help='Enable this exact recipe for local beta testing; does not approve public support.')
    parser.add_argument('--approved', action='store_true', help='Record maintainer approval for this exact beta recipe.')
    parser.add_argument('--release', default='0.4-beta.1')
    args = parser.parse_args()
    source, target = args.source.read_bytes(), args.target.read_bytes()
    if digest(source) not in KNOWN_SOURCES:
        raise SystemExit('Unknown source. Add support only after building and testing a port for that exact ROM.')
    game_id, version, aliases = KNOWN_SOURCES[digest(source)]
    if target[0x143] != 0 or target[0x147] != 0x1b or target[0x149] != 4:
        raise SystemExit('Expected a DMG/MBC5/128 KB RAM output.')
    if target[0x14c] != source[0x14c]:
        raise SystemExit('The target must preserve the source revision.')
    patch = make_delta(source, target)
    root = Path(__file__).resolve().parent
    recipe = f'recipes/{game_id}.d2m'
    (root / recipe).write_bytes(patch)
    entry = dict(id=game_id, name=f'Pokémon Crystal — English v{version}', version=version, aliases=aliases,
                 approved=args.approved, support_level='beta',
                 testing_enabled=args.testing, release=args.release, source_sha256=digest(source),
                 output_sha256=digest(target), recipe=recipe, recipe_sha256=digest(patch),
                 note='Beta. Clock advances during play only.')
    path = root / 'catalog.json'
    games = json.loads(path.read_text(encoding='utf-8'))['games'] if path.exists() else []
    games = [g for g in games if g['id'] != game_id] + [entry]
    games.sort(key=lambda g: g['id'])
    path.write_text(json.dumps({'schema': 1, 'games': games}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(entry, indent=2))
    print('Recipe bytes:', len(patch))

if __name__ == '__main__':
    main()
