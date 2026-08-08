"""
Subscription support - fetch list of Trojan/VLESS/VMess/SS URLs from URL (base64 encoded)
Like free VPN subscription links
"""

import base64
import requests

def fetch_subscription(url):
    """
    Fetch subscription URL which returns base64 encoded list of proxy URLs
    Example: https://example.com/sub.txt contains base64 of:
    trojan://...
    vless://...
    vmess://...
    """
    try:
        print(f"[Sub] Fetching {url}")
        resp = requests.get(url, timeout=10)
        content = resp.text.strip()
        # Try base64 decode
        try:
            # Add padding
            content_b64 = content
            content_b64 += '=' * (-len(content_b64) % 4)
            decoded = base64.b64decode(content_b64).decode()
            print(f"[Sub] Base64 decoded {len(decoded)} chars")
            # Split lines
            urls = [line.strip() for line in decoded.split('\n') if line.strip()]
            print(f"[Sub] Found {len(urls)} proxy URLs")
            return urls
        except:
            # Not base64, assume plain list
            urls = [line.strip() for line in content.split('\n') if line.strip() and '://' in line]
            print(f"[Sub] Plain list {len(urls)} URLs")
            return urls
    except Exception as e:
        print(f"[Sub] Error: {e}")
        return []

def parse_subscription_file(path):
    with open(path, 'r') as f:
        content = f.read()
    urls = [line.strip() for line in content.split('\n') if line.strip() and '://' in line]
    return urls
