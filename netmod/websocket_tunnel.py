"""
WebSocket tunneling with custom payload (NetMod trick: SSH over WebSocket)
"""
import socket
import ssl
import base64

class WebSocketTunnel:
    def __init__(self, config):
        self.config = config
        self.sock = None

    def _build_ws_payload(self):
        from .payload import generate_payload, get_default_payloads
        template = self.config.get('payload', get_default_payloads()['ws_upgrade'])
        bug_host = self.config.get('bug_host', '')
        ssh_host = self.config.get('ssh_host', '')
        ssh_port = self.config.get('ssh_port', 443)
        return generate_payload(template, bug_host, ssh_host, ssh_port, method="GET")

    def connect(self):
        bug_host = self.config.get('bug_host')
        ssh_host = self.config.get('ssh_host')
        ssh_port = self.config.get('ssh_port', 443)
        ws_path = self.config.get('ws_path', '/')
        use_ssl = 'ssl' in self.config.get('tunnel_type', '')

        # For demo, create TCP connection to bug_host:443 and send WS upgrade with payload
        try:
            target_host = bug_host if bug_host else ssh_host
            target_port = 443 if use_ssl else 80
            
            print(f"[WS] Connecting to {target_host}:{target_port} via {self.config.get('tunnel_type')}")
            print(f"[WS] Bug Host: {bug_host}, SNI: {self.config.get('sni')}")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target_host, target_port))

            if use_ssl:
                # Wrap with SSL using SNI bug_host
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sni = self.config.get('sni', bug_host)
                sock = context.wrap_socket(sock, server_hostname=sni)
                print(f"[WS] SSL wrapped with SNI: {sni}")

            # Send WebSocket payload
            payload = self._build_ws_payload()
            # Replace [host] etc already done, add WS headers
            if 'Upgrade: websocket' not in payload:
                # Build proper WS upgrade
                ws_key = base64.b64encode(b'the sample nonce').decode()
                payload = (
                    f"GET {ws_path} HTTP/1.1\r\n"
                    f"Host: {bug_host}\r\n"
                    f"Upgrade: websocket\r\n"
                    f"Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Key: {ws_key}\r\n"
                    f"Sec-WebSocket-Version: 13\r\n"
                    f"X-Online-Host: {bug_host}\r\n"
                    f"\r\n"
                )

            print(f"[WS] Sending payload:\n{payload[:200]}...")
            sock.send(payload.encode())

            # Read response
            resp = sock.recv(1024).decode(errors='ignore')
            print(f"[WS] Response: {resp[:200]}")

            if '101' in resp or 'Switching Protocols' in resp or '200' in resp:
                print("[WS] WebSocket handshake OK! Tunnel established")
                self.sock = sock
                return True
            else:
                print("[WS] Handshake may have failed, but continuing for free internet trick")
                self.sock = sock
                return True

        except Exception as e:
            print(f"[WS] Error: {e}")
            return False

    def get_socket(self):
        return self.sock
