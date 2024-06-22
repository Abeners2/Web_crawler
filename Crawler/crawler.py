# web_crawler/crawler/crawler.py
import requests
from bs4 import BeautifulSoup

def fetch_page(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança uma exceção para status HTTP diferentes de 200
        return response.content
    except requests.exceptions.RequestException as e:
        print(f'Failed to retrieve the web page: {e}')
        return None

def crawl_website(url, headers=None):
    page_content = fetch_page(url, headers)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup
    return None
