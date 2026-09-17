"""Check recipe files without needing a game ROM."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
entries = json.loads((root/'catalog.json').read_text())['games']
assert len({g['source_sha256'] for g in entries}) == len(entries), 'Duplicate source hash'
for entry in entries:
    recipe = (root/entry['recipe']).resolve()
    assert recipe.is_relative_to(root.resolve())
    assert hashlib.sha256(recipe.read_bytes()).hexdigest() == entry['recipe_sha256']
    for field in ['source_sha256', 'output_sha256', 'recipe_sha256']:
        assert len(entry[field]) == 64 and all(c in '0123456789abcdef' for c in entry[field])
    assert entry['support_level'] == 'beta'
print(f'{len(entries)} catalog entries and recipe checksums OK.')
