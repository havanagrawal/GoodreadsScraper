import scrapy

from book_spider import BookSpider

GOODREADS_URL_PREFIX = "https://www.goodreads.com"

class ListSpider(scrapy.Spider):
    name = "list"
    start_urls = ["https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once"]

    def __init__(self):
        self.book_spider = BookSpider()

    def parse(self, response):
        list_of_books = response.css("a.bookTitle::attr(href)").extract()
        print(list_of_books)
        #yield {"link": GOODREADS_URL_PREFIX + x}

        for book in list_of_books:
            yield response.follow(book, callback=book_spider.parse)
