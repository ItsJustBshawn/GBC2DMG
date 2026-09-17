"""Read a ROM's version without changing it: python identify_rom.py file.gbc."""
import argparse
import json
from converter import identify


def main():
    parser = argparse.ArgumentParser(description='Identify a ROM by SHA-256 and inspect its Game Boy header.')
    parser.add_argument('rom')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        result = identify(args.rom)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(result['file'])
        print(result.get('game', 'Unknown ROM — no exact match in the support catalog'))
        print('Kind:', result['kind'])
        if result.get('aliases'):
            print('Also called:', ', '.join(result['aliases']))
        print('Header revision:', result['header_revision'])
        print('SHA-256:', result['sha256'])
        print('Conversion available:', 'yes' if result['can_convert'] else 'no')


if __name__ == '__main__':
    main()
