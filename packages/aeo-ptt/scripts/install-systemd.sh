#!/usr/bin/env bash
# Generate and install systemd service for AEO Push-to-Talk
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATE="$SCRIPT_DIR/aeo-ptt.service.template"
OUTPUT="/tmp/aeo-ptt.service"

# Parse args
AUTO_YES=0
if [[ "${1:-}" == "--yes" ]] || [[ "${1:-}" == "-y" ]]; then
    AUTO_YES=1
fi

# Detect values
USER="$(whoami)"
HOME="$HOME"
UV_PATH="$(command -v uv || true)"

# Validate
if [[ ! -f "$TEMPLATE" ]]; then
    echo "ERROR: Template not found: $TEMPLATE"
    exit 1
fi

if [[ -z "$UV_PATH" ]]; then
    echo "ERROR: uv not found."
    echo ""
    echo "Install uv with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  source ~/.bashrc"
    exit 1
fi

echo "=== AEO Push-to-Talk Systemd Installer ==="
echo ""
echo "Detected configuration:"
echo "  User:        $USER"
echo "  Home:        $HOME"
echo "  Project:     $PROJECT_DIR"
echo "  uv path:     $UV_PATH"
echo ""

# Generate from template
sed -e "s|{{USER}}|$USER|g" \
    -e "s|{{HOME}}|$HOME|g" \
    -e "s|{{PROJECT_DIR}}|$PROJECT_DIR|g" \
    -e "s|{{UV_PATH}}|$UV_PATH|g" \
    "$TEMPLATE" > "$OUTPUT"

echo "Generated service file:"
echo "----------------------------------------"
cat "$OUTPUT"
echo "----------------------------------------"
echo ""

if [[ "$AUTO_YES" == "1" ]]; then
    REPLY="y"
else
    read -p "Install to /etc/systemd/system/aeo-ptt.service? [y/N] " -n 1 -r
    echo
fi
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo cp "$OUTPUT" /etc/systemd/system/aeo-ptt.service
    sudo systemctl daemon-reload
    sudo systemctl enable aeo-ptt
    rm -f "$OUTPUT"  # Clean up temp file
    echo ""
    echo "Installed and enabled. Commands:"
    echo "  sudo systemctl start aeo-ptt    # Start now"
    echo "  sudo systemctl status aeo-ptt   # Check status"
    echo "  journalctl -u aeo-ptt -f        # View logs"
else
    echo ""
    echo "Skipped. Generated file saved to: $OUTPUT"
fi

