# -*- mode: python ; coding: utf-8 -*-
import json
from pathlib import Path
entries = json.loads(Path('catalog.json').read_text(encoding='utf-8'))['games']


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('catalog.json', '.')] + [(entry['recipe'], 'recipes') for entry in entries],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GBC2DMG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GBC2DMG',
)
