import pandas as pd
from time import sleep, time
from amazon_price_extractor import get_amazon_book_detail, make_chrome_browser, AmazonBookDetail

def get_book_details_or_empty(browser, url):
    #sleep(2)
    try:
        start = time()
        book_detail = get_amazon_book_detail(browser, url, retries=1)
        end = time()
        print(book_detail)
        print("Took {0:.2f}s for {1}".format(end - start, url))
    except:
        return AmazonBookDetail(None, None)

    return book_detail

def main():

    update = False
    n = 10

    df = pd.read_csv('goodreads_extract.csv')
    df = df.head(n)

    if update:
        no_price_mask = df['kindle_price'].isnull()
    else:
        no_price_mask = [True] * df.shape[0]

    df_without_prices = df[no_price_mask]
    urls = df_without_prices['url'].tolist()

    browser = make_chrome_browser()

    book_details = df[no_price_mask].url.apply(lambda url: get_book_details_or_empty(browser, url))

    browser.quit()

    df.loc[no_price_mask, 'kindle_price'] = book_details.map(lambda d: d.kindle_price)
    df.loc[no_price_mask, 'amazon_product_id'] = book_details.map(lambda d: d.amazon_product_id)

    print(df.head())
    df.to_csv('goodreads_extract_with_kindle_price.csv')

if __name__ == "__main__":
    main()
