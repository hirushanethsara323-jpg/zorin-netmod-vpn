# Zorin NetMod VPN - NetMod-like VPN for Linux (Zorin OS) 🌀🔐

**NetMod wage VPN ekak Linux (Zorin OS) ekata! SSH/SSL/WebSocket tunneling + Bug Host + Payload**

Android NetMod app eke wage Linux eke free internet config use karanna puluwan VPN ekak!

### Features - NetMod wage

✅ **SSH Tunneling** - SSH account + dynamic port forwarding (-D 1080)
✅ **SSL/TLS Tunneling** - SNI / Bug Host support
✅ **WebSocket Tunneling** - WS/WSS + custom payload (HTTP injection)
✅ **Payload / Bug Host** - `CONNECT` method, `GET` with bug.com, X-Online-Host, etc.
✅ **SSH + SSL + WebSocket Combo** - SSH over WebSocket over SSL (NetMod trick)
✅ **Proxy** - HTTP proxy :8888 + SOCKS5 :1080
✅ **Config Import** - JSON config (NetMod .nm wage)
✅ **Free Internet Configs** - configs/ folder eke
✅ **CLI + GUI** - Terminal + Tkinter GUI for Zorin

### One-Command Install for Zorin OS

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/hirushanethsara323-jpg/zorin-netmod-vpn/main/install.sh)"
```

### Manual Install

```bash
git clone https://github.com/hirushanethsara323-jpg/zorin-netmod-vpn.git
cd zorin-netmod-vpn
chmod +x install.sh
./install.sh
```

### Usage

**CLI:**
```bash
netmod --config configs/example.json --start
netmod --config configs/free_internet_example.json --start
netmod --gui  # Open GUI
netmod --list-configs
```

**GUI:**
```bash
python3 gui/main.py
# or
netmod --gui
```

### Config Example

```json
{
  "name": "Free Internet - Dialog",
  "ssh_host": "sg1.sshdropbear.net",
  "ssh_port": 443,
  "ssh_user": "user",
  "ssh_pass": "pass",
  "tunnel_type": "ws-ssl",
  "bug_host": "www.dialog.lk",
  "sni": "www.dialog.lk",
  "payload": "GET / HTTP/1.1[crlf]Host: [host][crlf]X-Online-Host: [host][crlf][crlf]",
  "ws_path": "/",
  "proxy_port": 8888,
  "socks_port": 1080,
  "dns": "1.1.1.1"
}
```

Payload keywords: `[host]`, `[port]`, `[crlf]`, `[lf]`, `[method]`

### How NetMod Trick Works (Linux eke)

1. **Bug Host / SNI:** ISP eke free host (e.g., `www.dialog.lk`) use karala data free karanawa
2. **Payload:** `GET / HTTP/1.1
Host: bug.com
X-Online-Host: bug.com` wage custom header eken ISP bypass
3. **WebSocket:** Bug host eka WebSocket upgrade karala, athule SSH tunnel
4. **SSL:** SNI bug.com dala TLS handshake, athule SSH
5. **Result:** Free internet via SSH account!

### Requirements

- Zorin OS / Ubuntu 20.04+
- Python3, SSH, Stunnel, Python websockets

### Repo Structure

```
zorin-netmod-vpn/
├── install.sh - One-command installer
├── netmod/ - Core module
│   ├── cli.py - CLI
│   ├── ssh_tunnel.py - SSH -D 1080
│   ├── ssl_tunnel.py - SSL/TLS + SNI
│   ├── websocket_tunnel.py - WS/WSS + payload
│   ├── payload.py - Bug host payload generator
│   └── config.py - Config load/save
├── configs/ - Example configs
├── gui/main.py - Tkinter GUI Zorin style
└── tools/ - Helper tools
```

### Disclaimer

Educational purpose only. Use your own SSH accounts. Respect ISP ToS. Free internet tricks depend on ISP.

### Made for Zorin OS

Zorin OS eke Windows wage look ekath ekka NetMod wage VPN!

By: hirushanethsara323-jpg | Zero OS Team

### Colab Link

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hirushanethsara323-jpg/zorin-netmod-vpn/blob/main/colab.ipynb)

---

## 🆕 v1.1 Trojan Support - NetMod eke hodatama wada!

**Tested Trojan URL from user:**
```
trojan://1a23c3c4-1665-41d1-9c3c-3df4bb9933c9@us.cloudnet.one:443?type=tcp&headerType=none&security=tls&sni=aka.ms&alpn=h2,http/1.1#US-1-cloudnetfreev2ray-8f57
```

**Test Result in Linux (Python):**
```
[Trojan] TLS handshake with SNI: aka.ms
[Trojan] TLS OK, cipher: ('TLS_AES_128_GCM_SHA256', 'TLSv1.3', 128)
[Trojan] Tunnel to 1.1.1.1:80 established via us.cloudnet.one (SNI aka.ms)
Received via Trojan tunnel: 381 bytes HTTP 301 Moved Permanently from Cloudflare
✅ Trojan works! NetMod wage wada!
```

**How to use:**
- CLI: `netmod --trojan "trojan://..." --start` or `--test-trojan`
- GUI: Paste Trojan URL in Trojan field → Test Trojan → Connect Trojan
- SNI `aka.ms` is bug host / domain fronting trick - TLS handshake with SNI aka.ms to us.cloudnet.one

**Trojan Protocol:**
1. TCP connect to us.cloudnet.one:443
2. TLS wrap with SNI aka.ms (domain fronting)
3. Send SHA224(password) + \r\n + CONNECT request to target (e.g., 8.8.8.8:53)
4. Tunnel established, now SOCKS5 127.0.0.1:1080 forwards via Trojan

**Zorin Install:**
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/hirushanethsara323-jpg/zorin-netmod-vpn/main/install.sh)"
netmod --gui
# Paste Trojan URL in Trojan field
```

---

## 🆕 v2.0 Mega - Okkoma Hodatama - All Protocols Perfect

**New Protocols Added (User Request: Okkoma hodatama hadanna):**

- **VMess** `vmess://` - V2Ray VMess with UUID, TLS SNI, WS path, base64 JSON parsing
  - Test: `netmod --test-vmess 'vmess://...'`
  - Example: `vmess://eyJ2IjoiMiIsInBzIjoi...` (base64 JSON with add, port, id, net, tls, sni)

- **Shadowsocks** `ss://` - SS with method:password@host:port
  - Supports `ss://base64(method:password)@host:port` and `ss://base64(method:password@host:port)`
  - Test: `netmod --test-ss 'ss://...'`

- **Subscription** - Fetch list of Trojan/VLESS/VMess/SS from URL (base64 encoded sub.txt like free VPN subs)
  - `netmod --sub https://example.com/sub.txt` -> saves to `configs/subscription.txt`
  - Supports plain list and base64 decoded list

- **Speedtest** - Test latency of proxies
  - `netmod --speedtest` - tests all configs and subscription proxies, sorted by ms

**All Protocols Now (Okkoma):**
- SSH, SSL/TLS + SNI, WebSocket WS/WSS + payload, Trojan (tested working SNI aka.ms), VLESS (tested working), VMess, Shadowsocks, plus combo ws-ssl, etc.

**GUI Updated v2.0 Mega:**
- Trojan field + VLESS field + VMess + SS fields
- Test buttons for each protocol
- Subscription fetch + Speedtest buttons
- Log shows all protocols tested working!

**Tested Working:**
- Trojan: `us.cloudnet.one:443` SNI `aka.ms` TLS_AES_128_GCM_SHA256 → 381 bytes HTTP 301
- VLESS: `sgping.cloudnet-movies.win:443` SNI `aka.ms` → 383 bytes HTTP 301
- Both use SNI aka.ms domain fronting trick - NetMod eke hodatama wada!

**How to use all protocols:**
```bash
netmod --trojan "trojan://..." 
netmod --vless "vless://..."
netmod --vmess "vmess://..."
netmod --ss "ss://..."
netmod --sub https://raw.githubusercontent.com/.../sub.txt
netmod --speedtest
netmod --gui # All protocols in GUI
```

**One-command install still works:**
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/hirushanethsara323-jpg/zorin-netmod-vpn/main/install.sh)"
```
---

## 📦 AppImage - Single File, No Install, GUI Only, Terminal Nathi!

**User Request:** "Mata appimage ekak okata hadannako" - AppImage haduwa!

**Download & Run - Zorin OS eke one command:**

```bash
# Download AppImage
wget https://github.com/hirushanethsara323-jpg/zorin-netmod-vpn/releases/download/v2.0/Zorin-NetMod-VPN-x86_64.AppImage

# Make executable
chmod +x Zorin-NetMod-VPN-x86_64.AppImage

# Run GUI only, terminal nathiwa!
./Zorin-NetMod-VPN-x86_64.AppImage
# or
./Zorin-NetMod-VPN-x86_64.AppImage --gui
```

**AppImage Features:**
- Single file 210K, no install needed
- No terminal - GUI only (`Terminal=false`)
- All protocols: SSH, SSL, WS, Trojan (tested SNI aka.ms working), VLESS (tested working), VMess, SS, Subscription, Speedtest
- Works on Zorin OS, Ubuntu, any Linux distro
- No dependencies except python3 + python3-tk + paramiko + websockets (installed via system python)
- AppRun sets PYTHONPATH to bundled netmod package

**GUI Only Mode:**
```bash
nohup ./Zorin-NetMod-VPN-x86_64.AppImage >/dev/null 2>&1 &
# Terminal close karath GUI thiyenawa!
```

**Desktop Integration:**
```bash
# Extract and integrate to App Menu
./Zorin-NetMod-VPN-x86_64.AppImage --appimage-extract
cp squashfs-root/netmod.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
# Now Super key -> NetMod -> GUI witharai!
```

**CLI still works via AppImage:**
```bash
./Zorin-NetMod-VPN-x86_64.AppImage --cli --help
./Zorin-NetMod-VPN-x86_64.AppImage --cli --test-trojan "trojan://..."
./Zorin-NetMod-VPN-x86_64.AppImage --cli --test-vless "vless://..."
```

**Build AppImage Yourself:**
```bash
git clone https://github.com/hirushanethsara323-jpg/zorin-netmod-vpn.git
cd zorin-netmod-vpn
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage --appimage-extract
# Build
ARCH=x86_64 ./squashfs-root/AppRun AppDir Zorin-NetMod-VPN-x86_64.AppImage
```

**Size:** 210K only! (Python app, uses system python3)
