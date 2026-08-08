"""
VMess protocol support - for Zorin NetMod VPN
URL: vmess://base64(json) - V2Ray VMess
"""

import base64
import json
import socket
import ssl
import struct

class VmessTunnel:
    def __init__(self, url):
        self.url = url
        self.parsed = self.parse_vmess_url(url)

    def parse_vmess_url(self, url):
        # vmess://base64(json) - json contains v, ps, add, port, id, aid, net, type, host, path, tls, sni
        import urllib.parse
        import base64
        # Remove vmess://
        b64 = url.replace('vmess://', '')
        # Add padding if needed
        b64 += '=' * (-len(b64) % 4)
        try:
            decoded = base64.b64decode(b64).decode()
            data = json.loads(decoded)
        except Exception as e:
            # Try as direct json? Sometimes vmess:// is already with query params?
            # Fallback: try parse as URL with params like vless
            try:
                parsed = urllib.parse.urlparse(url)
                # Some vmess uses query params
                data = {"add": parsed.hostname, "port": parsed.port, "id": parsed.username, "ps": urllib.parse.unquote(parsed.fragment)}
            except:
                data = {"ps": "VMess", "add": "unknown", "port": 443, "id": "unknown"}

        return {
            "name": data.get('ps', 'VMess'),
            "host": data.get('add', ''),
            "port": int(data.get('port', 443)),
            "uuid": data.get('id', ''),
            "aid": data.get('aid', 0),
            "net": data.get('net', 'tcp'),
            "type": data.get('type', 'none'),
            "host_header": data.get('host', ''),
            "path": data.get('path', '/'),
            "tls": data.get('tls', ''),
            "sni": data.get('sni', ''),
            "raw": data
        }

    def connect(self, target_host="1.1.1.1", target_port=80):
        p = self.parsed
        print(f"[VMess] {p['name']} - {p['host']}:{p['port']} SNI: {p['sni']} Net: {p['net']} TLS: {p['tls']}")
        print(f"[VMess] UUID: {p['uuid'][:8]}...")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            print(f"[VMess] TCP connect to {p['host']}:{p['port']}")
            sock.connect((p['host'], p['port']))

            if p['tls'] in ['tls', 'reality']:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sni = p['sni'] if p['sni'] else p['host']
                print(f"[VMess] TLS handshake SNI: {sni}")
                sock = ctx.wrap_socket(sock, server_hostname=sni)
                print(f"[VMess] TLS OK {sock.cipher()}")

            # VMess handshake is complex (requires time, UUID, etc.)
            # For demo, we simulate - real V2Ray would do full handshake
            # Here we just show that we can connect via TLS with SNI
            print(f"[VMess] Handshake to {target_host}:{target_port} via {p['host']} (sim, real Xray-core would do full VMess AEAD)")
            print(f"[VMess] Tunnel established (sim)")

            self.sock = sock
            return True

        except Exception as e:
            print(f"[VMess] Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else ""
    if url:
        t = VmessTunnel(url)
        print(t.parsed)
