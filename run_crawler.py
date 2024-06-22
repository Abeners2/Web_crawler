# run_crawler.py

import sys
from urllib.parse import urljoin
from crawler.crawler import crawl_website

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site HTTPS que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py https://www.example.com")
        return

    url = sys.argv[1]
    
    # Chamar a função crawl_website do seu módulo crawler
    soup = crawl_website(url)
    
    if soup:
        # Extrair e imprimir o título da página
        if soup.title:
            print(f"Title of the page: {soup.title.string.strip()}")

        # Extrair e imprimir os links encontrados na página
        links = soup.find_all('a', href=True)
        print(f"\nLinks found ({len(links)}):")
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)  # Transforma em URL absoluta se necessário
            print(full_url)

        # Extrair e imprimir as imagens encontradas na página
        images = soup.find_all('img', src=True)
        print(f"\nImages found ({len(images)}):")
        for image in images:
            src = image['src']
            full_url = urljoin(url, src)  # Transforma em URL absoluta se necessário
            print(full_url)
    else:
        print(f"Failed to crawl {url}")

if __name__ == "__main__":
    main()
