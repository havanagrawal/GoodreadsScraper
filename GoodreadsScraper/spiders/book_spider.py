import scrapy
from dateutil.parser import parse as dateutil_parse

class BookSpider(scrapy.Spider):

    name = "book"

    def parse(self, response):

        book_details = {}

        book_details['num_ratings'] = response.css("span.votes::text").extract_first().strip()
        book_details['num_reviews'] = response.css("span.count::text").extract_first().strip()
        book_details['avg_ratings'] = float(response.css("span.average[itemprop=ratingValue]::text").extract_first().strip())
        book_details['genres'] = response.css("div.left>a[href*=genres]::text").extract()

        num_pages = response.css("span[itemprop=numberOfPages]::text").extract_first()

        if num_pages:
            book_details['num_pages'] = num_pages.strip().split()[0]

        book_data = response.css("div#bookDataBox")

        book_details['awards'] = book_data.css(".award::text").extract()
        book_details['places'] = book_data.css("a[href*=places]::text").extract()
        book_details['character_names'] = book_data.css('a[href*="characters"]::text').extract()
        book_details['language'] = book_data.css("div[itemprop=inLanguage]::text").extract_first()

        if book_details['language']:
            book_details['language'].strip()


        maybe_dates = response.css("div.row::text").extract()
        maybe_dates = [s for s in maybe_dates if "published" in s.lower()]

        published_dates = [dateutil_parse(date, fuzzy=True) for date in maybe_dates]

        book_details['publish_date'] = published_dates

        feature_names = book_data.css("div.infoBoxRowTitle::text").extract()
        feature_values = book_data.css("div.infoBoxRowItem::text").extract()

        desired_names = set(["Original Title", "ISBN"])

        for name, value in zip(feature_names, feature_values):
            if name in desired_names:
                book_details[name.strip()] = value.strip()

        yield book_details
