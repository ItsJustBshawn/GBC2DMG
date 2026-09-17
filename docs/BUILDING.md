# Running and developing GBC2DMG

Use Python 3.11 or newer with Tk. The app uses the Python standard library; no pip installation is required.

```sh
python app.py
```

On Windows, `launch.cmd` looks for the Python launcher, then `python`. `GBC2DMG.pyw` opens without a console if your Python installation has registered that file type. You can also pass a ROM path:

```sh
python app.py "your-game.gbc"
python identify_rom.py "your-game.gbc" --json
```

On macOS and Linux, use `python3` if that is your Python command. If importing `tkinter` fails on Linux, install your distribution's Tk package for Python. Check the installation with `python3 -m tkinter`.

## Tests

```sh
python -m unittest discover -s tests -v
python tools/check_catalog.py
```

GUI tests need a working Tk display. On a headless Linux machine, run them with Xvfb; without a display they are skipped.

## Files

- `app.py`: Tk desktop interface.
- `converter.py`: ROM identification, recipe application and integrity checks.
- `identify_rom.py`: command-line version report.
- `catalog.json`: supported inputs, output hashes and recipe paths.
- `recipes/`: conversion data for approved versions.
- `build_recipe.py`: maintainer tool for packaging an already-built port.

The main download is a Python source package. Keep the app, catalog and recipes together. To create that ZIP:

```sh
python tools/package.py
```

The package script uses an explicit file list and includes only the recipes referenced by the catalog. It never includes a ROM, save, Python runtime or frozen executable.
