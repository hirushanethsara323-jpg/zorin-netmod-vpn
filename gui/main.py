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
except:
    from config import list_configs, load_config
    from vpn import NetModVPN
    from payload import get_default_payloads

class NetModGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zorin NetMod VPN - NetMod-like VPN for Linux")
        self.root.geometry("700x600")
        self.vpn = None

        # Title
        ttk.Label(root, text="🌀 Zorin NetMod VPN", font=("Arial", 18, "bold")).pack(pady=10)
        ttk.Label(root, text="NetMod-like VPN for Linux (Zorin OS) - SSH/SSL/WebSocket", font=("Arial", 10)).pack()

        # Config list
        frame = ttk.Frame(root)
        frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(frame, text="Config:").pack(anchor=tk.W)
        self.config_var = tk.StringVar()
        self.config_combo = ttk.Combobox(frame, textvariable=self.config_var, width=60)
        self.refresh_configs()
        self.config_combo.pack(fill=tk.X, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_configs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load", command=self.load_selected).pack(side=tk.LEFT, padx=5)

        # Fields
        fields_frame = ttk.LabelFrame(root, text="Config Details")
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.entries = {}
        fields = [
            ("Name", "name"),
            ("SSH Host", "ssh_host"),
            ("SSH Port", "ssh_port"),
            ("SSH User", "ssh_user"),
            ("SSH Pass", "ssh_pass"),
            ("Tunnel Type (ssh/ws/ssl/ws-ssl)", "tunnel_type"),
            ("Bug Host", "bug_host"),
            ("SNI", "sni"),
            ("WS Path", "ws_path"),
            ("Payload", "payload"),
            ("HTTP Proxy Port", "proxy_port"),
            ("SOCKS Port", "socks_port")
        ]

        for i, (label, key) in enumerate(fields):
            row = ttk.Frame(fields_frame)
            row.pack(fill=tk.X, pady=2, padx=5)
            ttk.Label(row, text=label, width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(row)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key] = entry

        # Payload presets
        payload_frame = ttk.Frame(fields_frame)
        payload_frame.pack(fill=tk.X, pady=5)
        ttk.Label(payload_frame, text="Payload Preset:").pack(side=tk.LEFT)
        self.payload_combo = ttk.Combobox(payload_frame, values=list(get_default_payloads().keys()))
        self.payload_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(payload_frame, text="Use", command=self.use_payload_preset).pack(side=tk.LEFT)

        # Buttons
        action_frame = ttk.Frame(root)
        action_frame.pack(fill=tk.X, padx=20, pady=10)
        self.start_btn = ttk.Button(action_frame, text="START VPN", command=self.start_vpn)
        self.start_btn.pack(side=tk.LEFT, padx=5, ipadx=20)
        ttk.Button(action_frame, text="STOP", command=self.stop_vpn).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Save Config", command=self.save_config).pack(side=tk.LEFT, padx=5)

        # Log
        log_frame = ttk.LabelFrame(root, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.log_text = tk.Text(log_frame, height=10, font=("Monospace", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def refresh_configs(self):
        configs = list_configs()
        self.config_combo['values'] = configs
        if configs:
            self.config_combo.set(configs[0])

    def load_selected(self):
        path = self.config_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Select valid config")
            return
        try:
            with open(path, 'r') as f:
                cfg = json.load(f)
            for key, entry in self.entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, str(cfg.get(key, "")))
            self.log(f"Loaded {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def use_payload_preset(self):
        preset = self.payload_combo.get()
        payloads = get_default_payloads()
        if preset in payloads:
            self.entries['payload'].delete(0, tk.END)
            self.entries['payload'].insert(0, payloads[preset])

    def get_current_config(self):
        cfg = {}
        for key, entry in self.entries.items():
            val = entry.get()
            # Try int conversion for ports
            if key in ['ssh_port', 'proxy_port', 'socks_port']:
                try:
                    cfg[key] = int(val)
                except:
                    cfg[key] = val
            else:
                cfg[key] = val
        return cfg

    def save_config(self):
        cfg = self.get_current_config()
        path = filedialog.asksaveasfilename(defaultextension=".json", initialdir="configs", filetypes=[("JSON", "*.json")])
        if path:
            with open(path, 'w') as f:
                json.dump(cfg, f, indent=2)
            self.log(f"Saved to {path}")
            self.refresh_configs()

    def start_vpn(self):
        cfg = self.get_current_config()
        self.log(f"Starting VPN {cfg.get('name')} type {cfg.get('tunnel_type')}")
        self.log(f"Bug Host: {cfg.get('bug_host')} SNI: {cfg.get('sni')}")
        # In real, start in thread
        self.vpn = NetModVPN(cfg)
        # For demo, just log, not actually start blocking
        self.log("VPN would start here - SSH SOCKS :1080 HTTP :8888")
        self.log("Configure Zorin Settings > Network > Proxy > Manual HTTP 127.0.0.1 8888")
        messagebox.showinfo("VPN", "VPN Started (demo) - Check log for proxy settings. Real SSH would connect now.")

    def stop_vpn(self):
        if self.vpn:
            self.vpn.stop()
            self.log("VPN Stopped")
        else:
            self.log("No VPN running")

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = NetModGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
