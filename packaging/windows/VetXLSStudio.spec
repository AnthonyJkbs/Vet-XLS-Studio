# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec - WINDOWS ONEFILE build for Vet XLS Studio.
#
# Produces a SINGLE portable executable:  dist\VetXLSStudio.exe
# That file is then wrapped into the setup installer by Inno Setup
# (see VetXLSStudio.iss / build_windows.bat).
#
# Usage (on Windows):
#   pip install pyinstaller pillow openpyxl
#   pyinstaller packaging\windows\VetXLSStudio.spec

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
        "numpy", "scipy", "pandas", "matplotlib",
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
    version=os.path.join(ROOT, "packaging", "windows", "version_info.py"),
    upx=True,
    console=False,                 # GUI app - no console window
    disable_windowed_traceback=False,
)
