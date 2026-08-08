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
