"""Package the Python app from an explicit list of distributable files."""
from pathlib import Path
import hashlib
import json
import zipfile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import APP_VERSION


def main():
    entries = json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['games']
    files = ['app.py', 'converter.py', 'identify_rom.py', 'GBC2DMG.pyw', 'launch.cmd',
             'catalog.json', 'README.md', 'LICENSE', 'CHANGELOG.md', 'build_recipe.py',
             'docs/BUILDING.md', 'docs/HOW-IT-WORKS.md', 'tools/package.py', 'tools/check_catalog.py']
    files += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'tests').glob('test_*.py'))]
    for entry in entries:
        path = (ROOT/entry['recipe']).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError('Recipe outside project directory')
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry['recipe_sha256']:
            raise ValueError('Recipe hash mismatch')
        files.append(entry['recipe'])
    release = ROOT/'release'
    release.mkdir(exist_ok=True)
    target = release/f'GBC2DMG-v{APP_VERSION}-Python.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(set(files)):
            path = ROOT/name
            if path.suffix.lower() in {'.gb', '.gbc', '.sav', '.exe', '.dll', '.pyc'}:
                raise ValueError('Unexpected distributable file')
            archive.write(path, Path('GBC2DMG')/name)
    sha = hashlib.sha256(target.read_bytes()).hexdigest()
    (release/f'GBC2DMG-v{APP_VERSION}-SHA256SUMS.txt').write_text(sha+'  '+target.name+'\n', encoding='ascii')
    print(target)
    print('SHA-256:', sha)


if __name__ == '__main__':
    main()
