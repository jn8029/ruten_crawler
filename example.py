from rutencrawler import ProductCrawler

if __name__ == "__main__":

    product_crawler = ProductCrawler(seller_id = "hambergurs")
    results = product_crawler.get_crawl_result()
    with open("result.json","w",encoding='utf-8') as f:
        f.write(str(results))
