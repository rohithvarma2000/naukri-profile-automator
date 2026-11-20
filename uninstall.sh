#!/usr/bin/env bash
set -e

echo "Uninstalling Naukri Profile Activity Automator..."

PLIST_TARGET="$HOME/Library/LaunchAgents/com.anuragh.naukri-automation.plist"

if [ -f "$PLIST_TARGET" ]; then
    launchctl unload "$PLIST_TARGET" 2>/dev/null || true
    rm -f "$PLIST_TARGET"
    echo "Removed LaunchAgent plist."
fi

rm -f "$HOME/.local/bin/naukri_browse.py"
rm -f "$HOME/.local/bin/naukri-automation"

echo "Removed CLI binaries."
echo "Note: Logs preserved at ~/Library/Logs/naukri-automation/ (delete manually if desired)."
echo "Uninstallation complete."
