"""
Speed test for proxies - test latency
"""

import socket
import time

def test_latency(host, port, timeout=5):
    start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        latency = (time.time() - start) * 1000
        return latency
    except:
        return 9999

def speedtest_proxies(proxies):
    """
    proxies: list of dict with host, port, name, url
    Returns sorted by latency
    """
    results = []
    for proxy in proxies:
        host = proxy.get('host')
        port = proxy.get('port', 443)
        name = proxy.get('name', f"{host}:{port}")
        print(f"[Speed] Testing {name} {host}:{port}...")
        latency = test_latency(host, port)
        print(f"[Speed] {name}: {latency:.0f}ms")
        results.append((latency, proxy))
    
    results.sort(key=lambda x: x[0])
    return results
