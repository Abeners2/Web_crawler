import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor

# Lista global para armazenar URLs visitadas
visited_urls = set()

def fetch_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP ruins
        return response.content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

def extract_links(soup, base_url):
    try:
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            links.append(full_url)
        return links
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []

def extract_images(soup):
    try:
        images = []
        for img in soup.find_all('img', src=True):
            images.append(img['src'])
        return images
    except Exception as e:
        print(f"Error extracting images: {e}")
        return []

def extract_technologies_from_files(page_url):
    technologies = []
    page_content = fetch_page(page_url)
    if not page_content:
        return technologies

    try:
        soup = BeautifulSoup(page_content, 'html.parser')
        script_tags = soup.find_all('script', src=True)
        for script in script_tags:
            script_url = script['src']
            if script_url and '.js' in script_url:
                technologies.append(script_url)

        link_tags = soup.find_all('link', rel='stylesheet')
        for link in link_tags:
            css_url = link.get('href')
            if css_url and '.css' in css_url:
                technologies.append(css_url)
    except Exception as e:
        print(f"Error extracting technologies from files: {e}")

    return technologies

def extract_technologies(soup):
    technologies = []
    try:
        if soup.find(string=re.compile(r'WordPress', re.IGNORECASE)):
            technologies.append('WordPress')
        if soup.find(string=re.compile(r'Joomla', re.IGNORECASE)):
            technologies.append('Joomla')
        if soup.find(string=re.compile(r'Drupal', re.IGNORECASE)):
            technologies.append('Drupal')
        if 'mysql' in soup.text.lower():
            technologies.append('MySQL')
        if 'mongodb' in soup.text.lower():
            technologies.append('MongoDB')
        if 'react' in soup.text.lower():
            technologies.append('React')
        if 'vue.js' in soup.text.lower() or 'vuejs' in soup.text.lower():
            technologies.append('Vue.js')
        if 'angular' in soup.text.lower():
            technologies.append('Angular')
        if 'jquery' in soup.text.lower():
            technologies.append('jQuery')
        if 'bootstrap' in soup.text.lower():
            technologies.append('Bootstrap')
    except Exception as e:
        print(f"Error extracting technologies: {e}")

    return technologies

def find_login_pages(links):
    try:
        login_pages = []
        keywords = ['login', 'signin', 'account', 'admin']
        for link in links:
            for keyword in keywords:
                if keyword in link.lower():
                    login_pages.append(link)
                    break
        return login_pages
    except Exception as e:
        print(f"Error finding login pages: {e}")
        return []

def find_database_references(content):
    try:
        databases = []
        keywords = ['mysql', 'mongodb', 'sql server', 'postgresql']
        for keyword in keywords:
            if keyword in content.lower():
                databases.append(keyword)
        return databases
    except Exception as e:
        print(f"Error finding database references: {e}")
        return []

def is_internal_link(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

def process_url(url, depth, max_depth, max_urls, processed_urls):
    if url in visited_urls:
        return

    page_content = fetch_page(url)
    if not page_content:
        return

    visited_urls.add(url)
    processed_urls += 1

    try:
        soup = BeautifulSoup(page_content, 'html.parser')
    except Exception as e:
        print(f"Error parsing page {url}: {e}")
        return

    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    links = extract_links(soup, base_url)
    images = extract_images(soup)
    technologies_from_files = extract_technologies_from_files(url)
    technologies_from_content = extract_technologies(soup)
    technologies = list(set(technologies_from_files + technologies_from_content))
    login_pages = find_login_pages(links)
    database_references = find_database_references(page_content.decode('utf-8', errors='ignore'))

    print(f"\nTitle of the page: {soup.title.string if soup.title else 'No title found'}")
    print("\nLinks found:")
    for link in links:
        print(link)

    print("\nImages found:")
    for img in images:
        print(img)

    if technologies:
        print("\nTechnologies found:")
        for tech in technologies:
            print(tech)
    else:
        print("\nNo technology information found.")

    if login_pages:
        print("\nLogin pages found:")
        for page in login_pages:
            print(page)

    if database_references:
        print("\nDatabase references found:")
        for db in database_references:
            print(db)

    if depth < max_depth:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for link in links:
                if is_internal_link(link, base_url) and link not in visited_urls and processed_urls < max_urls:
                    futures.append(executor.submit(process_url, link, depth + 1, max_depth, max_urls, processed_urls))
            for future in futures:
                future.result()

def main(url, max_depth=2, max_urls=100):
    global visited_urls
    visited_urls = set()
    process_url(url, 0, max_depth, max_urls, 0)
    print("\nCrawler finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py http://www.example.com")
    else:
        url = sys.argv[1]
        main(url)
