"""Frozen-aware application paths (works both as script and PyInstaller exe).

Layout when running from source: everything stays inside the project dir.
When packaged:
  - resources (assets/) are unpacked by PyInstaller into sys._MEIPASS;
  - user data goes next to the executable on Windows (portable-friendly)
    and into ~/.local/share/VetXLSStudio on Linux (menu installs live
    in ~/.local/bin, which is no place for clinic records).
"""
from __future__ import annotations

import os
import sys

if getattr(sys, "frozen", False):          # running as packaged exe
    if sys.platform == "win32":
        APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
    else:
        xdg = os.environ.get("XDG_DATA_HOME") or os.path.join(
            os.path.expanduser("~"), ".local", "share")
        APP_DIR = os.path.join(xdg, "VetXLSStudio")
    _BUNDLED = getattr(sys, "_MEIPASS", os.path.dirname(APP_DIR))
else:                                      # running from source tree
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    _BUNDLED = APP_DIR

DATA_DIR = os.path.join(APP_DIR, "data")


def resource(rel: str) -> str:
    """Path to a bundled read-only resource (assets, fonts...)."""
    return os.path.join(_BUNDLED, rel)


def writable(rel: str) -> str:
    """Path under the app data dir (created on demand)."""
    p = os.path.join(DATA_DIR, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


os.makedirs(DATA_DIR, exist_ok=True)
