# GBC2DMG

A Python tool that converts supported Game Boy Color ROMs to run on the original Game Boy.

[Download](https://github.com/ItsJustBshawn/GBC2DMG/releases/tag/v0.4-beta.2)

## Compatibility

- **Pokémon Crystal, English (USA/Europe), v1.0**
- **Pokémon Crystal, English (USA/Europe), v1.1 — Rev 1 / Rev A**

Rev 1 and Rev A are the same revision. Other games, regions and modified ROMs are not supported. The app checks the file's contents, not its name.

## Run it

Requires **Python 3.11 or newer with Tk**. No pip packages are needed.

1. Download and extract the Python ZIP.
2. On Windows, double-click `launch.cmd`. On macOS or Linux, run `python3 app.py`.
3. Select your ROM and save the converted file.

Get Python from [python.org](https://www.python.org/downloads/). Keep the extracted folder together. Your original ROM is not changed. ROMs are not included.

## About the port

Crystal uses memory banks and graphics hardware that the DMG doesn't have. The port moves some working data into cartridge RAM, remaps graphics into one VRAM bank, and replaces Color-only transfers. The Python app applies that port to a matching ROM and verifies the result.

Supporting another game requires adapting its engine first. The converter and version checks are reusable; each new game still needs its own tested port before it can be added to the compatibility list.

[How it works](docs/HOW-IT-WORKS.md) · [Development](docs/BUILDING.md)

## Notes

This is a beta. Back up your saves. Crystal's clock advances during play and pauses when powered off. The converted game requires MBC5 with 128 KB save RAM.

[Report a bug](https://github.com/ItsJustBshawn/GBC2DMG/issues) with the version report and your hardware or emulator. Please don't upload ROMs.

## Credits

[pret/pokecrystal](https://github.com/pret/pokecrystal) · [RGBDS](https://github.com/gbdev/rgbds) · [Pan Docs](https://gbdev.io/pandocs/) · [SameBoy](https://github.com/LIJI32/SameBoy)

Application code is [MIT licensed](LICENSE). GBC2DMG is unofficial and is not affiliated with Nintendo, Game Freak or The Pokémon Company.
