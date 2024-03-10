import socket
import validators
import requests
from urllib.parse import urlparse
import sys
import click
import whois
from bs4 import BeautifulSoup
from urllib.parse import urljoin


@click.command()
@click.option('-d', '--depth', default=1, help='Maximum depth for crawling.')
def crawl_domain(depth):
    if len(sys.argv) != 2:
        click.echo("Usage: python script.py <domain_url>")
        sys.exit(1)

    url = sys.argv[1]
    visited_urls = set()
    pages_to_visit = [(url, 0)]

    while pages_to_visit:
        current_url, current_depth = pages_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        click.echo("Visiting: {}".format(current_url))
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(current_url, link['href'])
                    if absolute_link.startswith(url) and current_depth < depth:
                        pages_to_visit.append((absolute_link, current_depth + 1))
        except Exception as e:
            click.echo("Error: {}".format(e))

    url = sys.argv[1]
    max_depth = int(sys.argv[2])
    crawl_domain(url, max_depth)


def get_info(domain):
    try:
        info = whois.re
        return info
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


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


input = "facebook.com"
domain_url = input
crawl_domain("https://" + domain_url)
