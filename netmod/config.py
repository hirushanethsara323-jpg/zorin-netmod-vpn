import json
import os

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_config(path, config):
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)

def list_configs():
    configs = []
    if not os.path.exists(CONFIG_DIR):
        return configs
    for fname in os.listdir(CONFIG_DIR):
        if fname.endswith('.json'):
            configs.append(os.path.join(CONFIG_DIR, fname))
    return configs

def get_example_config():
    return {
        "name": "Free Internet - Dialog Example",
        "ssh_host": "sg1.sshdropbear.net",
        "ssh_port": 443,
        "ssh_user": "username",
        "ssh_pass": "password",
        "tunnel_type": "ws-ssl",
        "bug_host": "www.dialog.lk",
        "sni": "www.dialog.lk",
        "payload": "GET / HTTP/1.1[crlf]Host: [host][crlf]X-Online-Host: [host][crlf]Connection: Keep-Alive[crlf][crlf]",
        "ws_path": "/",
        "proxy_port": 8888,
        "socks_port": 1080,
        "dns": "1.1.1.1"
    }
