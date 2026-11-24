import urllib.request
import urllib.error
import ssl
import socket
import time
import re
import sys
from datetime import datetime


def check_ssl_expiry(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry_str = cert['notAfter']
                expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.utcnow()).days
                return True, days_left
    except Exception:
        return False, 0


def audit_website(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    hostname = url.split('//')[-1].split('/')[0]
    start_time = time.time()

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'WebHealthChecker/1.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            status_code = response.getcode()
            html = response.read().decode('utf-8', errors='ignore')

            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Missing <title>"
            has_viewport = bool(re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.IGNORECASE))
            ssl_valid, ssl_days = check_ssl_expiry(hostname) if url.startswith('https://') else (False, 0)

            print(f"\n[OK] {url}")
            print(f"  - HTTP Status : {status_code}")
            print(f"  - Response    : {latency} ms")
            print(f"  - SSL Valid   : {'Yes (' + str(ssl_days) + ' days left)' if ssl_valid else 'No / HTTP'}")
            print(f"  - Page Title  : {title[:60]}")
            print(f"  - Mobile Tag  : {'Found' if has_viewport else 'Missing viewport meta'}")

    except urllib.error.HTTPError as e:
        print(f"\n[HTTP ERROR] {url} -> Status Code: {e.code}")
    except Exception as e:
        print(f"\n[FAILED] {url} -> Reason: {e}")


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["https://example.com", "https://github.com"]
    print("=== Web Health & Code Validator ===")
    for site in targets:
        audit_website(site)
  
