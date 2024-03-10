import requests
from bs4 import BeautifulSoup
import click
import socket
from urllib.parse import urlparse, urljoin
import validators


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


def get_hostname(ip):
    try:
        host_name = socket.gethostbyaddr(ip)
        return True, host_name[0]
    except:
        return False, None


def is_live(domain):
    try:
        code = requests.get("https://" + domain, timeout=7)
        if code.status_code == 200:
            print(f"STATUS : Running")
    except requests.exceptions.ConnectionError:
        print(f"STATUS : Not Running")


@click.command()
@click.option('-d', '--depth', default=1, help='Maximum depth for crawling.')
@click.argument('url')
def crawl_domain(depth, url):
    visited_urls = set()
    pages_to_visit = [(url, 0)]
    all_links = set()  # Use a set to store unique links

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

                # Extract all hyperlinks from the page
                links = soup.find_all('a', href=True)
                for link in links:
                    absolute_link = urljoin(current_url, link['href'])
                    all_links.add(absolute_link)  # Add link to the set

                # Extract links from text-based HTML tags
                text_tags = soup.find_all(['p', 'div', 'span'])
                for tag in text_tags:
                    links = tag.find_all('a', href=True)
                    for link in links:
                        absolute_link = urljoin(current_url, link['href'])
                        all_links.add(absolute_link)  # Add link to the set

                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(current_url, link['href'])
                    if absolute_link.startswith(url) and current_depth < depth:
                        pages_to_visit.append((absolute_link, current_depth + 1))
        except Exception as e:
            print("Error:", e)

    # Writing the links to a file
    with open('Links.txt', 'w', encoding='utf-8') as f:
        for i, link in enumerate(all_links, 1):
            f.write(f"{i} : {link}  \n")


if __name__ == "__main__":
    crawl_domain()
