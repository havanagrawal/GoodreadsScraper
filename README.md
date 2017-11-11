# GoodreadsScraper

A small Python project to pull data from Goodreads using Scrapy

## What is it?

This is a small Python + Scrapy based web scraper that pulls certain features about books from Goodreads. This can be used for collecting a large data set in a short period of time, for a pet data analysis/visualization project.

## How To Run

Simply run the `run_scraper.sh` with 4 command line arguments; the list name (from Listopia on Goodreads), the start page, the end page, and the prefix with which you want the JSON file to be stored. 

For instance:

`./run_scraper.sh "1.Best_Books_Ever" 1 50 best_books`

will crawl the first 50 pages of [this list](https://www.goodreads.com/list/show/1.Best_Books_Ever), which is approximately around 5k books, and generate a file called `best_books_01_50.json`. 

The paging approach avoids hitting the Goodreads site too heavily. You should also ideally set the `DOWNLOAD_DELAY` to at least 1.

## How to Contribute (if you really want to)

Fixes and improvements are more than welcome, so send a PR! 
