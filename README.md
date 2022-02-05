<h1 align="center">GoodreadsScraper</h1>

<div align="center">

![Python version](https://img.shields.io/badge/python-3.4+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h5>A full-fledged web crawler for Goodreads</h5>
</div>

A small Python project to pull data from Goodreads using Scrapy and Selenium

## Table of Contents

1. [Introduction](#introduction)
1. [Installation](#installation)
1. [How To Run](#how-to-run)
    1. [Author Crawls](#author-crawls)
    1. [List Crawls](#list-crawls)
1. [Data Schema](#data-schema)
    1. [Book](#book)
    1. [Author](#author)
1. [Note About Temporality](#note-about-temporality)
1. [[Bonus] Project Ideas](#bonus-project-ideas)
1. [Contributing](#contributing)

## Introduction

This is a Python + Scrapy (+ Selenium) based web crawler that fetches book and author data from Goodreads. This can be used for collecting a large data set in a short period of time, for a data analysis/visualization project.

With appropriate controls, the crawler can collect metadata for ~50 books per minute (~3000 per hour). If you want to be more aggressive (at the risk of getting your IP blocked by Goodreads), you can set the `DOWNLOAD_DELAY` to a smaller value in [`settings.py`](./GoodreadsScraper/settings.py#L30), but this is not recommended.

## Installation

For crawling, install [`requirements.txt`](./requirements.txt)
```
# Creates a virtual environment
virtualenv gscraper

# This may vary depending on your shell
. gscraper/bin/activate

pip3 install -r requirements.txt
```

## How To Run

Run `python3 crawl.py --help` for all sub-commands that the CLI offers.

### Author Crawls

Run the following command to crawl all authors on the Goodreads website:

```bash
python3 crawl.py author
```

By default, this will store the result to a file called `author_all.jl`

Use `python3 crawl.py author --help` for all options and defaults.

### List Crawls

Run the following command to crawl all books from the first 50 pages of a Listopia list (say 1.Best_Books_Ever). This will

```bash
python3 crawl.py list \
  --list_name="1.Best_Books_Ever" \
  --start_page=1 \
  --end_page=50 \
  --output_file_suffix="best_001_050"
```

This will
1. crawl the first 50 pages of [this list](https://www.goodreads.com/list/show/1.Best_Books_Ever), which is approximately around 5k books, and
1. Store all the books in a file called `book_best_001_050.jl`, and all authors in a file called `author_best_001_050.jl`.

The paging approach avoids hitting the Goodreads site too heavily. You should also ideally set the `DOWNLOAD_DELAY` to at least 1.

Use `python3 crawl.py list --help` for all options and defaults.

### Cleaning and Aggregating

Note that since the output files are in jsonlines (.jl) format, you can simply cat them together into a single jl file...

```bash
cat book_*.jl > all_books.jl
cat author_*.jl > all_authors.jl
```

and load them in for analysis using pandas (not included in requirements.txt):

```python
import pandas as pd

all_books = pd.read_json('all_books.jl', lines=True)
all_authors = pd.read_json('all_authors.jl', lines=True)
```

Alternatively, you can use the `cleanup.py` file, which can be used as both a utility and a script.

As a utility, it provides multiple functions that can be used to transform the data into a format that might be more amenable to analysis or visualization.

As a script, it cleans up some of the multivalued attributes, deduplicates rows, and writes it out to the specified CSV file.

```bash
python3 cleanup.py \
  --filenames best_books_01_50.jl young_adult_01_50.jl \
  --output goodreads.csv
```

### Extracting Kindle Price

A useful feature is the Kindle price of the book on Amazon. Since this data is populated dynamically on the page, Scrapy is unable to extract it. We now use Selenium to get the Amazon product ID as well as the Kindle price:

```bash
# Install selenium, not included in requirements.txt
pip3 install selenium

# Run the Kindle price populator script
python3 populate_kindle_price.py -f goodreads.csv -o goodreads_with_kindle_price.csv
```

The reason we don't use Selenium for extracting the initial information is because Selenium is slow, since it loads up a browser and works through that. This is only an additional step to make the data slightly richer, but is completely optional.

Now the data are ready to be analyzed, visualized and basically anything else you care to do with it!

## Data Schema

### Book

| Column  | Description |
|---------|-------------|
| url     | The Goodreads URL |
| title   | The title |
| author  | The author \* \*\* |
| asin | The [Amazon Standard Identifier Number](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number) for this edition |
| isbn | The [International Standard Book Number](https://en.wikipedia.org/wiki/International_Standard_Book_Number) for this edition |
| num_ratings | The number of user ratings |
| num_reviews | The number of user reviews |
| avg_rating | The average rating (1 - 5) |
| num_pages | The total number of pages |
| language | The language for this edition |
| publish_date | The publish date for this edition |
| original_publish_year | The original year of publication for this novel |
| series | The series of which this novel is a part |
| genres | A list of genres/shelves |
| awards | A list of awards (if any) won by this novel |
| characters | An (incomplete) list of characters that occur in this novel |
| places | A list of places (locations) that occur in this novel |
| rating_histogram | A dictionary that has individual rating counts (5, 4, 3, 2, 1) |

\* Goodreads [distinguishes between authors of the same name](https://www.goodreads.com/help/show/20-separating-authors-with-the-same-name) by introducing additional spaces between their names, so this column should be treated with special consideration during cleaning.
\*\* While there may be multiple authors for a novel, the scraper only records the first one.

### Author

| Column  | Description |
|---------|-------------|
| url     | The Goodreads URL |
| name    | Name of the author |
| birth_date | The author's birth date |
| death_date | The author's death date \* |
| genres | A list of genres this author writes about |
| influences | A list of authors who influenced this author |
| avg_rating | The average rating of all books by this author |
| num_reviews | The total number of reviews for all books by this author |
| num_ratings | The total number of ratings for all books by this author |
| about | A short blurb about this author \*\* |

\* In some cases the death date appears to be earlier than the birth date. This is most likely because the dates are BC, and should be inspected to validate this.
\*\* This blurb is most likely incomplete because it is shortened, and the complete version is available only through a Javascript function (which Scrapy is incapable of executing). If this is a desired field, then the URL can be used in conjunction with a library like selenium to extract the entire blurb.

## Note About Temporality

Since Goodreads is a dynamic platform, with thousands of users constantly adding/deleting/updating reviews and ratings, the data collected through this scraper are valid at a particular timestamp only. Care must be taken while aggregating and deduplicating these data; in most cases one would want to retain the most recently scraped data, but this may change from a case-to-case basis.

## [Bonus] Project Ideas

What can you do with these data? Well, here are a few ideas:

1. Each author has a set of other authors who influenced them, which can be naturally modeled as a **directed graph**. This graph can then either be visualized, OR one could perform graph analysis (community detection, central figures, determining oldest ancestor influencers, etc)
2. One could perform **hypothesis testing** to confirm/reject if:
    1. Female authors have the same number of ratings/reviews as male authors
    1. Fantasy novels have a higher average rating than non-fiction novels
3. As mentioned [here](#note-about-temporality), Goodreads is a dynamic platform, and thus if one chooses to collect these data periodically, one could generate **time-series data**, and observe trends for a particular novel/author over time. One could also perform event detection to determine if the author made a breakthrough in their writing career.


## Contributing

Fixes and improvements are more than welcome, so raise an issue or send a PR!
