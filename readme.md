# Ruten Seller Product Parser

## Entry Point: main.py
* url = seller's Ruten url
* ProductCrawler:get_crawl_resul to execute the crawl
* results will be returned as json

## Note
* I did not check/set a limit to the number of threads within the process.
* Enhancements can be made with thread pool.
* Wait for 1 seconds per 20 threads
