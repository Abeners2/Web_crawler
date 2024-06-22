# web_crawler/tests/test_parser.py
import unittest
from bs4 import BeautifulSoup
from crawler.parser import extract_titles

class TestParser(unittest.TestCase):
    def test_extract_titles(self):
        html_doc = "<html><body><h2>Title 1</h2><h2>Title 2</h2></body></html>"
        soup = BeautifulSoup(html_doc, 'html.parser')
        titles = extract_titles(soup)
        self.assertEqual(titles, ['Title 1', 'Title 2'])

if __name__ == '__main__':
    unittest.main()
