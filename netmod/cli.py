import argparse
import json
import os
from .config import load_config, list_configs, get_example_config
from .vpn import NetModVPN
from .trojan_tunnel import TrojanTunnel
from .vless_tunnel import VlessTunnel

def main():
    parser = argparse.ArgumentParser(description="Zorin NetMod VPN - SSH/SSL/WS/Trojan/VLESS for Linux")
    parser.add_argument('--config', '-c', help='Config file path (JSON)')
    parser.add_argument('--trojan', help='Trojan URL trojan://...')
    parser.add_argument('--vless', help='VLESS URL vless://...')
    parser.add_argument('--start', action='store_true', help='Start VPN')
    parser.add_argument('--gui', action='store_true', help='Open GUI')
    parser.add_argument('--list-configs', action='store_true', help='List configs')
    parser.add_argument('--create-example', action='store_true', help='Create example config')
    parser.add_argument('--test-trojan', help='Test Trojan URL')
    parser.add_argument('--test-vless', help='Test VLESS URL')
    args = parser.parse_args()

    if args.list_configs:
        configs = list_configs()
        print("Available configs:")
        for cfg in configs:
            print(f"  - {cfg}")
        return

    if args.create_example:
        example = get_example_config()
        os.makedirs("configs", exist_ok=True)
        with open("configs/example.json", "w") as f:
            json.dump(example, f, indent=2)
        print("Created configs/example.json")
        return

    if args.test_trojan:
        t = TrojanTunnel(args.test_trojan)
        t.connect()
        return
    if args.test_vless:
        t = VlessTunnel(args.test_vless)
        t.connect()
        return

    if args.trojan:
        t = TrojanTunnel(args.trojan)
        t.connect()
        return

    if args.vless:
        t = VlessTunnel(args.vless)
        t.connect()
        return

    if args.gui:
        try:
            from gui.main import main as gui_main
            gui_main()
        except:
            os.system("python3 gui/main.py")
        return

    if args.config and args.start:
        config = load_config(args.config)
        vpn = NetModVPN(config)
        vpn.start()
    elif args.config:
        config = load_config(args.config)
        print(json.dumps(config, indent=2))
    else:
        parser.print_help()
        print("\nExamples:")
        print("  netmod --config configs/example.json --start")
        print("  netmod --trojan 'trojan://...' --start")
        print("  netmod --vless 'vless://...' --start")
        print("  netmod --test-trojan 'trojan://...'")
        print("  netmod --test-vless 'vless://...'")
        print("  netmod --gui")

if __name__ == "__main__":
    main()
