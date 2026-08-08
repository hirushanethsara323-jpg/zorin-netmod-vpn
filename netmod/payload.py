"""
NetMod Payload Generator - Bug Host, SNI, Payload keywords
"""

def generate_payload(template, bug_host, ssh_host, ssh_port, method="GET"):
    """
    Generate payload from template with keywords:
    [host], [port], [crlf], [lf], [method], [real_host]
    Example: GET / HTTP/1.1[crlf]Host: [host][crlf]X-Online-Host: [host][crlf][crlf]
    """
    payload = template
    payload = payload.replace("[host]", bug_host)
    payload = payload.replace("[real_host]", ssh_host)
    payload = payload.replace("[port]", str(ssh_port))
    payload = payload.replace("[method]", method)
    payload = payload.replace("[crlf]", "\r\n")
    payload = payload.replace("[lf]", "\n")
    payload = payload.replace("\\r\\n", "\r\n")
    return payload

def get_default_payloads():
    return {
        "direct": "[method] / HTTP/1.1[crlf]Host: [host][crlf][crlf]",
        "x_online": "GET / HTTP/1.1[crlf]Host: [host][crlf]X-Online-Host: [host][crlf]Connection: Keep-Alive[crlf][crlf]",
        "x_forward": "GET http://[host]/ HTTP/1.1[crlf]Host: [host][crlf]X-Forwarded-For: [host][crlf][crlf]",
        "connect": "CONNECT [host]:[port] HTTP/1.1[crlf]Host: [host][crlf][crlf]",
        "ws_upgrade": "GET / HTTP/1.1[crlf]Host: [host][crlf]Upgrade: websocket[crlf]Connection: Upgrade[crlf]Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==[crlf][crlf]"
    }
