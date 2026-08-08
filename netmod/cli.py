import argparse
import json
import os
from .config import load_config, list_configs, get_example_config
from .vpn import NetModVPN
from .trojan_tunnel import TrojanTunnel

def main():
    parser = argparse.ArgumentParser(description="Zorin NetMod VPN - NetMod-like VPN for Linux with Trojan support")
    parser.add_argument('--config', '-c', help='Config file path (JSON)')
    parser.add_argument('--trojan', help='Trojan URL trojan://... support NetMod like Trojan')
    parser.add_argument('--start', action='store_true', help='Start VPN')
    parser.add_argument('--gui', action='store_true', help='Open GUI')
    parser.add_argument('--list-configs', action='store_true', help='List configs')
    parser.add_argument('--create-example', action='store_true', help='Create example config')
    parser.add_argument('--test-trojan', help='Test Trojan URL connectivity')
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

    if args.test_trojan or args.trojan:
        url = args.test_trojan or args.trojan
        print(f"Testing Trojan: {url[:50]}...")
        tun = TrojanTunnel(url)
        tun.connect()
        return

    if args.gui:
        try:
            from gui.main import main as gui_main
            gui_main()
        except ImportError:
            try:
                import gui.main
            except:
                print("GUI not found, trying python3 gui/main.py")
                os.system("python3 gui/main.py")
        return

    if args.config and args.start:
        config = load_config(args.config)
        vpn = NetModVPN(config)
        vpn.start()
    elif args.trojan and args.start:
        tun = TrojanTunnel(args.trojan)
        tun.connect()
    elif args.config:
        config = load_config(args.config)
        print(json.dumps(config, indent=2))
    else:
        parser.print_help()
        print("\nExamples:")
        print("  netmod --config configs/example.json --start")
        print("  netmod --trojan 'trojan://password@host:443?security=tls&sni=aka.ms#name' --start")
        print("  netmod --test-trojan 'trojan://...'")
        print("  netmod --gui")

if __name__ == "__main__":
    main()
