import validators
import requests
import click
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def is_ip(inp):
    return validators.ip_address.ipv4(inp) or validators.ip_address.ipv6(inp)


def get_domain(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc:
            return True, parsed_url.netloc
        elif parsed_url.path:
            return True, parsed_url.path
    except:
        return False, None


def is_live(domain):
    try:
        code = requests.get("https://" + domain, timeout=7)
        return code.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


@click.command()
@click.option('-d', '--depth', default=1, help='Maximum depth for crawling.')
@click.argument('url')
def crawl_domain(url, depth):
    visited_urls = set()
    pages_to_visit = [(url, 0)]

    while pages_to_visit:
        current_url, current_depth = pages_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        print("Visiting:", current_url)
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
            print("Error:", e)


def validation(url):
    ip = url
    if is_ip(url):
        print(f"IP ADDRESS : {url}")
        ip = url
    else:
        is_domain, domain = get_domain(url)
        if is_domain:
            print(f"DOMAIN : {domain}")
            if is_live(domain):
                print(f"STATUS : Running")
            else:
                print(f"STATUS : Not Running")


if __name__ == "__main__":
    crawl_domain()
    validation()
