# web_crawler/crawler/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Falha ao buscar {url}. Código do estado: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Falha ao buscar {url}: {e}")
        return None

def parse_html(content):
    return BeautifulSoup(content, 'html.parser') if content else None

def extract_links(soup, base_url):
    links = []
    if soup:
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                links.append(full_url)
    return links

def extract_images(soup, base_url):
    images = []
    if soup:
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                full_url = urljoin(base_url, src)
                images.append(full_url)
    return images

def crawl_website(url):
    content = fetch_page(url)
    if content:
        soup = parse_html(content)
        if soup:
            base_url = url
            links = extract_links(soup, base_url)
            images = extract_images(soup, base_url)
            return soup, links, images
    return None, [], []
