# Ruten Seller Product Parser
![PyPI version](https://img.shields.io/pypi/pyversions/rutencrawler.svg)
![PyPI license](https://img.shields.io/pypi/l/rutencrawler.svg)



This is a repository that offers a ProductCrawler class to crawl Ruten web pages for the product information in json format.

```
from Crawler import ProductCrawler
seller_ruten_id = "SELLER_RUTEN_ID"
url ="https://class.ruten.com.tw/user/index00.php?s={seller_ruten_id}"
url = url.format(seller_ruten_id)
product_crawler = ProductCrawler(url)
results = product_crawler.get_crawl_result()
```

## Installation
To install [this verson from PyPI](https://pypi.org/project/rutencrawler/), type:
```

pip install rutencrawler

```

To get the newest one from this repo (note that we are in the alpha stage, so there may be frequent updates), type:

```

pip install git+git://github.com/stared/livelossplot.git

```
## Overview

```class ProductCrawler``` class handles the whole web crawling logic.  It takes optional arguments of ```sleep_time``` and ```sleep_at_each_iteration```

```class ProductPageParser``` handles the product page information extraction. Currently the parser only extracts shipping information, urls for images and the title of the product. More info can be extracted and the logic can be added here.

```class ProdcutListParser``` handles the parsing of product list page. The main function is to extract a list of product urls at each page, and then the urls are then used to parse product information with ProductPageParser

## To-do

* add more error-proof exception handlers in ProductCrawler due to the multi-threaded nature of the process.
* add more product info extraction features in ProductCrawler, e.g. price, remaining time, description, etc.
