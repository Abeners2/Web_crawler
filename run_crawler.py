import sys
import re
from urllib.parse import urljoin
from crawler.crawler import crawl_website

def find_extensions(links):
    extensions = {}
    for link in links:
        match_php = re.search(r'\.php', link)
        if match_php:
            extensions['PHP'] = '7.2.7'  # Exemplo de versão fictícia
        match_wordpress = re.search(r'wordpress', link, re.IGNORECASE)
        if match_wordpress:
            extensions['WordPress'] = '5.3.0'  # Exemplo de versão fictícia
    return extensions

def main():
    if len(sys.argv) < 2:
        print("Por favor, forneça a URL do site HTTPS que deseja buscar.")
        print("Exemplo de uso: python run_crawler.py https://www.example.com")
        return

    url = sys.argv[1]
    
    # Chamar a função crawl_website do seu módulo crawler
    soup, links, images = crawl_website(url)
    
    if soup:
        # Processar links
        print(f"Links found ({len(links)}):")
        for link in links:
            print(urljoin(url, link))

        # Processar imagens
        print(f"\nImages found ({len(images)}):")
        for image in images:
            print(urljoin(url, image))

        # Encontrar extensões e suas versões
        extensions = find_extensions(links)
        if extensions:
            print("\nPrincipais extensões e versões encontradas:")
            for ext, version in extensions.items():
                print(f"- {ext}: {version}")
                if ext == 'PHP':
                    print(f"  [Mais informações sobre PHP](https://www.php.net/releases/index.php)")
                elif ext == 'WordPress':
                    print(f"  [Mais informações sobre WordPress](https://wordpress.org/news/category/releases/)")

        # Mostrar título da página
        print(f"\nTitle of the page: {soup.title.string}")
    else:
        print(f"Failed to crawl {url}")

if __name__ == "__main__":
    main()
