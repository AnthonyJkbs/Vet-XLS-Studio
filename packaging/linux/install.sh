#!/usr/bin/env bash
# Vet XLS Studio - Linux installer (user-level, no root required)
set -e

APP="VetXLSStudio"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN="$SRC_DIR/$APP"          # built binary expected next to this script
[ -f "$BIN" ] || BIN="$(dirname "$SRC_DIR")/../dist/$APP"
ICON="$SRC_DIR/vetxlsstudio.png"

[ -f "$BIN" ] || { echo "ERROR: $BIN not found. Build it first:"; \
                  echo "  pyinstaller packaging/linux/VetXLSStudio.spec"; exit 1; }

BIN_DIR="${HOME}/.local/bin"
ICO_DIR="${HOME}/.local/share/icons/hicolor/512x512/apps"
DESK_DIR="${HOME}/.local/share/applications"
mkdir -p "$BIN_DIR" "$ICO_DIR" "$DESK_DIR"

install -m 755 "$BIN" "$BIN_DIR/$APP"

if [ -f "$ICON" ]; then
    install -m 644 "$ICON" "$ICO_DIR/vetxlsstudio.png"
    gtk-update-icon-cache -q "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi

sed "s|Exec=.*|Exec=$BIN_DIR/$APP|" \
    "$SRC_DIR/vet-xls-studio.desktop" > "$DESK_DIR/vet-xls-studio.desktop"

update-desktop-database "$DESK_DIR" 2>/dev/null || true

echo
echo "Installed:"
echo "  binary : $BIN_DIR/$APP"
echo "  icon   : $ICO_DIR/vetxlsstudio.png"
echo "  menu   : $DESK_DIR/vet-xls-studio.desktop"
echo
echo "Launch it from your applications menu as 'Vet XLS Studio',"
echo "or run: $BIN_DIR/$APP"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/VetXLSStudio/data"
mkdir -p "$DATA_DIR"
echo "  data   : $DATA_DIR  (clinic records live here)"
echo
echo "Uninstall anytime with: $(dirname "$0")/uninstall.sh"
