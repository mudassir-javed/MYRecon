import socket
import validators
import requests
from urllib.parse import urlparse
import sys


def is_ip(inp):
    if validators.ipv4(inp) or validators.ipv6(inp):
        return True
    else:
        return False


def get_domain(url):
    try:
        a = urlparse(url)
        if a.netloc:
            return True, a.netloc
        else:
            return True, a.path
    except:
        return False, None


def get_hostname(ip):
    if is_ip(ip):
        try:
            host_name = socket.gethostbyaddr(ip)
            return True, host_name[0]
        except:
            return False, None
    else:
        return False, None


def is_live(domain):
    try:
        code = requests.get("https://" + domain, timeout=7)
        if code.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False


def validation(inp):
    if is_ip(inp):
        print(f"IP ADDRESS : {inp}")
    b, c = get_domain(inp)
    if b:
        print(f"DOMAIN : {c}")
    if is_live(inp):
        print(f"STATUS : Running")
    else:
        print(f"STATUS : Not Running")
    d, e = get_hostname(inp)
    if d:
        print(f"HOSTNAME : {e}")


input = sys.argv[1]
validation(input)
