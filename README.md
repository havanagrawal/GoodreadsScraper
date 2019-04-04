# GoodreadsScraper

A small Python project to pull data from Goodreads using Scrapy and Selenium

## Table of Contents

1. [Introduction](#introduction)
1. [Installation](#installation)
1. [How To Run](#how-to-run)
    1. [Author Crawls](#author-crawls)
    1. [List Crawls](#list-crawls)
1. [Contributing](#contributing)

## Introduction

This is a Python + Scrapy (+ Selenium) based web crawler that fetches book and author data from Goodreads. This can be used for collecting a large data set in a short period of time, for a data analysis/visualization project.

With appropriate controls, the crawler can collect metadata for ~50 books per minute (~3000 per hour). If you want to be more aggressive (at the risk of getting your IP blocked by Goodreads), you can set the `DOWNLOAD_DELAY` to a smaller value in [`settings.py`](./GoodreadsScraper/settings.py#L30), but this is not recommended.

## Installation

For crawling, you need to install scrapy, w3lib and python-dateutil:
```
virtualenv gscraper
. gscraper/bin/activate
pip3 install scrapy w3lib python-dateutil
```

For the optional data aggregation step, you will need pandas:
```
pip3 install pandas
```

## How To Run

### Author Crawls

Run the following command to crawl all authors on the Goodreads website:

```bash
scrapy crawl \
  --loglevel=INFO \
  --logfile=scrapy.log \
  --output=authors.json \
  -a author_crawl=true \
  author
```

### List Crawls

Run the following command to crawl all books from the first 25 pages of a Listopia list (say 1.Best_Books_Ever):

```bash
scrapy crawl \
  --logfile=scrapy.log \
  --output books.json \
  -a start_page_no=1 \
  -a end_page_no=25 \
  -a list_name="1.Best_Books_Ever" \
  list
```

Alternatively, run the `run_scraper.sh` with 4 command line arguments; the list name, the start page, the end page, and the prefix with which you want the JSON file to be stored.

For instance:

`./run_scraper.sh "1.Best_Books_Ever" 1 50 best_books`

will crawl the first 50 pages of [this list](https://www.goodreads.com/list/show/1.Best_Books_Ever), which is approximately around 5k books, and generate a file called `best_books_01_50.json`.

The paging approach avoids hitting the Goodreads site too heavily. You should also ideally set the `DOWNLOAD_DELAY` to at least 1.

### Cleaning and Aggregating

Once you've collected all the JSON files you need, you can aggregate them using the `aggregate_json.py` file.

`python3 aggregate_json.py -f best_books_01_50.json young_adult_01_50.json -o goodreads.csv`

This cleans out some of the multivalued attributes, deduplicates rows, and writes it out to the specified CSV file.

### Extracting Kindle Price

A useful feature is the Kindle price of the book on Amazon. Since this data is populated dynamically on the page, Scrapy is unable to extract it. We now use Selenium to get the Amazon product ID as well as the Kindle price:

`python populate_kindle_price.py -f goodreads.csv -o goodreads_with_kindle_price.csv`

The reason we don't use Selenium for extracting the initial information is because Selenium is slow, since it loads up a browser and works through that. This is only an additional step to make the data slightly richer, but is completely optional.

Now the data are ready to be analyzed, visualized and basically anything else you care to do with it!

## Contributing

Fixes and improvements are more than welcome, so raise an issue or send a PR!
