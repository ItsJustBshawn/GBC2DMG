# GBC2DMG

GBC2DMG converts supported Game Boy Color ROMs to run on the original Game Boy (DMG).

[Releases](https://github.com/ItsJustBshawn/GBC2DMG/releases/tag/v0.4-beta.1) · [Run from source](docs/BUILDING.md)

## Supported games

| Game | Region / language | Versions |
| --- | --- | --- |
| Pokémon Crystal | USA / Europe, English | 1.0 and 1.1 (Rev 1 / Rev A) |

Crystal is the only supported game right now. Rev 1 and Rev A are names for the same version. The app checks your ROM and tells you which version you have. Other games, regions and modified ROMs aren't supported.

## How to use it

The Windows download is currently unavailable. You can find the source and setup instructions in [BUILDING.md](docs/BUILDING.md).

1. Open the app and choose your ROM.
2. Click **Convert to DMG** and save the new `.gb` file.
3. Load it on your flash cartridge or in a DMG-mode emulator.

Your original ROM is left unchanged. ROMs are not included.

## Things to know

This is a beta. Back up your saves before trying it.

Crystal's clock runs while you're playing and pauses when the Game Boy is off. The converted game needs MBC5 support with 128 KB save RAM.

## Found a bug?

[Open an issue](https://github.com/ItsJustBshawn/GBC2DMG/issues) with what happened and which cartridge or emulator you're using. You can copy your ROM's version report from the app. Please don't upload ROMs.

## Source and credits

[Run or build from source](docs/BUILDING.md) · [License](LICENSE)

Built using [pret/pokecrystal](https://github.com/pret/pokecrystal) and [RGBDS](https://github.com/gbdev/rgbds), with emulator testing in [SameBoy](https://github.com/LIJI32/SameBoy).

GBC2DMG is an unofficial project and is not affiliated with Nintendo, Game Freak or The Pokémon Company.
