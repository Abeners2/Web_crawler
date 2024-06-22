# web_crawler/tests/test_crawler.py
import unittest
from crawler.crawler import fetch_page

class TestCrawler(unittest.TestCase):
    def test_fetch_page(self):
        url = 'http://exemplo.com'
        page_content = fetch_page(url)
        self.assertIsNotNone(page_content)

if __name__ == '__main__':
    unittest.main()
