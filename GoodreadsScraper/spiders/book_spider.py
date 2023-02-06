"""Spider to extract information from a /book/show type page on Goodreads"""

import scrapy

from .author_spider import AuthorSpider
from ..items import BookItem, BookLoader

class BookSpider(scrapy.Spider):
    """Extract information from a /book/show type page on Goodreads

        Technically, this is not a Spider in the sense that
        it is never initialized by scrapy. Consequently,
         - its from_crawler method is never invoked
         - its `crawler` attribute is not set
         - it does not have a list of start_urls or start_requests
         - running this spider with scrapy crawl will do nothing
    """
    name = "book"

    def __init__(self):
        super().__init__()
        self.author_spider = AuthorSpider()

    def parse(self, response, loader=None):
        if not loader:
            loader = BookLoader(BookItem(), response=response)

        loader.add_value('url', response.request.url)

        # The new Goodreads page sends JSON in a script tag
        # that has these values

        loader.add_css('title', 'script#__NEXT_DATA__::text')
        loader.add_css('titleComplete', 'script#__NEXT_DATA__::text')
        loader.add_css('description', 'script#__NEXT_DATA__::text')
        loader.add_css('imageUrl', 'script#__NEXT_DATA__::text')
        loader.add_css('genres', 'script#__NEXT_DATA__::text')
        loader.add_css('asin', 'script#__NEXT_DATA__::text')
        loader.add_css('isbn', 'script#__NEXT_DATA__::text')
        loader.add_css('isbn13', 'script#__NEXT_DATA__::text')
        loader.add_css('publisher', 'script#__NEXT_DATA__::text')
        loader.add_css('series', 'script#__NEXT_DATA__::text')
        loader.add_css('author', 'script#__NEXT_DATA__::text')
        loader.add_css('publishDate', 'script#__NEXT_DATA__::text')

        loader.add_css('characters', 'script#__NEXT_DATA__::text')
        loader.add_css('places', 'script#__NEXT_DATA__::text')
        loader.add_css('ratingHistogram', 'script#__NEXT_DATA__::text')
        loader.add_css("ratingsCount", 'script#__NEXT_DATA__::text')
        loader.add_css("reviewsCount", 'script#__NEXT_DATA__::text')
        loader.add_css('numPages', 'script#__NEXT_DATA__::text')
        loader.add_css("format", 'script#__NEXT_DATA__::text')

        loader.add_css('language', 'script#__NEXT_DATA__::text')
        loader.add_css("awards", 'script#__NEXT_DATA__::text')

        yield loader.load_item()

        author_url = response.css('a.ContributorLink::attr(href)').extract_first()
        yield response.follow(author_url, callback=self.author_spider.parse)
