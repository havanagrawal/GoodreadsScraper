import scrapy

class BookSpider(scrapy.Spider):

    start_urls = ["https://www.goodreads.com/book/show/5470.1984"]

    def parse(self, response):
        pass
