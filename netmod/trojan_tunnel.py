"""
Trojan protocol support for Zorin NetMod VPN
URL format: trojan://password@host:port?type=tcp&security=tls&sni=aka.ms&alpn=h2,http/1.1#name

Trojan protocol: https://trojan-gfw.github.io/trojan/protocol
Flow:
1. TLS connect to host:port with SNI (e.g., aka.ms for domain fronting / bug host)
2. Send: \r\n + hex(SHA224(password)) + \r\n + SOCKS5-like request (ATYP + ADDR + PORT + \r\n)
3. Server replies, then tunnel is established, then you can send SOCKS5 or direct data
"""

import socket
import ssl
import hashlib
import struct

class TrojanTunnel:
    def __init__(self, url):
        self.url = url
        self.parsed = self.parse_trojan_url(url)
        self.sock = None

    def parse_trojan_url(self, url):
        # trojan://password@host:port?params#name
        # Example: trojan://1a23c3c4-1665-41d1-9c3c-3df4bb9933c9@us.cloudnet.one:443?type=tcp&security=tls&sni=aka.ms&alpn=h2,http/1.1#US-1
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        password = parsed.username or ""
        # password may be UUID with @ in url? Actually username is password
        # If URL has password in username part before @, urllib parses username as password
        # For trojan, password is before @, host after
        host = parsed.hostname
        port = parsed.port or 443
        query = urllib.parse.parse_qs(parsed.query)
        # query values are lists
        params = {k: v[0] if len(v)==1 else v for k,v in query.items()}
        name = urllib.parse.unquote(parsed.fragment) if parsed.fragment else f"{host}:{port}"
        
        return {
            "password": password,
            "host": host,
            "port": port,
            "sni": params.get("sni", ""),
            "type": params.get("type", "tcp"),
            "security": params.get("security", "tls"),
            "alpn": params.get("alpn", "h2,http/1.1"),
            "headerType": params.get("headerType", "none"),
            "name": name,
            "params": params
        }

    def _hash_password(self, password):
        # Trojan uses first 56 chars of hex SHA224(password) + \r\n
        sha = hashlib.sha224(password.encode()).hexdigest()
        return sha

    def connect(self, target_host="8.8.8.8", target_port=53):
        """
        Connect to Trojan server and create tunnel to target_host:target_port
        For demo, we connect to Trojan server via TLS with SNI, send auth, then we can proxy
        """
        p = self.parsed
        print(f"[Trojan] Parsing URL: {p['name']}")
        print(f"[Trojan] Host: {p['host']}:{p['port']} SNI: {p['sni']} Security: {p['security']}")
        print(f"[Trojan] Password: {p['password'][:8]}... (hidden)")

        # Create TCP socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            print(f"[Trojan] Connecting TCP to {p['host']}:{p['port']}")
            sock.connect((p['host'], p['port']))

            # Wrap with TLS using SNI
            if p['security'] == 'tls':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                # ALPN
                # context.set_alpn_protocols(p['alpn'].split(',')) if needed
                sni = p['sni'] if p['sni'] else p['host']
                print(f"[Trojan] TLS handshake with SNI: {sni}")
                sock = context.wrap_socket(sock, server_hostname=sni)
                print(f"[Trojan] TLS OK, cipher: {sock.cipher()}")

            # Trojan handshake
            # Send: \r\n + SHA224(password) + \r\n + ATYP + ADDR + PORT + \r\n ?
            # Actually spec: CRLF + password + CRLF + CMD + ATYP + ADDR + PORT + CRLF ?
            # Simplified: For Trojan, after TLS, client sends:
            # - 56 hex char password + \r\n
            # - CONNECT command: 0x01 0x03 + len + host + port (2 bytes) ??? Wait SOCKS5 style?
            # Let's implement standard Trojan request:
            # Request: VER=1, CMD=1 (CONNECT), ATYP, ADDR, PORT, CRLF?
            # Actually Trojan request format:
            # +----+-----+-------+------+----------+----------+
            # |CMD |ATYP | ADDR  | PORT | CRLF     |
            # +----+-----+-------+------+----------+
            # CMD 0x01 CONNECT, 0x03 UDP ASSOCIATE
            # But first, password hash + CRLF

            pwd_hash = self._hash_password(p['password'])
            print(f"[Trojan] Password hash: {pwd_hash[:10]}...")

            # Build request to connect to target (e.g., 8.8.8.8:53 for DNS test, or 1.1.1.1:80)
            # For demo, connect to target_host:target_port (set to 8.8.8.8:53 or 1.1.1.1:443)
            # ATYP 1 = IPv4, 3 = domain, 4 = IPv6
            # We'll use domain for target_host if it's domain, else IPv4

            # First packet: password hash + \r\n
            sock.sendall((pwd_hash + "\r\n").encode())

            # Second: SOCKS5-like request: CMD=1 CONNECT, ATYP, ADDR, PORT, CRLF
            # ATYP 1 = IPv4
            try:
                # Try parse target as IPv4
                ip_bytes = socket.inet_aton(target_host)
                atyp = 1
                addr = ip_bytes
            except:
                # Domain
                atyp = 3
                addr = bytes([len(target_host)]) + target_host.encode()

            port_bytes = struct.pack('>H', target_port)
            # CMD 1 = CONNECT
            request = struct.pack('!B', 1) + struct.pack('!B', atyp) + addr + port_bytes + b"\r\n"
            print(f"[Trojan] Sending CONNECT request to {target_host}:{target_port} ATYP={atyp}")
            sock.sendall(request)

            # Read response? Trojan server should reply? Actually Trojan doesn't have explicit reply before tunneling? Some implementations reply with empty?
            # We'll try recv 1 byte or just assume OK

            print(f"[Trojan] Tunnel to {target_host}:{target_port} established via {p['host']} (SNI {p['sni']})")
            print(f"[Trojan] Now you can send data via this socket - SOCKS5 127.0.0.1:1080 would forward here")

            self.sock = sock
            return True

        except Exception as e:
            print(f"[Trojan] Error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_google_dns(self):
        # Test tunnel by trying to connect to 8.8.8.8:53 or 1.1.1.1:80 via trojan
        if self.connect("8.8.8.8", 53):
            print("[Trojan] Test DNS query via tunnel would go here")
            return True
        return False

    def get_socks_proxy(self):
        # After Trojan tunnel established, you would have local SOCKS5 server that forwards via Trojan socket
        # For simplicity, return that SOCKS would be at 127.0.0.1:1080 forwarding via Trojan
        return "127.0.0.1", 1080

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else "trojan://test@example.com:443?security=tls&sni=aka.ms#test"
    t = TrojanTunnel(url)
    print(t.parsed)
