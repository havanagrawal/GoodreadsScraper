import argparse
import pandas as pd
from time import sleep, time
from amazon_price_extractor import get_amazon_book_detail, make_chrome_browser, AmazonBookDetail

def parse_args():
    parser = argparse.ArgumentParser(description='Extractor script to retrieve and populate Kindle prices of books')

    parser.add_argument('-f', '--filename',
                        required=True,
                        help='CSV file with Goodreads data')

    parser.add_argument('-o', '--output',
                        required=True,
                        help='Output CSV file name to which data will be extracted')

    parser.add_argument('-u', '--update',
                        action='store_true',
                        default=False,
                        help='If specified, it is assumed that the input file has a "kindle_price" column')
    return parser.parse_args()

def get_book_details_or_empty(browser, url):
    #sleep(2)
    try:
        start = time()
        book_detail = get_amazon_book_detail(browser, url, retries=1)
        time_diff = time() - start
        print(book_detail)
        print(f"Took {time_diff:.2f}s for {url}")
    except:
        return AmazonBookDetail(None, None)

    return book_detail

def main():
    args = parse_args()

    df = pd.read_csv(args.filename)

    if args.update:
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
    df.to_csv(args.output)

if __name__ == "__main__":
    main()
