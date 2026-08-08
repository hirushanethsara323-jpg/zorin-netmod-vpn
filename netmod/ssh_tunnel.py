import subprocess
import time
import os

class SSHTunnel:
    def __init__(self, config):
        self.config = config
        self.process = None

    def start(self):
        ssh_host = self.config.get('ssh_host')
        ssh_port = self.config.get('ssh_port', 443)
        ssh_user = self.config.get('ssh_user')
        socks_port = self.config.get('socks_port', 1080)
        
        # Build SSH command with dynamic port forwarding
        cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=60",
            "-D", str(socks_port),
            "-p", str(ssh_port),
            f"{ssh_user}@{ssh_host}",
            "-N"  # No shell
        ]
        
        # If password auth, use sshpass if available
        ssh_pass = self.config.get('ssh_pass')
        if ssh_pass and self._has_sshpass():
            cmd = ["sshpass", "-p", ssh_pass] + cmd
        
        print(f"[SSH] Starting tunnel: {ssh_user}@{ssh_host}:{ssh_port} SOCKS :{socks_port}")
        print(f"[SSH] Command: {' '.join(cmd)}")
        
        try:
            self.process = subprocess.Popen(cmd)
            time.sleep(2)
            if self.process.poll() is None:
                print(f"[SSH] Tunnel started PID {self.process.pid}")
                return True
            else:
                print("[SSH] Failed to start")
                return False
        except Exception as e:
            print(f"[SSH] Error: {e}")
            return False

    def stop(self):
        if self.process:
            self.process.terminate()
            print("[SSH] Tunnel stopped")

    def _has_sshpass(self):
        return os.system("which sshpass > /dev/null 2>&1") == 0
