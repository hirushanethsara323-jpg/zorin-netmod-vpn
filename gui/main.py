import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from netmod.config import list_configs, load_config
    from netmod.vpn import NetModVPN
    from netmod.payload import get_default_payloads
    from netmod.trojan_tunnel import TrojanTunnel
except:
    from config import list_configs, load_config
    from vpn import NetModVPN
    from payload import get_default_payloads
    from trojan_tunnel import TrojanTunnel

class NetModGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zorin NetMod VPN - NetMod-like VPN for Linux + Trojan")
        self.root.geometry("800x700")
        self.vpn = None

        ttk.Label(root, text="🌀 Zorin NetMod VPN + Trojan", font=("Arial", 18, "bold")).pack(pady=10)
        ttk.Label(root, text="SSH/SSL/WebSocket/Trojan - NetMod-like for Zorin OS", font=("Arial", 10)).pack()

        # Trojan quick connect
        trojan_frame = ttk.LabelFrame(root, text="Trojan Quick Connect (NetMod eke hodatama wada)")
        trojan_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(trojan_frame, text="Trojan URL:").pack(anchor=tk.W, padx=5)
        self.trojan_entry = ttk.Entry(trojan_frame, width=80)
        self.trojan_entry.insert(0, "trojan://1a23c3c4-1665-41d1-9c3c-3df4bb9933c9@us.cloudnet.one:443?type=tcp&security=tls&sni=aka.ms#US-1")
        self.trojan_entry.pack(fill=tk.X, padx=5, pady=5)
        btn_frame = ttk.Frame(trojan_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="Test Trojan", command=self.test_trojan).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Connect Trojan", command=self.connect_trojan).pack(side=tk.LEFT, padx=5)

        # Config list
        frame = ttk.Frame(root)
        frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(frame, text="Or SSH/WS Config:").pack(anchor=tk.W)
        self.config_var = tk.StringVar()
        self.config_combo = ttk.Combobox(frame, textvariable=self.config_var, width=60)
        self.refresh_configs()
        self.config_combo.pack(fill=tk.X, pady=5)
        btn_frame2 = ttk.Frame(frame)
        btn_frame2.pack(fill=tk.X)
        ttk.Button(btn_frame2, text="Refresh", command=self.refresh_configs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame2, text="Load", command=self.load_selected).pack(side=tk.LEFT, padx=5)

        # Fields
        fields_frame = ttk.LabelFrame(root, text="Config Details")
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.entries = {}
        fields = [("Name","name"),("SSH Host","ssh_host"),("SSH Port","ssh_port"),("SSH User","ssh_user"),("SSH Pass","ssh_pass"),("Tunnel Type","tunnel_type"),("Bug Host","bug_host"),("SNI","sni"),("WS Path","ws_path"),("Payload","payload"),("HTTP Proxy","proxy_port"),("SOCKS Port","socks_port")]
        for label,key in fields:
            row = ttk.Frame(fields_frame)
            row.pack(fill=tk.X, pady=1, padx=5)
            ttk.Label(row, text=label, width=15).pack(side=tk.LEFT)
            entry = ttk.Entry(row)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key]=entry

        # Buttons
        action_frame = ttk.Frame(root)
        action_frame.pack(fill=tk.X, padx=20, pady=5)
        self.start_btn = ttk.Button(action_frame, text="START VPN", command=self.start_vpn)
        self.start_btn.pack(side=tk.LEFT, padx=5, ipadx=20)
        ttk.Button(action_frame, text="STOP", command=self.stop_vpn).pack(side=tk.LEFT, padx=5)

        # Log
        log_frame = ttk.LabelFrame(root, text="Log - Trojan SNI aka.ms tested working!")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.log_text = tk.Text(log_frame, height=12, font=("Monospace", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def refresh_configs(self):
        configs = list_configs()
        self.config_combo['values'] = configs
        if configs: self.config_combo.set(configs[0])

    def load_selected(self):
        path = self.config_var.get()
        if not path or not os.path.exists(path): return
        try:
            with open(path,'r') as f:
                cfg=json.load(f)
            for k,e in self.entries.items():
                e.delete(0, tk.END)
                e.insert(0, str(cfg.get(k,"")))
            self.log(f"Loaded {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_current_config(self):
        cfg={}
        for k,e in self.entries.items():
            v=e.get()
            if k in ['ssh_port','proxy_port','socks_port']:
                try: cfg[k]=int(v)
                except: cfg[k]=v
            else: cfg[k]=v
        return cfg

    def test_trojan(self):
        url=self.trojan_entry.get()
        if not url: return
        self.log(f"Testing Trojan: {url[:60]}...")
        try:
            t=TrojanTunnel(url)
            ok=t.connect("1.1.1.1", 80)
            if ok:
                self.log("✅ Trojan TLS handshake OK with SNI aka.ms, tunnel established! NetMod wage wada!")
            else:
                self.log("❌ Trojan failed")
        except Exception as e:
            self.log(f"Error: {e}")

    def connect_trojan(self):
        url=self.trojan_entry.get()
        if not url: return
        self.log(f"Connecting Trojan: {url[:60]}...")
        try:
            t=TrojanTunnel(url)
            if t.connect("8.8.8.8",53):
                self.log("✅ Trojan connected! SOCKS 127.0.0.1:1080 via Trojan")
                messagebox.showinfo("Trojan", "Connected! SOCKS 127.0.0.1:1080")
            else:
                self.log("❌ Failed")
        except Exception as e:
            self.log(f"Error {e}")

    def start_vpn(self):
        cfg=self.get_current_config()
        self.log(f"Starting {cfg.get('name')} {cfg.get('tunnel_type')}")
        self.vpn=NetModVPN(cfg)
        self.log("VPN would start - SOCKS :1080 HTTP :8888")

    def stop_vpn(self):
        if self.vpn:
            self.vpn.stop()
            self.log("Stopped")

    def log(self, msg):
        self.log_text.insert(tk.END, msg+"\n")
        self.log_text.see(tk.END)

def main():
    root=tk.Tk()
    app=NetModGUI(root)
    root.mainloop()

if __name__=="__main__":
    main()
