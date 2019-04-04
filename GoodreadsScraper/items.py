# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader

from scrapy.loader.processors import Identity, Compose, MapCompose, TakeFirst

from dateutil.parser import parse as dateutil_parse

def num_page_extractor(num_pages):
    if num_pages:
        return num_pages.split()[0]
    return None


def safe_parse(date):
    try:
        date = dateutil_parse(date, fuzzy=True)
    except ValueError:
        date = None

    return date


def extract_dates(maybe_dates):
    maybe_dates = [s for s in maybe_dates if "published" in s.lower()]
    return [safe_parse(date) for date in maybe_dates]


def extract_year(s):
    s = s.lower().strip()
    match = re.match(".*first published.*(\d{4})", s)
    if match:
        return match.group(1)


def extract_ratings(txt):
    """Extract the rating histogram from embedded Javascript code

        The embedded code looks like this:

        |----------------------------------------------------------|
        | renderRatingGraph([6, 3, 2, 2, 1]);                      |
        | if ($('rating_details')) {                               |
        |   $('rating_details').insert({top: $('rating_graph')})   |
        |  }                                                       |
        |----------------------------------------------------------|
    """
    codelines = "".join(txt).split(";")
    rating_code = [line.strip() for line in codelines if "renderRatingGraph" in line]
    if not rating_code:
        return None
    rating_code = rating_code[0]
    rating_array = rating_code[rating_code.index("[") + 1 : rating_code.index("]")]
    ratings = {5 - i:int(x) for i, x in enumerate(rating_array.split(","))}
    return ratings


class BookItem(scrapy.Item):
    # Scalars
    url = Field()

    title = Field(input_processor=MapCompose(str.strip))
    author = Field(input_processor=MapCompose(str.strip))

    num_ratings = Field(input_processor=MapCompose(str.strip, int))
    num_reviews = Field(input_processor=MapCompose(str.strip, int))
    avg_rating = Field(input_processor=MapCompose(str.strip, float))
    num_pages = Field(input_processor=MapCompose(str.strip, num_page_extractor, int))

    language = Field(input_processor=MapCompose(str.strip))
    publish_date = Field(input_processor=extract_dates)

    original_publish_year = Field(input_processor=MapCompose(extract_year, int))

    isbn = Field()
    asin = Field()
    series = Field()

    # Lists
    awards = Field(output_processor=Identity())
    places = Field(output_processor=Identity())
    characters = Field(output_processor=Identity())
    genres = Field(output_processor=Compose(set, list))

    # Dicts
    rating_histogram = Field(input_processor=MapCompose(extract_ratings))


class BookLoader(ItemLoader):
    default_output_processor = TakeFirst()
