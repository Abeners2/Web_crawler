# run_crawler.py

import sys
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
        # Aqui você pode adicionar lógica para processar o conteúdo obtido
        # Por exemplo, imprimir o título da página
        print(f"Title of the page: {soup.title.string}")
    else:
        print(f"Failed to crawl {url}")

if __name__ == "__main__":
    main()
