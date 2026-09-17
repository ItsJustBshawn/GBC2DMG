# Beta 1 testing

Both English Crystal inputs are approved for this beta. Approval means the exact input and output hashes passed the checks below, not that every part of the game has been tested.

| Check | 1.0 | 1.1 |
| --- | --- | --- |
| Map fixture loads | 97 passed | 97 passed |
| Scrolling trials | 58; movement in 56 | 58; movement in 56 |
| Tile cache overflow / resident pixel mismatch | 0 / 0 | 0 / 0 |
| Unown wall messages compared with source pixels | 4 passed | 4 passed |
| Route 29 / New Bark boundary banner | Passed | Passed |
| Suicune title animation | 4 poses | 4 poses |
| Battle completion and experience gain | Passed | Passed |
| Save, cold boot and MGB reload | Passed | Passed |
| Clock over 602.737 emulated seconds | +602 seconds | +602 seconds |

These are automated fixture and runtime tests using SameBoy, not a complete playthrough. Representative map images, Elm's desk and the Unown messages were also inspected. Map fixtures can start at positions that normal gameplay would not reach.

The port includes the second-VRAM-bank map handling, corrected desk tiles, Unown overlays, route-banner sprite clipping, title animation, intro transition handling and shorter Pokémon animation waits. Audio was left unchanged in this revision.

The 1.1 port is built as 1.1 and keeps its Battle Tower changes and Pokédex status allocation. It is not a conversion back to 1.0.

## Still needs testing

- This exact build on a physical DMG and EZ-Flash Jr.
- A complete playthrough, including event-dependent sprite combinations.
- The complete train ride. Its attribute-plane guard is source-reviewed, but the ride is not runtime-certified.
- Trading, link functions and every battle effect.
- Broad emulator and flash cartridge compatibility.

The clock intentionally advances only during play. Powered-off time is not counted.

Machine-readable results are in [validation.json](validation.json). Output hashes are also locked in the app's catalog. App tests cover recipe parsing, integrity checks, overwrite protection and version detection.
