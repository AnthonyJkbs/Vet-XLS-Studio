#!/usr/bin/env bash
# Vet XLS Studio - Linux uninstaller (reverses install.sh)
set -e

rm -f  "$HOME/.local/bin/VetXLSStudio"
rm -f  "$HOME/.local/share/icons/hicolor/512x512/apps/vetxlsstudio.png"
rm -f  "$HOME/.local/share/applications/vet-xls-studio.desktop"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
gtk-update-icon-cache -q "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

echo "Removed binary, icon and menu entry."
echo
echo "Your clinic data was kept at:"
if [ -n "$XDG_DATA_HOME" ]; then D="$XDG_DATA_HOME"; else D="$HOME/.local/share"; fi
echo "  $D/VetXLSStudio/data"
echo "Delete that folder too if you no longer need the records."
