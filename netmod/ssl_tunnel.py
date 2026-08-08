import socket
import ssl

class SSLTunnel:
    def __init__(self, config):
        self.config = config

    def connect(self):
        bug_host = self.config.get('bug_host')
        ssh_host = self.config.get('ssh_host')
        sni = self.config.get('sni', bug_host)

        target_host = bug_host if bug_host else ssh_host
        target_port = self.config.get('ssh_port', 443)

        try:
            print(f"[SSL] Connecting to {target_host}:{target_port} with SNI {sni}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ssl_sock = context.wrap_socket(sock, server_hostname=sni)
            ssl_sock.connect((target_host, target_port))
            print("[SSL] SSL handshake OK with SNI")
            return ssl_sock
        except Exception as e:
            print(f"[SSL] Error: {e}")
            return None
