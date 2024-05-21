"""
==================================================================
Name:        PyScavenger
Version:     0.1
Date:        2024-05-20

Repository:  https://github.com/JustinPhillipsPDX/PyScavenger

Author:      Justin Phillips

Description:
PyScavenger is an open-source web crawler written in Python.
==================================================================
"""
# Import necessary libraries
import requests
import time
import random
import concurrent.futures
import json
from bs4 import BeautifulSoup
from colorama import Fore, Style


class Scavenger:
    def __init__(self):
        pass

    def run_scavenger(self):
        # Create an instance of the Scavenger class and run the web scraping process
        soup = scavenge_all()
        print(soup.prettify())


def input_url():
    # Prompt user to enter seed URL and validate it
    url = input(Fore.YELLOW + 'Enter Seed URL: ' + Style.RESET_ALL)

    if not url.startswith('https://'):
        url = f'https://{url}'

    return url


def scavenge_urls(soup, url):
    # Initialize an empty list to store the URLs
    urls = []

    # Iterate over all anchor tags in the HTML content
    for link in soup.find_all('a'):
        href = link.get('href')

        # Check if the URL is a relative URL and not already visited
        if href.startswith('/') and href not in urls:
            # Combine base URL with relative URL
            combined_url = url + href

            # Add the new URL to the list of URLs if it hasn't been visited before
            if combined_url not in urls:
                urls.append(combined_url)

        # Check if the URL is an absolute URL and not already visited
        if href.startswith('http') and href not in urls:
            # Check if the URL points to a different page or resource
            if href.startswith('#'):  # Ignore fragment identifiers

                continue

            # Add the new URL to the list of URLs if it hasn't been visited before
            urls.append(href)

    return urls


def scavenge(url):
    # Initialize BeautifulSoup object with HTML content and parser
    page = None

    try:
        # Send an HTTP request to the provided URL
        page = requests.get(url)

    except requests.exceptions.RequestException as e:
        print(f'Request failed for URL "{url}": {e}')
        return None

    if page is not None:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup


def scavenge_all():
    # Prompt user to enter a seed URL
    url = input_url()

    # Scrape the initial page
    soup = scavenge(url=url)

    # Get all URLs from the initial page and its subpages
    urls = scavenge_urls(soup, url=url)

    # Parallel URL requests, add the ability to scrape multiple URLs
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each URL request to the thread pool for execution
        future_to_url = {executor.submit(scavenge, url): url for url in urls}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            print(Fore.RED + f'Visiting {url}' + Style.RESET_ALL)

            # Rate Limiting, add a random delay between 0.5 and 2 seconds before making the request
            time.sleep(random.uniform(0.5, 2))

            # Scrape each URL and process it (e.g., extract data, save to file, etc.)
            try:
                new_soup = future.result()
                # Process the new page here

            except Exception as exc:
                print(f'Error while scraping {url}: {exc}')

    return soup


def main():
    # Call the run_scavenger method of the Scavenger class
    py_scavenger = Scavenger()
    py_scavenger.run_scavenger()


if __name__ == '__main__':
    main()
