import requests
from HtmlParser import ProductListParser, ProductPageParser
import threading
class ProductCrawler:
    headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def __init__(self, url):
        self.products = []
        self.url = url
        self.threads = []
    def _crawl_in_thread(self, url, title):
        response = requests.get(url, headers=self.headers)
        product_page_parser = ProductPageParser(response)
        product = {
                    "title":title,
                    "images":product_page_parser.get_images(),
                    "shipping_fees":product_page_parser.get_shipping_fees()
                    }
        self.products.append(product)

    def get_crawl_result(self, pages):
        page_number = 1
        while page_number<=pages:
            url_with_page_num = "{base_url}&p={page_number}".format(base_url = self.url, page_number = page_number)
            response = requests.get(url_with_page_num, headers = self.headers)
            product_list_parser = ProductListParser(response)
            product_list = product_list_parser.get_product_list()
            if len(product_list)==0:
                print("Parser has reached the end of the page")
                break
            else:
                for title, product_url in product_list.items():
                    thread = threading.Thread(target = self._crawl_in_thread,args=(product_url, title))
                    thread.start()
                    self.threads.append(thread)
                page_number += 1

        for thread in self.threads:
            thread.join()
        return self.products
