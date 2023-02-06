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

        # loader.add_css("title", "[data-testid=bookTitle]::text")
        loader.add_css("author", "span.ContributorLink__name[data-testid=name]::text")

        # loader.add_css("num_ratings", "[data-testid=ratingsCount]::text")
        # loader.add_css("num_reviews", "[data-testid=reviewsCount]::text")
        # loader.add_css("avg_rating", "div.RatingStatistics__rating::text")
        # loader.add_css("num_pages", "[data-testid=pagesFormat]::text")

        loader.add_css('publish_date', '[data-testid=publicationInfo]::text')
        loader.add_css('publish_date', 'nobr.greyText::text')

        loader.add_css('original_publish_year', 'nobr.greyText::text')

        # loader.add_css("genres", 'div.left>a.bookPageGenreLink[href*="/genres/"]::text')

        loader.add_css('characters', 'a[href*="/characters/"]::text')
        loader.add_css('places', 'div.infoBoxRowItem>a[href*=places]::text')

        loader.add_css('rating_histogram', 'script[type*="protovis"]::text')

        # The new Goodreads page sends JSON in a script tag
        # that has these values

        loader.add_css('title', 'script#__NEXT_DATA__::text')
        loader.add_css('title_complete', 'script#__NEXT_DATA__::text')
        loader.add_css('description', 'script#__NEXT_DATA__::text')
        loader.add_css('image_url', 'script#__NEXT_DATA__::text')
        loader.add_css('genres', 'script#__NEXT_DATA__::text')
        loader.add_css('asin', 'script#__NEXT_DATA__::text')
        loader.add_css('isbn', 'script#__NEXT_DATA__::text')
        loader.add_css('isbn13', 'script#__NEXT_DATA__::text')
        loader.add_css('publisher', 'script#__NEXT_DATA__::text')
        loader.add_css('series', 'script#__NEXT_DATA__::text')

        loader.add_css('language', 'script[type*="json"]::text')
        # loader.add_css('isbn', 'script[type*="json"]::text')
        # loader.add_css('isbn13', 'script[type*="json"]::text')
        loader.add_css('num_pages', 'script[type*="json"]::text')
        loader.add_css("num_ratings", 'script[type*="json"]::text')
        loader.add_css("num_reviews", 'script[type*="json"]::text')
        loader.add_css("avg_rating", 'script[type*="json"]::text')
        loader.add_css("awards", 'script[type*="json"]::text')
        loader.add_css("book_format", 'script[type*="json"]::text')

        yield loader.load_item()

        author_url = response.css('a.authorName::attr(href)').extract_first()
        yield response.follow(author_url, callback=self.author_spider.parse)
