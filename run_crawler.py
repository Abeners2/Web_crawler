import sys
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin

# Lista global para armazenar URLs visitadas
visited_urls = set()

def fetch_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}. Exception: {str(e)}")
        return None

def extract_links(soup, base_url):
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        links.append(full_url)
    return links

def extract_images(soup):
    images = []
    for img in soup.find_all('img', src=True):
        images.append(img['src'])
    return images

def extract_technologies_from_files(page_url):
    technologies = []

    # Fetch da página web
    page_content = fetch_page(page_url)
    if not page_content:
        return technologies

    soup = BeautifulSoup(page_content, 'html.parser')

    # Busca por JavaScript
    script_tags = soup.find_all('script', src=True)
    for script in script_tags:
        script_url = script['src']
        if script_url:
            if '.js' in script_url:
                technologies.append(script_url)

    # Busca por CSS
    link_tags = soup.find_all('link', rel='stylesheet')
    for link in link_tags:
        css_url = link.get('href')
        if css_url:
            if '.css' in css_url:
                technologies.append(css_url)

    return technologies

def extract_technologies(soup):
    technologies = []

    # WordPress
    if soup.find(string=re.compile(r'WordPress', re.IGNORECASE)):
        technologies.append('WordPress')

    # Joomla
    if soup.find(string=re.compile(r'Joomla', re.IGNORECASE)):
        technologies.append('Joomla')

    # Drupal
    if soup.find(string=re.compile(r'Drupal', re.IGNORECASE)):
        technologies.append('Drupal')

    # MySQL
    if 'mysql' in soup.text.lower():
        technologies.append('MySQL')

    # MongoDB
    if 'mongodb' in soup.text.lower():
        technologies.append('MongoDB')

    # React
    if 'react' in soup.text.lower():
        technologies.append('React')

    # Vue.js
    if 'vue.js' in soup.text.lower() or 'vuejs' in soup.text.lower():
        technologies.append('Vue.js')

    # Angular
    if 'angular' in soup.text.lower():
        technologies.append('Angular')

    # jQuery
    if 'jquery' in soup.text.lower():
        technologies.append('jQuery')

    # Bootstrap
    if 'bootstrap' in soup.text.lower():
        technologies.append('Bootstrap')

    return technologies

def find_login_pages(links):
    login_pages = []
    keywords = ['login', 'signin', 'account', 'admin']

    for link in links:
        for keyword in keywords:
            if keyword in link.lower():
                login_pages.append(link)
                break

    return login_pages

def find_database_references(content):
    databases = []
    keywords = ['mysql', 'mongodb', 'sql server', 'postgresql']

    for keyword in keywords:
        if keyword in content.lower():
            databases.append(keyword)

    return databases

def is_internal_link(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

def main(url, max_depth=2, max_urls=100):
    global visited_urls
    queue = [(url, 0)]  # Fila de URLs para visitar, com a profundidade atual
    processed_urls = 0

    while queue and processed_urls < max_urls:
        url, depth = queue.pop(0)

        if url in visited_urls:
            continue

        # Fetch da página web
        page_content = fetch_page(url)
        if not page_content:
            continue

        visited_urls.add(url)
        processed_urls += 1

        # Parsing da página com BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        # Verificação de título
        if soup.title and soup.title.string:
            print(f"\nTitle of the page: {soup.title.string}")
        else:
            print("\nTitle not found")

        # Extração de links, imagens e tecnologias
        base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
        links = extract_links(soup, base_url)
        images = extract_images(soup)
        technologies_from_files = extract_technologies_from_files(url)
        technologies_from_content = extract_technologies(soup)

        # Combinação de todas as tecnologias encontradas
        technologies = list(set(technologies_from_files + technologies_from_content))

        # Busca por páginas de login
        login_pages = find_login_pages(links)

        # Busca por referências a bancos de dados
        database_references = find_database_references(page_content.decode('utf-8', errors='ignore'))

        # Exibindo os resultados da página atual
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

        # Adicionar links internos à fila, se não ultrapassar a profundidade máxima
        if depth < max_depth:
            for link in links:
                if is_internal_link(link, base_url) and link not in visited_urls:
                    queue.append((link, depth + 1))

    print("\nCrawler finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py http://www.example.com")
    else:
        url = sys.argv[1]
        main(url)
