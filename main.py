from Crawler import ProductCrawler

if __name__ == "__main__":
    url ="https://class.ruten.com.tw/user/index00.php?s=hambergurs"
    product_crawler = ProductCrawler(url)
    results = product_crawler.get_crawl_result(pages=3)
    print(results)
