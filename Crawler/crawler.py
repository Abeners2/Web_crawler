# crawler.py

import requests
from bs4 import BeautifulSoup

def fetch_page(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors different from 200
        return response.content
    except requests.exceptions.RequestException as e:
        print(f'Failed to retrieve the web page: {e}')
        return None

def crawl_website(url, headers=None):
    page_content = fetch_page(url, headers)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Extract page title
        page_title = soup.title.string.strip() if soup.title else 'No title found'
        print(f'Title of the page: {page_title}')
        
        # Extract all links
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        print(f'Links found ({len(links)}):')
        for link in links:
            print(link)
        
        # Extract all images
        images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
        print(f'Images found ({len(images)}):')
        for img in images:
            print(img)

        # You can add more extraction logic here for other elements like text, metadata, etc.

        return soup

    return None
