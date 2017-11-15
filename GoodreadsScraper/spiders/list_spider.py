"""Spider to extract URL's of books from a Listopia list on Goodreads"""

import scrapy

from .book_spider import BookSpider

GOODREADS_URL_PREFIX = "https://www.goodreads.com"

class ListSpider(scrapy.Spider):
    """Extract URLs of books from a Listopia list on Goodreads

        This subsequently passes on the URLs to BookSpider
    """
    name = "list"

    goodreads_list_url = "https://www.goodreads.com/list/show/{}?page={}"

    def __init__(self, list_name, start_page_no, end_page_no):
        super().__init__()
        self.book_spider = BookSpider()

        self.start_urls = []
        for page_no in range(int(start_page_no), int(end_page_no) + 1):
            list_url = self.goodreads_list_url.format(list_name, page_no)
            self.start_urls.append(list_url)

    def parse(self, response):
        list_of_books = response.css("a.bookTitle::attr(href)").extract()

        for book in list_of_books:
            yield response.follow(book, callback=self.book_spider.parse)
