# GBC2DMG

GBC2DMG converts supported Game Boy Color ROMs to run on the original Game Boy (DMG).

[Releases](https://github.com/ItsJustBshawn/GBC2DMG/releases/tag/v0.4-beta.1) · [Run from source](docs/BUILDING.md)

The Windows download is temporarily unavailable while antivirus detections are reviewed. [VirusTotal report](https://www.virustotal.com/gui/file/36007e1132f18c6e5829699571edc35353a5a02ea7798b728f34ff91617110a4).

## Supported games

| Game | Region / language | Versions |
| --- | --- | --- |
| PokÃ©mon Crystal | USA / Europe, English | 1.0 and 1.1 (Rev 1 / Rev A) |

Crystal is the only supported game right now. Rev 1 and Rev A are names for the same version. The app checks your ROM and tells you which version you have. Other games, regions and modified ROMs aren't supported.

## How to use it

1. Download the Windows ZIP and extract it.
2. Open **GBC2DMG.exe**.
3. Choose your ROM, then click **Convert to DMG**.
4. Save the new `.gb` file and load it on your flash cartridge or in a DMG-mode emulator.

Keep the extracted folder together. You don't need Python or an internet connection to use the Windows app. Your original ROM is left unchanged. ROMs are not included.

## Things to know

This is a beta. Back up your saves before trying it.

Crystal's clock runs while you're playing and pauses when the Game Boy is off. The converted game needs MBC5 support with 128 KB save RAM.

## Found a bug?

[Open an issue](https://github.com/ItsJustBshawn/GBC2DMG/issues) with what happened and which cartridge or emulator you're using. You can copy your ROM's version report from the app. Please don't upload ROMs.

## Source and credits

[Run or build from source](docs/BUILDING.md) Â· [License](LICENSE)

Built using [pret/pokecrystal](https://github.com/pret/pokecrystal) and [RGBDS](https://github.com/gbdev/rgbds), with emulator testing in [SameBoy](https://github.com/LIJI32/SameBoy).

GBC2DMG is an unofficial project and is not affiliated with Nintendo, Game Freak or The PokÃ©mon Company.
