import requests
from HtmlParser import ProductListParser, ProductPageParser
import threading
import time
class ProductCrawler:
    headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def __init__(self, url):
        self.products = []
        self.url = url
        self.threads = []
        self.product_urls = []

    def _crawl_product_in_thread(self, url):
        success = False
        fail = 0
        while success is False:
            try:
                response = requests.get(url, headers=self.headers)
                success = True
                print("Success to Crawl with fail={}, url={}".format(fail,url.split("?")[-1]))
            except Exception:
                fail += 1
                print("Fail to Crawl with fail={}, url={}".format(fail,url.split("?")[-1]))
                time.sleep(5)
            else:
                product_page_parser = ProductPageParser(response)
                product = product_page_parser.get_product()
                self.products.append(product)

    def _crawl_list_in_thread(self, url):
        response = requests.get(url, headers = self.headers)
        print("Success {}".format(url))
        product_list_parser = ProductListParser(response)
        product_list = product_list_parser.get_product_list()
        self.product_urls += product_list

    def get_product_urls(self):
        max_page = ProductListParser(requests.get(self.url, headers=self.headers)).get_max_page()
        page_number = 1
        while page_number<=max_page:
            url_with_page_num = "{base_url}&p={page_number}".format(base_url = self.url, page_number = page_number)
            print(url_with_page_num)
            thread = threading.Thread(target = self._crawl_list_in_thread, args=(url_with_page_num,))
            thread.start()
            self.threads.append(thread)
            page_number+=1
            if page_number%20 == 0:
                time.sleep(1)
        for thread in self.threads:
            thread.join()
        self.threads = []
        return self.product_urls

    def get_crawl_result(self):
        product_urls = self.get_product_urls()
        for index, product_url in enumerate(product_urls):
            print("crawling{}".format(index))
            thread = threading.Thread(target = self._crawl_product_in_thread,args=(product_url,))
            thread.start()
            self.threads.append(thread)
            if index%20 ==0:
                time.sleep(1)
        for thread in self.threads:
            thread.join()
        return self.products
