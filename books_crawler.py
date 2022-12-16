#Emil Javurek
#13331124
"""
The goal of this script is to get info about individual books,
knowing their goodread links.

We get:



"""

from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
from math import ceil
import argparse
import time

def main(input_file_name, output_file_name):
    #read input file
    df = pd.read_csv(input_file_name)

    #initialize storage
    books_df = pd.DataFrame()

    #iterate over links
    for index, link in df["link"].items():
        #check
        print(f"Now running:{link}")

        one_book = extract_info(link)
        books_df = pd.concat([books_df, one_book])

    #save to file
    books_df.to_csv(output_file_name, index = False)


def extract_info(link):
    """
    For individual book we extract following info:


    """
    #load website
    html = simple_get(link)
    # time.sleep(1)
    dom = BeautifulSoup(html, 'html.parser')


    # author

    author = dom.find("a", {"class": "authorName"}).find("span").getText()

    #check
    print(author)

    # description
    # rating
    # number_of_ratings
    # number_of_reviews
    # genres
    # review_rating
    # review_text


    #save as dataframe of one row
    data = {"author": author
    }
    df = pd.DataFrame(data, index = [0])
    return df






if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "input output")

    # Add arguments
    parser.add_argument("input", help = "input csv file location" )
    parser.add_argument("output", help = "output csv file location" )

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output)
