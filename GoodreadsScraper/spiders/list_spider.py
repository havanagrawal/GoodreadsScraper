import scrapy

from .book_spider import BookSpider

GOODREADS_URL_PREFIX = "https://www.goodreads.com"

class ListSpider(scrapy.Spider):
    name = "list"

    def __init__(self, page_no):
        self.book_spider = BookSpider()
        list_name = "264.Books_That_Everyone_Should_Read_At_Least_Once"
        self.start_urls = ["https://www.goodreads.com/list/show/{}?page={}".format(list_name, page_no)]

    def parse(self, response):
        list_of_books = response.css("a.bookTitle::attr(href)").extract()

        for book in list_of_books:
            yield response.follow(book, callback=self.book_spider.parse)
