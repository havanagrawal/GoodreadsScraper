import logging
from selenium import webdriver
from datetime import datetime
from collections import namedtuple

AmazonBookDetail = namedtuple('AmazonBookDetail', ['kindle_price', 'amazon_product_id'])

def main():
    urls = ["https://www.goodreads.com/book/show/17212231-inferno"]#, "https://www.goodreads.com/book/show/13148921-bloodline", "https://www.goodreads.com/book/show/5470.1984", "https://www.goodreads.com/book/show/13651.The_Dispossessed"]

    browser = make_chrome_browser()
    for url in urls:
        print(get_amazon_book_detail(browser, url))

    browser.quit()

def make_chrome_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

    return browser

def get_amazon_book_detail(browser, url, retries=0):
    """Retrieve the Kindle price and Amazon product ID from the Goodreads book URL

        Occasionally, the webdriver can fail to retrieve the data even though it exists,
        which can be resolved by providing a positive retry count.
    """
    # Prevent negative retries
    retries = max(retries, 0)

    browser.get(url)

    element = browser.find_element_by_css_selector("a[data-asin]")

    amzn_product_id = element.get_attribute('data-asin')
    kindle_price = element.text.split(" ")[-1]

    if not kindle_price and retries != 0:
        logging.info(f"Retrying for {url}. #Retries left = {retries}")
        return get_amazon_book_detail(browser, url, retries - 1)

    return AmazonBookDetail(kindle_price, amzn_product_id)

if __name__ == "__main__":
    main()
