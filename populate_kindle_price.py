import pandas as pd
from time import sleep, time
from amazon_price_extractor import get_kindle_price, make_chrome_browser

def get_kindle_price_or_none(browser, url):
    sleep(5)
    try:
        start = time()
        price = get_kindle_price(browser, url)
        end = time()
        print("Took {0:.2f}s for {}".format(end - start, url))
    except:
        price = None

    return price

def main():

    update = True
    n = 100

    df = pd.read_csv('goodreads_extract_with_kindle_price.csv')
    df = df.head(n)

    if update:
        no_price_mask = df['kindle_price'].isnull()
    else:
        no_price_mask = [True] * df.shape[0]

    df_without_prices = df[no_price_mask]
    urls = df_without_prices['url'].tolist()

    browser = make_chrome_browser()

    df.loc[no_price_mask, 'kindle_price'] = df[no_price_mask].url.apply(lambda url: get_kindle_price_or_none(browser, url))
    print(df.head())
    df.to_csv('goodreads_extract_with_kindle_price.csv')

if __name__ == "__main__":
    main()
