# web_crawler/crawler/parser.py
def extract_titles(soup):
    titles = soup.find_all('h2')
    return [title.get_text() for title in titles]

def save_results(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            f.write("%s\n" % item)
