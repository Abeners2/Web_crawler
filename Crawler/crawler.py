# web_crawler/crawler/crawler.py
import requests
from bs4 import BeautifulSoup

def fetch_page(url, headers=None):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f'Failed to retrieve the web page. Status code: {response.status_code}')
        return None

def crawl_website(url, headers=None):
    page_content = fetch_page(url, headers)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup
    return None
