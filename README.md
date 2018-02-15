# GoodreadsScraper

A small Python project to pull data from Goodreads using Scrapy and Selenium

## What is it?

This is a small Python + Scrapy + Selenium based web scraper that pulls certain features about books from Goodreads. This can be used for collecting a large data set in a short period of time, for a pet data analysis/visualization project.

## How To Run


### Initial Data Collection

Simply run the `run_scraper.sh` with 4 command line arguments; the list name (from Listopia on Goodreads), the start page, the end page, and the prefix with which you want the JSON file to be stored.

For instance:

`./run_scraper.sh "1.Best_Books_Ever" 1 50 best_books`

will crawl the first 50 pages of [this list](https://www.goodreads.com/list/show/1.Best_Books_Ever), which is approximately around 5k books, and generate a file called `best_books_01_50.json`.

The paging approach avoids hitting the Goodreads site too heavily. You should also ideally set the `DOWNLOAD_DELAY` to at least 1.

### Cleaning and Aggregating

Once you've collected all the JSON files you need, you can aggregate them using the `aggregate_json.py` file.

`python aggregate_json.py -f best_books_01_50.json young_adult_01_50.json -o goodreads.csv`

This cleans out some of the multivalued attributes, deduplicates rows, and writes it out to the specified CSV file.

### Extracting Kindle Price

A useful feature is the Kindle price of the book on Amazon. Since this data is populated dynamically on the page, Scrapy is unable to extract it. We now use Selenium to get the Amazon product ID as well as the Kindle price:

`python populate_kindle_price.py -f goodreads.csv -o goodreads_with_kindle_price.csv`

The reason we don't use Selenium for extracting the initial information is because Selenium is slow, since it loads up a browser and works through that. This is only an additional step to make the data slightly richer, but is completely optional.

Now the data are ready to be analyzed, visualized and basically anything else you care to do with it!

## How to Contribute (if you really want to)

Fixes and improvements are more than welcome, so send a PR!
