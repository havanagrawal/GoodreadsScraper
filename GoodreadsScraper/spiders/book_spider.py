import scrapy

class BookSpider(scrapy.Spider):

    name = "book"
    start_urls = ["https://www.goodreads.com/book/show/5470.1984"]

    def parse(self, response):

        book_details = {}

        book_details['num_ratings'] = response.css("span.votes::text").extract_first().strip()
        book_details['num_reviews'] = response.css("span.count::text").extract_first().strip()
        book_details['avg_ratings'] = float(response.css("span.average[itemprop=ratingValue]::text").extract_first().strip())
        book_details['genres'] = response.css("div.left>a[href*=genres]::text").extract()

        num_pages = response.css("span[itemprop=numberOfPages]::text").extract_first().strip()

        if num_pages:
            book_details['num_pages'] = num_pages.split()[0]

        book_data = response.css("div#bookDataBox")

        book_details['awards'] = book_data.css(".award::text").extract()
        book_details['places'] = book_data.css("a[href*=places]::text").extract()
        book_details['character_names'] = book_data.css('a[href*="characters"]::text').extract()
        book_details['language'] = book_data.css("div[itemprop=inLanguage]::text").extract_first().strip()

        book_details['publish_date'] = response.css("nobr.greyText::text").extract_first().split()[-3:]

        feature_names = book_data.css("div.infoBoxRowTitle::text").extract()
        feature_values = book_data.css("div.infoBoxRowItem::text").extract()

        desired_names = set(["Original Title", "ISBN"])

        for name, value in zip(feature_names, feature_values):
            if name in desired_names:
                book_details[name.strip()] = value.strip()

        yield book_details
