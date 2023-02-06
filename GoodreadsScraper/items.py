# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import json
import datetime
from typing import Any, Dict

import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader

from itemloaders.processors import Identity, Compose, MapCompose, TakeFirst, Join

from dateutil.parser import parse as dateutil_parse
from w3lib.html import remove_tags


def print_schema(d, tabs=1):
    if type(d) != dict:
        return
    for key in d.keys():
        print('\t'*tabs + key)
        print_schema(d[key], tabs+1)


def visit_path(data: Dict[str, Any], key: str, original_key: str):
    """If the generator returned by this function yields None, then no more data is left"""

    # print(f"Processing {key} for {data.keys() if type(data) == dict else data}")

    if not data:
        # print for debugging
        if key:
            print(f'No data found for key {original_key} in data')
            print(data)
        return None

    # if no key is left, then yield the data at this point
    if not key:
        yield data
        # stop the generator since there is no more key left to parse
        return None

    if '.' in key:
        idx = key.index('.')
        subkey, remaining_key = key[:idx], key[idx + 1:]
    else:
        subkey, remaining_key = key, None

    # handle partial matches on the key
    # this is needed when the key can be dynamic
    if subkey.endswith('*'):
        # remove '*'
        subkey_prefix = subkey[:-1]

        # find all keys which match subkey_prefix
        matching_subkeys = [k for k in data.keys() if k.startswith(subkey_prefix)]

        # print for debugging
        if len(matching_subkeys) > 1:
            print("Found more than one key matching pattern '{key}'.")

        for sk in matching_subkeys:
            yield from visit_path(data[sk], remaining_key, original_key)

    elif subkey.endswith('[]'):
        # TODO(havan): Handle arrays

        # remove '[]'
        subkey = subkey[:-2]

        values = data.get(subkey, [])

        for value in values:
            yield from visit_path(value, remaining_key, original_key)
    # handle regular keys
    else:
        yield from visit_path(data.get(subkey, None), remaining_key, original_key)



def json_field_extractor_v2(key: str):
    def extract_field(text: str):
        data = json.loads(text)
        return list(visit_path(data, key, key))
    return extract_field


def json_field_extractor(key: str):
    def extract_field(text: str):
        data = json.loads(text)
        value = data
        for subkey in key.split("."):
            # handle partial matches on the key
            # this is needed when the key is dynamic
            if subkey.endswith('*'):
                subkey_prefix = subkey[:-1]
                sk = [k for k in value.keys() if k.startswith(subkey_prefix)]
                if len(sk) > 1:
                    print("Found more than one key matching pattern '{key}'. Arbitrarily returning the first matched value.")
                subkey = sk[0]
            value = value.get(subkey, None)
            if not value:
                return None
        return value
    return extract_field


def splitter(split_on=','):
    return lambda s: s.split(split_on)


def safe_parse_date(date):
    try:
        date = dateutil_parse(date, fuzzy=True, default=datetime.datetime.min)
        date = date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        date = None

    return date


def extract_publish_dates(maybe_dates):
    maybe_dates = [s for s in maybe_dates if "published" in s.lower()]
    return [safe_parse_date(date) for date in maybe_dates]


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
    rating_code = [
        line.strip() for line in codelines if "renderRatingGraph" in line
    ]
    if not rating_code:
        return None
    rating_code = rating_code[0]
    rating_array = rating_code[rating_code.index("[") +
                               1:rating_code.index("]")]
    ratings = {5 - i: int(x) for i, x in enumerate(rating_array.split(","))}
    return ratings


def filter_asin(asin):
    if asin and len(str(asin)) == 10:
        return asin
    return None


def isbn_filter(isbn):
    if isbn and len(str(isbn)) == 10 and isbn.isdigit():
        return isbn


def isbn13_filter(isbn):
    if isbn and len(str(isbn)) == 13 and isbn.isdigit():
        return isbn


def filter_empty(vals):
    return [v.strip() for v in vals if v.strip()]


def split_by_newline(txt):
    return txt.split("\n")


class BookItem(scrapy.Item):
    # Scalars
    url = Field()

    # title = Field(input_processor=MapCompose(str.strip))
    title = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.title')))
    title_complete = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.titleComplete')))
    description = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.description')))
    image_url = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.imageUrl')))
    genres = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.bookGenres[].genre.name')), output_processor=Compose(set, list))
    asin = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.details.asin')))
    isbn = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.details.isbn')))
    isbn13 = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.details.isbn13')))
    publisher = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.details.publisher')))
    series = Field(input_processor=MapCompose(json_field_extractor_v2('props.pageProps.apolloState.Book*.details.bookSeries')))

    author = Field(input_processor=MapCompose(str.strip))

    num_ratings = Field(input_processor=MapCompose(json_field_extractor_v2('aggregateRating.ratingCount')))
    num_reviews = Field(input_processor=MapCompose(json_field_extractor_v2('aggregateRating.reviewCount')))
    avg_rating = Field(input_processor=MapCompose(json_field_extractor_v2('aggregateRating.ratingValue')))
    num_pages = Field(input_processor=MapCompose(json_field_extractor_v2('numberOfPages')))
    language = Field(input_processor=MapCompose(json_field_extractor_v2('inLanguage')))
    book_format = Field(input_processor=MapCompose(json_field_extractor_v2('bookFormat')))
    publish_date = Field(input_processor=extract_publish_dates)

    original_publish_year = Field(
        input_processor=MapCompose(extract_year, int))

    # isbn = Field(input_processor=MapCompose(str.strip, json_field_extractor('isbn'), isbn_filter))
    # isbn13 = Field(input_processor=MapCompose(str.strip, json_field_extractor('isbn'), isbn13_filter))

    # series = Field()

    # Lists
    awards = Field(input_processor=MapCompose(json_field_extractor('awards'), splitter(',')), output_processor=Identity())
    places = Field(output_processor=Identity())
    characters = Field(output_processor=Identity())

    # Dicts
    rating_histogram = Field(input_processor=MapCompose(extract_ratings))


class BookLoader(ItemLoader):
    default_output_processor = TakeFirst()


class AuthorItem(scrapy.Item):
    # Scalars
    url = Field()

    name = Field()
    birth_date = Field(input_processor=MapCompose(safe_parse_date))
    death_date = Field(input_processor=MapCompose(safe_parse_date))

    avg_rating = Field(serializer=float)
    num_ratings = Field(serializer=int)
    num_reviews = Field(serializer=int)

    # Lists
    genres = Field(output_processor=Compose(set, list))
    influences = Field(output_processor=Compose(set, list))

    # Blobs
    about = Field(
        # Take the first match, remove HTML tags, convert to list of lines, remove empty lines, remove the "edit data" prefix
        input_processor=Compose(TakeFirst(), remove_tags, split_by_newline,
                                filter_empty, lambda s: s[1:]),
        output_processor=Join())


class AuthorLoader(ItemLoader):
    default_output_processor = TakeFirst()
