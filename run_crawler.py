import sys
import requests
from bs4 import BeautifulSoup
import re
from colorama import init, Fore, Style

# Inicializa o colorama para suporte a cores no terminal do Windows
init()

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

def extract_links(soup):
    links = []
    hidden_links = []

    # Procurar por links visíveis
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    # Procurar por links em elementos ocultos
    hidden_elements = soup.find_all(lambda tag: tag.has_attr('style') and ('display: none;' in tag['style'] or 'visibility: hidden;' in tag['style']))

    for element in hidden_elements:
        # Extrair links ocultos
        for link in element.find_all('a', href=True):
            hidden_links.append(link['href'])

    return links, hidden_links

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
    links, hidden_links = extract_links(soup)
    images = extract_images(soup)
    technologies_from_files = extract_technologies_from_files(url)
    technologies_from_content = extract_technologies(soup)

    # Combinação de todas as tecnologias encontradas
    technologies = list(set(technologies_from_files + technologies_from_content))

    # Busca por páginas de login
    login_pages = find_login_pages(links + hidden_links)

    # Busca por referências a bancos de dados
    database_references = find_database_references(page_content.decode('utf-8', errors='ignore'))

    # Exibindo os resultados
    print(f"Title of the page: {soup.title.string}")
    print("\nLinks found:")
    for link in links:
        print(f"{Fore.BLUE}{link}{Style.RESET_ALL}")  # Adiciona cor ao link

    if hidden_links:
        print("\nHidden links found:")
        for link in hidden_links:
            print(f"{Fore.BLUE}{link}{Style.RESET_ALL}")  # Adiciona cor ao link

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
            print(f"{Fore.BLUE}{page}{Style.RESET_ALL}")  # Adiciona cor ao link

    if database_references:
        print("\nDatabase references found:")
        for db in database_references:
            print(db)

if __name__ == "__main__":
    main()
