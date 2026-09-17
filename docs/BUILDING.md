# Building GBC2DMG

Use Python 3.11 or newer with Tk. The standard Windows Python installer includes Tk.

Run the app:

```sh
python app.py
```

Identify a ROM from the command line:

```sh
python identify_rom.py "your-game.gbc"
```

Build the Windows app on Windows:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-build.txt
.venv\Scripts\python -m PyInstaller --clean --noconfirm GBC2DMG.spec
```

The output is in `dist/GBC2DMG`. Keep that folder together.

Run the application tests:

```sh
python -m unittest discover -s tests -v
python tools/check_catalog.py
```

Supported ROMs and their conversion recipes are listed in `catalog.json`. `build_recipe.py` packages an existing port into a recipe; it doesn't port games automatically.
