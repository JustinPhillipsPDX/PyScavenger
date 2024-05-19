import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style


def input_url():
    url = input(Fore.YELLOW + 'Enter Seed URL: ' + Style.RESET_ALL)
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    return url


def scavenge_urls(soup, url):
    url = url
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        # print(href + '\n')
        if href.startswith('/') and href not in urls:
            combined_url = url + href
            if combined_url not in urls:
                urls.append(combined_url)
        if href.startswith('http') and href not in urls:
            # Check if the URL points to a different page or resource
            if href.startswith('#'):  # Ignore fragment identifiers
                continue
            urls.append(href)

    # print(f'URLs: {urls}')
    return urls


def scavenge(url):
    page = None
    try:
        # print(Fore.MAGENTA + f'Visiting {url}' + Style.RESET_ALL)
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f'Request failed for URL "{url}": {e}')
        return None

    if page is not None:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup


def scavenge_all():
    url = input_url()
    soup = scavenge(url=url)
    urls = scavenge_urls(soup, url=url)

    for url in urls:
        print(Fore.RED + f'Visiting {url}' + Style.RESET_ALL)
        new_soup = scavenge(url=url)
        # Process the new page (e.g., extract data, save to file, etc.) here

    return soup


class Scavenger:
    def __init__(self):
        pass

    def run_scavenger(self):
        soup = scavenge_all()
        print(soup.prettify())


py_scavenger = Scavenger()
py_scavenger.run_scavenger()
