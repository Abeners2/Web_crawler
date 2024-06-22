import sys
import requests
from bs4 import BeautifulSoup
import re

def fetch_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Tentar decodificar com diferentes codecs
            codecs_to_try = ['utf-8', 'iso-8859-1', 'ascii', 'cp1252', 'latin1']  # Exemplos de codecs para tentar
            for codec in codecs_to_try:
                try:
                    content = response.content.decode(codec)
                    return content
                except UnicodeDecodeError:
                    continue  # Tenta o próximo codec se der erro
            print(f"Failed to decode content from {url}.")
            return None
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}. Exception: {str(e)}")
        return None

def extract_links(soup):
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

def extract_images(soup):
    images = []
    for img in soup.find_all('img', src=True):
        images.append(img['src'])
    return images

def extract_technologies(soup):
    technologies = []
    
    # Exemplo: Buscando versão do PHP no HTML
    php_version_tag = soup.find(string=re.compile(r'PHP (\d+\.\d+\.\d+)'))
    if php_version_tag:
        technologies.append(f'PHP: {php_version_tag.strip()}')

    # Exemplo: Buscando outras tecnologias
    # Adicione mais padrões conforme necessário
    other_technologies = {
        'WordPress': r'WordPress (\d+\.\d+\.\d+)',
        'Joomla': r'Joomla! (\d+\.\d+\.\d+)',
        'Drupal': r'Drupal (\d+\.\d+\.\d+)',
        'MySQL': r'MySQL (\d+\.\d+\.\d+)',
        'MongoDB': r'MongoDB (\d+\.\d+\.\d+)',
        'PostgreSQL': r'PostgreSQL (\d+\.\d+\.\d+)',
    }

    for tech, pattern in other_technologies.items():
        tag = soup.find(string=re.compile(pattern))
        if tag:
            technologies.append(f'{tech}: {tag.strip()}')

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

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py http://www.example.com")
        return

    url = sys.argv[1]

    # Fetch da página web
    page_content = fetch_page(url)
    if not page_content:
        return

    # Parsing da página com BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # Extração de links, imagens e tecnologias
    links = extract_links(soup)
    images = extract_images(soup)
    technologies = extract_technologies(soup)

    # Busca por páginas de login
    login_pages = find_login_pages(links)

    # Busca por referências a bancos de dados
    database_references = find_database_references(page_content)

    # Exibindo os resultados
    print(f"Title of the page: {soup.title.string}")
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

if __name__ == "__main__":
    main()
