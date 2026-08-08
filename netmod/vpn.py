from .ssh_tunnel import SSHTunnel
from .websocket_tunnel import WebSocketTunnel
from .ssl_tunnel import SSLTunnel
import time

class NetModVPN:
    def __init__(self, config):
        self.config = config
        self.ssh_tunnel = None
        self.running = False

    def start(self):
        print(f"\n🌀 Starting Zorin NetMod VPN - {self.config.get('name')}")
        print(f"Tunnel Type: {self.config.get('tunnel_type')}")
        print(f"Bug Host: {self.config.get('bug_host')} SNI: {self.config.get('sni')}")
        print(f"SSH: {self.config.get('ssh_user')}@{self.config.get('ssh_host')}:{self.config.get('ssh_port')}")
        print(f"Proxy: HTTP :{self.config.get('proxy_port', 8888)} SOCKS :{self.config.get('socks_port', 1080)}")
        print("")

        tunnel_type = self.config.get('tunnel_type', 'ssh')

        # Handle different tunnel types like NetMod
        if 'ws' in tunnel_type:
            ws = WebSocketTunnel(self.config)
            if not ws.connect():
                print("[VPN] WebSocket failed")
                return False
            # In real NetMod, SSH goes over WS socket
            # For demo, we still start SSH over the WS is complex, so we start SSH direct
            # Real implementation would forward SSH via WS socket using port forwarding

        if 'ssl' in tunnel_type:
            ssl_tun = SSLTunnel(self.config)
            # SSL tunnel would be used

        # Start SSH SOCKS tunnel
        self.ssh_tunnel = SSHTunnel(self.config)
        if not self.ssh_tunnel.start():
            print("[VPN] Failed to start SSH tunnel - check SSH account")
            return False

        self.running = True
        print("\n✅ VPN Started! Configure browser/system proxy:")
        print(f"  HTTP Proxy: 127.0.0.1:{self.config.get('proxy_port', 8888)}")
        print(f"  SOCKS5 Proxy: 127.0.0.1:{self.config.get('socks_port', 1080)}")
        print(f"  DNS: {self.config.get('dns', '1.1.1.1')}")
        print("\n  Zorin Settings > Network > Proxy > Manual -> HTTP 127.0.0.1 8888")
        print("\n  Press Ctrl+C to stop")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

        return True

    def stop(self):
        self.running = False
        if self.ssh_tunnel:
            self.ssh_tunnel.stop()
        print("\n🛑 VPN Stopped")
