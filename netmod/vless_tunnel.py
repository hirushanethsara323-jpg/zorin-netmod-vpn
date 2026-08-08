"""
VLESS protocol support for Zorin NetMod VPN
URL: vless://uuid@host:port?encryption=none&type=tcp&security=tls&sni=aka.ms#name
Spec: https://xtls.github.io/config/outbounds/vless.html
"""

import socket
import ssl
import struct
import uuid

class VlessTunnel:
    def __init__(self, url):
        self.url = url
        self.parsed = self.parse_vless_url(url)
        self.sock = None

    def parse_vless_url(self, url):
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        uuid_str = parsed.username or ""
        host = parsed.hostname
        port = parsed.port or 443
        query = urllib.parse.parse_qs(parsed.query)
        params = {k: v[0] if len(v)==1 else v for k,v in query.items()}
        name = urllib.parse.unquote(parsed.fragment) if parsed.fragment else f"{host}:{port}"
        return {
            "uuid": uuid_str,
            "host": host,
            "port": port,
            "sni": params.get("sni", ""),
            "type": params.get("type", "tcp"),
            "security": params.get("security", "tls"),
            "encryption": params.get("encryption", "none"),
            "alpn": params.get("alpn", "h2,http/1.1"),
            "name": name,
            "params": params
        }

    def connect(self, target_host="1.1.1.1", target_port=80):
        p = self.parsed
        print(f"[VLESS] {p['name']} - {p['host']}:{p['port']} SNI: {p['sni']}")
        print(f"[VLESS] UUID: {p['uuid'][:8]}...")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            print(f"[VLESS] TCP connect to {p['host']}:{p['port']}")
            sock.connect((p['host'], p['port']))

            if p['security'] == 'tls':
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sni = p['sni'] if p['sni'] else p['host']
                print(f"[VLESS] TLS handshake SNI: {sni}")
                sock = ctx.wrap_socket(sock, server_hostname=sni)
                print(f"[VLESS] TLS OK {sock.cipher()}")

            # VLESS handshake
            # Version 0, UUID 16 bytes, Addon len 0, Command 1 TCP, Port, ATYP + Addr
            # UUID string to bytes
            try:
                uuid_bytes = uuid.UUID(p['uuid']).bytes
            except:
                # If not valid UUID, use first 16 bytes of string
                uuid_bytes = p['uuid'].encode()[:16].ljust(16, b'\0')

            ver = b'\x00'
            addon_len = b'\x00'
            cmd = b'\x01'  # 1 TCP, 2 UDP, 3 MUX
            port_bytes = struct.pack('>H', target_port)

            # ATYP + ADDR
            try:
                ip = socket.inet_aton(target_host)
                atyp = b'\x01'
                addr = ip
            except:
                atyp = b'\x03'
                addr = bytes([len(target_host)]) + target_host.encode()

            req = ver + uuid_bytes + addon_len + cmd + port_bytes + atyp + addr
            print(f"[VLESS] Sending handshake to {target_host}:{target_port}")
            sock.sendall(req)

            # Normally server replies? VLESS has no explicit reply before tunneling, just starts tunneling
            print(f"[VLESS] Tunnel established to {target_host}:{target_port} via {p['host']}")
            self.sock = sock
            return True

        except Exception as e:
            print(f"[VLESS] Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else ""
    if url:
        t = VlessTunnel(url)
        print(t.parsed)
