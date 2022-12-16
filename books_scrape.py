#Emil Javurek
#13331124
"""
The goal of this script is to scrape all books from a goodreads "shelf"

We choose the "to-read" shelf as it has the most books (2 billion +)

In practice, goodread website is only willing to show the first 1249 books
so we scrape all of them

We get:
name of book
link to books page
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
import argparse
from math import ceil


def complete_url(page):
    """
    Creates a valid url for one page of the search
    """
    to_read = "https://www.goodreads.com/shelf/show/to-read?page="
    return to_read + str(page)


def main(output_file_name):
    #output dataframe
    books_df = pd.DataFrame()

    #loop through pages until last page=25
    page = 1
    while page < 26:
        print(f"Number of books collected:{page*50}")

        #load website
        url = complete_url(page)
        html = simple_get(url)
        dom = BeautifulSoup(html, 'html.parser')

        #extract book info from one page and add to result
        one_page = extract_info(dom)
        books_df = pd.concat([books_df, one_page])

        #update counter
        page += 1

    #save result to output file
    books_df.to_csv(output_file_name, index = False)

def extract_info(dom):
    """
    From single search page gets for each book:
    name
    link
    """
    #initialize result
    names = []
    links = []

    #get the info
    titles = dom.find_all("a", {"class": "bookTitle"})
    for title in titles:
        names.append(title.getText())
        links.append('https://www.goodreads.com/' + title["href"])

    #store all data in dataframe and return in
    data = {"name": names, "link": links}
    df = pd.DataFrame(data)
    return df



if __name__ == "__main__":
    #setup parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract books from amazon search")

    #Add arguments
    parser.add_argument("output", help = "output file (csv)")

    args = parser.parse_args()
    main(args.output)
