"""
Shadowsocks SS support - ss://
URL: ss://base64(method:password)@host:port#name or ss://base64(method:password@host:port)#name
"""

import base64
import socket
import struct

class SSTunnel:
    def __init__(self, url):
        self.url = url
        self.parsed = self.parse_ss_url(url)

    def parse_ss_url(self, url):
        import urllib.parse
        import base64
        # ss://base64(method:password)@host:port#name or ss://base64(method:password@host:port)#name
        # Try to parse
        if '@' in url.split('#')[0] and '://' in url:
            # Format: ss://base64(method:password)@host:port
            # or ss://base64(method:password@host:port)
            try:
                # Remove ss://
                remaining = url[5:]
                name = ""
                if '#' in remaining:
                    remaining, name = remaining.split('#', 1)
                    name = urllib.parse.unquote(name)
                
                if '@' in remaining:
                    # Could be base64(method:password)@host:port or base64(method:password@host:port)
                    # Try split by @
                    parts = remaining.split('@')
                    if len(parts) == 2:
                        # First part may be base64(method:password)
                        b64_part = parts[0]
                        host_port = parts[1]
                        # Try decode b64
                        try:
                            b64_part += '=' * (-len(b64_part) % 4)
                            decoded = base64.b64decode(b64_part).decode()
                            # decoded should be method:password
                            if ':' in decoded:
                                method, password = decoded.split(':', 1)
                            else:
                                method, password = "aes-256-gcm", decoded
                        except:
                            # If not base64, maybe it's method:password@host:port base64 encoded whole?
                            method, password = "aes-256-gcm", b64_part

                        # Parse host:port
                        if ':' in host_port:
                            host, port = host_port.rsplit(':', 1)
                            port = int(port)
                        else:
                            host, port = host_port, 8388

                    else:
                        # Single part that is base64 of method:password@host:port
                        try:
                            remaining_b64 = remaining
                            remaining_b64 += '=' * (-len(remaining_b64) % 4)
                            decoded = base64.b64decode(remaining_b64).decode()
                            # decoded format method:password@host:port
                            # Split
                            if '@' in decoded:
                                method_pass, host_port = decoded.rsplit('@', 1)
                                if ':' in method_pass:
                                    method, password = method_pass.split(':', 1)
                                else:
                                    method, password = "aes-256-gcm", method_pass
                                if ':' in host_port:
                                    host, port = host_port.rsplit(':', 1)
                                    port = int(port)
                                else:
                                    host, port = host_port, 8388
                            else:
                                method, password, host, port = "aes-256-gcm", "", "unknown", 8388
                        except Exception as e:
                            print(f"SS parse error {e}")
                            method, password, host, port = "aes-256-gcm", "", "unknown", 8388
                else:
                    # Only base64 part, no @
                    method, password, host, port = "aes-256-gcm", "", "unknown", 8388

            except Exception as e:
                print(f"SS parse exception {e}")
                method, password, host, port = "aes-256-gcm", "", "unknown", 8388
                name = "SS"
        else:
            method, password, host, port, name = "aes-256-gcm", "", "unknown", 8388, "SS"

        return {
            "method": method,
            "password": password,
            "host": host,
            "port": port,
            "name": name
        }

    def connect(self, target_host="1.1.1.1", target_port=80):
        p = self.parsed
        print(f"[SS] {p['name']} - {p['host']}:{p['port']} Method: {p['method']}")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            print(f"[SS] TCP connect to {p['host']}:{p['port']}")
            sock.connect((p['host'], p['port']))
            print(f"[SS] Connected, now SOCKS5 handshake would happen with method {p['method']}")
            # SS handshake: send target via encrypted? For demo, just say OK
            print(f"[SS] Tunnel to {target_host}:{target_port} via {p['host']} (sim)")
            self.sock = sock
            return True
        except Exception as e:
            print(f"[SS] Error: {e}")
            return False

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else ""
    if url:
        t = SSTunnel(url)
        print(t.parsed)
