"""Spider to extract information from a /book/show type page on Goodreads"""

import scrapy
from ..items import BookItem, BookLoader

class BookSpider(scrapy.Spider):
    """Extract information from a /book/show type page on Goodreads"""
    name = "book"

    def __init__(self):
        super().__init__()
        self.books_parsed = 0

    def report_progress_every_n(self, n):
        if self.books_parsed % n == 0:
            self.logger.info("%d books parsed till now.", self.books_parsed)

    def parse(self, response):
        loader = BookLoader(BookItem(), response=response)
        self.books_parsed += 1
        self.report_progress_every_n(50)

        loader.add_value('url', response.request.url)

        loader.add_css("title", "#bookTitle::text")
        loader.add_css("author", "a.authorName>span::text")

        loader.add_css("num_ratings", "[itemprop=ratingCount]::attr(content)")
        loader.add_css("num_reviews", "[itemprop=reviewCount]::attr(content)")
        loader.add_css("avg_rating", "span[itemprop=ratingValue]::text")
        loader.add_css("num_pages", "span[itemprop=numberOfPages]::text")

        loader.add_css("language", "div[itemprop=inLanguage]::text")
        loader.add_css('publish_date', 'div.row::text')
        loader.add_css('publish_date', 'nobr.greyText::text')

        loader.add_css('original_publish_year', 'nobr.greyText::text')

        loader.add_css("genres", "div.left>a[href*=genres]::text")
        loader.add_css("awards", "div#bookDataBox>.award::text")
        loader.add_css('characters', 'a[href*="/characters/"]::text')
        loader.add_css('places', 'div.infoBoxRowItem>a[href*=places]::text')
        loader.add_css('series', 'div.infoBoxRowItem>a[href*="/series/"]::text')
        loader.add_css('asin', 'div.infoBoxRowItem[itemprop=isbn]::text')
        loader.add_css('isbn', 'div.infoBoxRowItem>span[itemprop=isbn]::text')

        yield loader.load_item()
