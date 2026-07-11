import ssl
import socket
from urllib.parse import urlparse


def check_ssl(url):
    try:
        domain = urlparse(url).netloc

        if domain.startswith("www."):
            domain = domain[4:]

        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain):
                return True

    except Exception:
        return False


def ssl_risk_score(is_valid):
    if is_valid:
        return 0
    else:
        return 20
    