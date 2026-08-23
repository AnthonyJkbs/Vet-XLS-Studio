# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Vet XLS Studio (Linux build).
# Usage:  pyinstaller packaging/linux/VetXLSStudio.spec

import os

ROOT = os.path.abspath(os.path.join(SPECPATH, "..", ".."))

a = Analysis(
    [os.path.join(ROOT, "main.py")],
    pathex=[ROOT],
    binaries=[],
    datas=[(os.path.join(ROOT, "assets"), "assets")],
    hiddenimports=["PIL._tkinter_finder"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        "numpy", "scipy", "pandas", "matplotlib", "flexiblas",
        "tkinter.test", "test",
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="VetXLSStudio",
    icon=os.path.join(ROOT, "assets", "logo.ico"),
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
