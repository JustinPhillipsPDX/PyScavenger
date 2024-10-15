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
import os
import concurrent.futures
import random
import time

# Import necessary libraries
try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import Fore, Style    
except ModuleNotFoundError:
    os.system("pip install requests==2.31.0")
    os.system("pip install beautifulsoup4==4.12.3")
    os.system("pip install colorama~=0.4.6")

class Scavenger:
    def __init__(self):
        pass

    def run_scavenger(self):
        # Create an instance of the Scavenger class and run the web scraping process
        soup = self.scavenge_all()

    def input_url(self, url):
        # Prompt user to enter seed URL and validate it
        url = input(Fore.YELLOW + 'Enter Seed URL: ' + Style.RESET_ALL)

        if not url.startswith('https://'):
            url = f'https://{url}'

        return url

    def extract_table_data(self, soup, url):

        # Find all table elements without specifying class or ID attribute
        table_elements = soup.find_all('table')
        table_data = []

        for table_element in table_elements:
            # Extract the table rows as a list of lists
            table_rows = []

            for row in table_element.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                table_rows.append(row_data)

            # Print the extracted data from each table
            print(Fore.LIGHTYELLOW_EX + f'Table data for {url}:\n{table_rows}' + Style.RESET_ALL)

            # Store the extracted data from each table
            table_data.extend(table_rows)

        return {'url': url, 'table_data': table_data, 'soup': soup}

    def scavenge(self, url):
        # Initialize BeautifulSoup object with HTML content and parser
        page = None

        try:
            # Send an HTTP request to the provided URL
            page = requests.get(url)

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f'Request failed for URL "{url}": {e}' + Style.RESET_ALL)
            return None

        if page is not None:
            soup = BeautifulSoup(page.content, 'html.parser')
            return self.extract_table_data(soup, url)

    def scavenge_all(self):
        # Prompt user to enter a seed URL
        url = self.input_url(self)

        # Scrape the initial page
        soup = self.scavenge(url=url)

        # print(soup['soup'])

        # Get all URLs from the initial page and its subpages
        urls = self.scavenge_urls(soup['soup'], url=url)

        # Parallel URL requests, add the ability to scrape multiple URLs
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit each URL request to the thread pool for execution
            future_to_url = {executor.submit(self.scavenge, url): url for url in urls}

            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]

                print(Fore.RED + f'Visiting... {url}' + Style.RESET_ALL)

                # Rate Limiting, add a random delay between 0.5 and 2 seconds before making the request
                time.sleep(random.uniform(0.5, 2))

                # Scrape each URL and process it (e.g., extract data, save to file, etc.)
                try:
                    new_soup = future.result()

                    # Process the new page here
                    self.extract_table_data(new_soup['soup'], url)

                except Exception as exc:
                    print(Fore.RED + f'Error while scraping {url}: {exc}' + Style.RESET_ALL)

        return soup

    def scavenge_urls(self, soup, url):
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


def main():
    # Call the run_scavenger method of the Scavenger class
    py_scavenger = Scavenger()
    py_scavenger.run_scavenger()


if __name__ == '__main__':
    main()
