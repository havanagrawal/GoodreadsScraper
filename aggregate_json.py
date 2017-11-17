import pandas as pd
import numpy as np
import argparse

from collections import namedtuple

def parse_args():
    parser = argparse.ArgumentParser(description='Aggregator script to clean and persist Goodreads data')
    parser.add_argument('-f', '--filenames', nargs='+', help='Space separated JSON files extracted from Goodreads', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file name to which data will be extracted', required=True)
    return parser.parse_args()

def main():
    args = parse_args()

    dfs = [pd.read_json(filename) for filename in args.filenames]

    df = pd.concat(dfs)

    encode_genres(df)
    drop_unnecessary_columns(df)
    clean_numbers(df)
    breakdown_publish_date(df)

    df.drop_duplicates(inplace=True)

    print(df.head())

    df.to_csv(args.output)

def encode_genres(df):
    all_genres = {genre for row_genres in df.genres for genre in row_genres}

    for genre in all_genres:
        has_genre = lambda g: genre in g
        df[genre] = df.genres.apply(has_genre)

    most_common_genres = df[list(all_genres)].sum().sort_values(ascending=False).head(30)
    most_common_genres = most_common_genres.index.tolist()

    unwanted_genres = list(all_genres - set(most_common_genres))
    df.drop(unwanted_genres, axis=1, inplace=True)

def drop_unnecessary_columns(df):
    df['num_awards'] = df['awards'].apply(len)
    df.drop(['genres', 'awards', 'places', 'character_names'], axis=1, inplace=True)

def clean_numbers(df):
    for col in ['num_reviews', 'num_ratings']:
        df[col] = df[col].apply(lambda s: int(s.replace(",", "")))

def breakdown_publish_date(df):
    Date = namedtuple('Date', ['year', 'month', 'day'])

    def breakdown_date(date):
        if not date:
            return Date(None, None, None)
        year, month, day = date.split()[0].split("-")
        return Date(year, month, day)

    publish_dates = df['publish_date'].replace(np.nan, None).apply(breakdown_date)

    df['publish_year'] = publish_dates.map(lambda x: x.year)
    df['publish_month'] = publish_dates.map(lambda x: x.month)
    df['publish_day'] = publish_dates.map(lambda x: x.day)


if __name__ == "__main__":
    main()
