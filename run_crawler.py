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
    keywords = ['login', 'signin', 'account', 'admin', 'administrador', 'pass', 'password']

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

def process_url(url, depth):
    if url in visited_urls:
        return None

    page_content = fetch_page(url)
    if not page_content:
        return None

    visited_urls.add(url)

    soup = BeautifulSoup(page_content, 'html.parser')
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    links = extract_links(soup, base_url)
    images = extract_images(soup)
    technologies_from_files = extract_technologies_from_files(url)
    technologies_from_content = extract_technologies(soup)
    technologies = list(set(technologies_from_files + technologies_from_content))
    login_pages = find_login_pages(links)
    database_references = find_database_references(page_content.decode('utf-8', errors='ignore'))

    result = {
        'url': url,
        'titulo': soup.title.string if soup.title else 'Sem Titulo',
        'links': links,
        'imagens': images,
        'tecnologias': technologies,
        'paginas_de_login': login_pages,
        'referencias_de_banco_de_dados': database_references,
        'profundidade': depth
    }

    return result

def filter_data(data, filters):
    filtered_data = []

    for item in data:
        match = True
        for key, value in filters.items():
            if key in item and value.lower() not in str(item[key]).lower():
                match = False
                break
        if match:
            filtered_data.append(item)

    return filtered_data

def search_data(data, query):
    search_results = []

    for item in data:
        for key, value in item.items():
            if query.lower() in str(value).lower():
                search_results.append(item)
                break

    return search_results

def display_results(data):
    for item in data:
        print(f"\nURL: {item['url']}")
        print(f"Titulo: {item['titulo']}")
        print(f"Links encontrados: {len(item['links'])}")
        for link in item['links']:
            print(link)
        print(f"Imagens encontradas: {len(item['imagens'])}")
        for img in item['imagens']:
            print(img)
        print(f"Tecnologias encontradas: {len(item['tecnologias'])}")
        for tech in item['tecnologias']:
            print(tech)
        print(f"Paginas de Login encontradas: {len(item['paginas_de_login'])}")
        for page in item['paginas_de_login']:
            print(page)
        print(f"Referencias de banco de dados: {len(item['referencias_de_banco_de_dados'])}")
        for db in item['referencias_de_banco_de_dados']:
            print(db)
        print("-" * 80)

def main(url, max_depth=2, max_urls=100):
    global visited_urls
    queue = [(url, 0)]  # Fila de URLs para visitar, com a profundidade atual
    processed_urls = 0
    results = []  # Lista para armazenar os dados extraídos

    with ThreadPoolExecutor(max_workers=10) as executor:
        while queue and processed_urls < max_urls:
            futures = [executor.submit(process_url, u, d) for u, d in queue]
            queue = []
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        queue.extend([(link, result['profundidade'] + 1) for link in result['links'] if is_internal_link(link, url) and result['profundidade'] < max_depth])
                        processed_urls += 1
                except Exception as e:
                    print(f"Erro processando URL: {e}")

    print("\nCrawler Terminou. Dados Coletados.")

    # Exibir resultados da coleta de dados
    display_results(results)

    # Permitir ao usuário realizar filtros e buscas
    while True:
        print("\nOpções:")
        print("1. Filtrar dados")
        print("2. Procurar dados")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            filters = {}
            print("\nInsira os filtros (Deixe vazio para pular):")
            title_filter = input("O titulo contém: ")
            if title_filter:
                filters['titulo'] = title_filter
            url_filter = input("URL contém: ")
            if url_filter:
                filters['url'] = url_filter
            tech_filter = input("Tecnologia contém: ")
            if tech_filter:
                filters['tecnologias'] = tech_filter

            filtered_results = filter_data(results, filters)
            display_results(filtered_results)

        elif choice == '2':
            query = input("\nInsira a consulta de pesquisa: ")
            search_results = search_data(results, query)
            display_results(search_results)

        elif choice == '3':
            break

        else:
            print("Escolha Invalida, Por favor tente novamente.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py http://www.exemplo.com")
    else:
        url = sys.argv[1]
        main(url)
