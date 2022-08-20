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

    def parse(self, response):
        loader = BookLoader(BookItem(), response=response)

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

        loader.add_css("genres", 'div.left>a.bookPageGenreLink[href*="/genres/"]::text')
        loader.add_css("awards", "a.award::text")
        loader.add_css('characters', 'a[href*="/characters/"]::text')
        loader.add_css('places', 'div.infoBoxRowItem>a[href*=places]::text')
        loader.add_css('series', 'div.infoBoxRowItem>a[href*="/series/"]::text')

        loader.add_css('asin', 'div.infoBoxRowItem[itemprop=isbn]::text')
        loader.add_css('isbn', 'div.infoBoxRowItem[itemprop=isbn]::text')
        loader.add_css('isbn', 'span[itemprop=isbn]::text')
        loader.add_css('isbn', 'div.infoBoxRowItem::text')
        loader.add_css('isbn13', 'div.infoBoxRowItem[itemprop=isbn]::text')
        loader.add_css('isbn13', 'span[itemprop=isbn]::text')
        loader.add_css('isbn13', 'div.infoBoxRowItem::text')

        loader.add_css('rating_histogram', 'script[type*="protovis"]::text')

        loader.add_css("cover", "img.ResponsiveImage::attr(src)")

        yield loader.load_item()

        author_url = response.css('a.authorName::attr(href)').extract_first()
        yield response.follow(author_url, callback=self.author_spider.parse)
