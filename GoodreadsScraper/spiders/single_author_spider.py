"""Spider to extract URL's of books from a single author"""

import scrapy
from scrapy import signals
from .book_spider import BookSpider


class SingleAuthorSpider(scrapy.Spider):
    """Extract and crawl URLs of books by a specific author

        This subsequently passes on the URLs to BookSpider.
        Consequently, this spider also yields BookItem's and AuthorItem's.
    """
    name = "single-author"

    def _set_crawler(self, crawler):
        super()._set_crawler(crawler)
        crawler.signals.connect(self.item_scraped_callback,
                                signal=signals.item_scraped)

    def __init__(self, author_id, item_scraped_callback=None):
        super().__init__()
        self.book_spider = BookSpider()
        self.item_scraped_callback = item_scraped_callback
        self.start_urls = [f"https://www.goodreads.com/author/show/{author_id}", f"https://www.goodreads.com/author/list/{author_id}"]

    def parse(self, response):
        book_urls = response.css("a.bookTitle::attr(href)").extract()

        for book_url in book_urls:
            yield response.follow(book_url, callback=self.book_spider.parse)

        next_page = response.css('a.next_page').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
