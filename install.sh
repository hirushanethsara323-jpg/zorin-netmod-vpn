#!/bin/bash
# Zorin NetMod VPN - One-Command Installer for Zorin OS
# Repo: https://github.com/hirushanethsara323-jpg/zorin-netmod-vpn
# Usage: bash -c "$(curl -fsSL https://raw.githubusercontent.com/hirushanethsara323-jpg/zorin-netmod-vpn/main/install.sh)"

set -e
echo "🌀 Zorin NetMod VPN - NetMod-like VPN for Linux - Installer"
echo "=========================================================="

# Fix package errors first
echo ">>> [1/6] Package Error Repair..."
sudo dpkg --configure -a || true
sudo apt --fix-broken install -y || true
sudo apt install -f -y || true

echo ">>> [2/6] System Update..."
export DEBIAN_FRONTEND=noninteractive
sudo apt update
sudo apt upgrade -y || true

echo ">>> [3/6] Installing Dependencies for NetMod..."
sudo apt install -y python3 python3-pip python3-tk openssh-client stunnel4 curl wget git \
  python3-paramiko python3-websockets || {
    pip3 install paramiko websockets --break-system-packages || pip3 install paramiko websockets
  }

echo ">>> [4/6] Installing Python deps..."
pip3 install --break-system-packages paramiko websockets 2>/dev/null || pip3 install paramiko websockets

echo ">>> [5/6] Installing NetMod..."
INSTALL_DIR="$HOME/.local/share/zorin-netmod-vpn"
BIN_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR" "$BIN_DIR"

# If run from git clone, copy files, else download
if [ -f "netmod/cli.py" ]; then
  cp -r . "$INSTALL_DIR/"
else
  # Download from GitHub
  TMPDIR=$(mktemp -d)
  git clone https://github.com/hirushanethsara323-jpg/zorin-netmod-vpn.git "$TMPDIR/repo" || {
    echo "Git clone failed, trying wget..."
    mkdir -p "$TMPDIR"
    wget -q https://github.com/hirushanethsara323-jpg/zorin-netmod-vpn/archive/main.zip -O "$TMPDIR/main.zip"
    unzip -q "$TMPDIR/main.zip" -d "$TMPDIR"
  }
  cp -r $TMPDIR/repo/* "$INSTALL_DIR/" 2>/dev/null || cp -r $TMPDIR/zorin-netmod-vpn-main/* "$INSTALL_DIR/" 2>/dev/null || true
  rm -rf "$TMPDIR"
fi

# Create bin wrapper
cat > "$BIN_DIR/netmod" << 'BIN_EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/zorin-netmod-vpn"
cd "$INSTALL_DIR"
python3 -m netmod.cli "$@"
BIN_EOF
chmod +x "$BIN_DIR/netmod"

# Add to PATH if not already
if ! echo $PATH | grep -q "$BIN_DIR"; then
  echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> ~/.bashrc
  export PATH="$HOME/.local/bin:$PATH"
fi

# Create desktop entry for Zorin
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/netmod.desktop << DESKTOP
[Desktop Entry]
Name=Zorin NetMod VPN
Comment=NetMod-like VPN for Linux - SSH/SSL/WebSocket tunneling
Exec=$BIN_DIR/netmod --gui
Icon=network-vpn
Terminal=false
Type=Application
Categories=Network;VPN;
DESKTOP

echo ""
echo "✅ DONE! Zorin NetMod VPN installed!"
echo ""
echo "Usage:"
echo "  netmod --config configs/example.json --start"
echo "  netmod --gui"
echo "  netmod --list-configs"
echo ""
echo "GUI: App Menu > Zorin NetMod VPN"
echo "CLI: netmod --help"
echo ""
echo "Example config in $INSTALL_DIR/configs/"
ls "$INSTALL_DIR/configs/" || true
