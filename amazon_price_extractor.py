from selenium import webdriver
from datetime import datetime


def main():
    browser = make_chrome_browser()
    urls = ["https://www.goodreads.com/book/show/17212231-inferno"]#, "https://www.goodreads.com/book/show/13148921-bloodline", "https://www.goodreads.com/book/show/5470.1984", "https://www.goodreads.com/book/show/13651.The_Dispossessed"]

    for url in urls:
        print(get_kindle_price(browser, url))

    browser.quit()

def make_chrome_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

    return browser

def get_kindle_price(browser, url):
    browser.get(url)

    element = browser.find_element_by_css_selector("a[data-asin]")

    if not element:
        return None

    kindle_price = element.text.split(" ")[-1]

    return kindle_price

if __name__ == "__main__":
    main()
