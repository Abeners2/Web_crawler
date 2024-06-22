# run_crawler.py

import sys
import requests
from bs4 import BeautifulSoup

def crawl_website(url):
    try:
        # Faz a requisição GET para a URL
        response = requests.get(url)
        response.raise_for_status()  # Verifica por erros na requisição

        # Cria o objeto BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontra todos os links na página
        links = [link.get('href') for link in soup.find_all('a', href=True)]

        # Encontra todas as imagens na página
        images = [image.get('src') for image in soup.find_all('img', src=True)]

        # Encontra informações sobre tecnologias principais
        technology_info = find_technology_info(soup)

        return soup, links, images, technology_info

    except requests.exceptions.RequestException as e:
        print(f"Failed to crawl {url}: {e}")
        return None, [], [], {}

def find_technology_info(soup):
    # Implemente a lógica para buscar informações específicas como versões de PHP, WordPress, etc.
    # Exemplo simples para encontrar versão de PHP
    php_version = soup.find(string=lambda text: 'PHP Version' in str(text))
    if php_version:
        return {'PHP': php_version.strip()}  # Retorna um dicionário com a informação encontrada
    else:
        return {}

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site HTTPS que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py https://www.example.com")
        return

    url = sys.argv[1]

    # Chama a função crawl_website para buscar informações na página
    soup, links, images, technology_info = crawl_website(url)

    if soup:
        # Mostra informações para o usuário
        print(f"Title of the page: {soup.title.string}")
        print("Links found:")
        for link in links:
            print(link)
        print("\nImages found:")
        for image in images:
            print(image)
        print("\nTechnology information:")
        for key, value in technology_info.items():
            print(f"{key}: {value}")

    else:
        print(f"Failed to crawl {url}")

if __name__ == "__main__":
    main()
