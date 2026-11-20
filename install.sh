#!/usr/bin/env bash
set -e

echo "================================================="
echo " Installing Naukri Profile Activity Automator   "
echo "================================================="

# 1. Check requirements
if [ ! -d "/Applications/Google Chrome.app" ]; then
    echo "Error: Google Chrome was not found at /Applications/Google Chrome.app"
    exit 1
fi

PYTHON_BIN="$(which python3 || echo "/opt/homebrew/bin/python3")"
if [ ! -x "$PYTHON_BIN" ]; then
    echo "Error: Python 3 not found on system."
    exit 1
fi

echo "Using Python: $PYTHON_BIN"

# 2. Setup ~/.local/bin
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/Library/Logs/naukri-automation"
mkdir -p "$HOME/Library/LaunchAgents"

cp bin/naukri_browse.py "$HOME/.local/bin/naukri_browse.py"
cp bin/naukri-automation "$HOME/.local/bin/naukri-automation"
chmod +x "$HOME/.local/bin/naukri_browse.py" "$HOME/.local/bin/naukri-automation"

# 3. Setup LaunchAgent plist with dynamic home path
PLIST_TARGET="$HOME/Library/LaunchAgents/com.anuragh.naukri-automation.plist"
sed -e "s|/Users/anuraghragidimilli|$HOME|g" \
    -e "s|/opt/homebrew/bin/python3|$PYTHON_BIN|g" \
    launchd/com.anuragh.naukri-automation.plist > "$PLIST_TARGET"

# 4. Load into launchctl
launchctl unload "$PLIST_TARGET" 2>/dev/null || true
launchctl load "$PLIST_TARGET"

echo ""
echo "Installation complete!"
echo "Service is now active in macOS launchd."
echo "Use 'naukri-automation status' to verify."
echo "================================================="
