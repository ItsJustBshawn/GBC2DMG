# How the Crystal port works

There are two parts to GBC2DMG: the game-specific DMG port and the Python application that applies it to a matching ROM. The application doesn't automatically translate arbitrary Game Boy Color code.

## Working within DMG hardware

The original Game Boy and the Color share a CPU instruction set, but they don't have the same resources.

| Resource | Original Game Boy | Game Boy Color |
| --- | --- | --- |
| Video RAM | 8 KiB, one bank | 16 KiB, two banks |
| Work RAM | 8 KiB | 32 KiB, banked |
| CPU speed | Normal speed | Normal or double speed |
| Display | Four shades | Color palettes and per-tile attributes |
| Graphics transfer | CPU copies and OAM DMA | Also supports general-purpose and HBlank VRAM DMA |

See [Pan Docs: CGB registers](https://gbdev.io/pandocs/CGB_Registers.html) and [tile data](https://gbdev.io/pandocs/Tile_Data.html) for the hardware details.

Crystal depends on the extra banks and Color-specific transfer routines. A DMG cannot supply those simply because a cartridge header says the game is compatible.

## Making room for working data

The port relocates six of Crystal's banked work-memory sections into cartridge SRAM. The routines selecting those sections are changed to select the corresponding cartridge RAM bank. Save access and interrupt handling must preserve the correct bank as well.

The resulting ROM uses an MBC5 cartridge layout with 128 KiB of RAM. Part of that RAM holds saves, and part serves as working storage. This is why the cartridge or emulator's RAM support matters.

## Fitting the graphics

Color backgrounds can select tiles from either VRAM bank. The DMG only has one. The port remaps those references and arranges the required tile graphics in the available space.

Smaller areas use fixed tile layouts. Seven larger tilesets use a 96-slot background cache. The cache reuses identical tile graphics and keeps the tiles required by both sides of a scrolling transition. Fonts, roofs and animated tiles have reserved handling so loading a new view doesn't overwrite graphics still on screen.

This preserves the underlying map and collision data. The job is to change where graphics live and how they are loaded, rather than replace the game's maps.

## Transfers, attributes and timing

The DMG doesn't have the Color's VRAM DMA hardware. The port replaces those transfers with software copies that respect when video memory can be written. Color attributes also need separate handling: on a DMG, writing as though the second VRAM bank exists can overwrite the tilemap in the first bank.

Animations and screen transitions have to fit the smaller graphics budget and normal CPU speed. The title screen retains four Suicune running poses. Some transitions blank the display while graphics are replaced.

The cartridge layout uses a software play clock. It is saved with the game and advances while playing; it doesn't count time while the console is switched off.

## What the Python app does

1. Calculate the input ROM's SHA-256 and find an approved entry in the catalog.
2. Check the corresponding recipe's SHA-256.
3. Apply the recipe's source-copy and literal-data operations.
4. Check the output SHA-256 before writing a new file.

The recipe contains the changes needed for that exact game revision. It avoids distributing a complete ROM, and the app refuses unknown inputs rather than guessing from the filename or header.

English Crystal 1.0 and 1.1 have separate recipes and output hashes. Rev A and Rev 1 identify the same 1.1 input.

## Adding another game

The Python side can already handle more catalog entries and recipes. Supporting a new game still requires examining its engine:

- Which Color hardware features does it use?
- How much working data must be kept at once, and can cartridge RAM hold it?
- Which graphics must coexist on screen, and can they fit or be streamed safely?
- Does game logic depend on double-speed timing?
- What cartridge, save and clock behavior must be preserved?

The Crystal cache is tailored to Crystal's map renderer. It is a useful approach, not a drop-in replacement for every game's renderer. A different game might need another cache layout, a different palette conversion, or changes to individual effects.

Once a port is built and tested, its exact input and output hashes and recipe can be added to the catalog. New support is a maintainer decision. Sharing a platform or engine doesn't by itself establish compatibility.

The repository contains the Python converter and ready-to-apply recipes. It is not a complete source-build kit for the Crystal port. The original disassembly is maintained by [pret/pokecrystal](https://github.com/pret/pokecrystal).
