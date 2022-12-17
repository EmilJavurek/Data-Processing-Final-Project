#Emil Javurek
#13331124
"""
The goal of this script is to scrape all books from a goodreads "shelf"

We choose the "to-read" shelf as it has the most books (2 billion +)
but except for one line where we specifiy the link, the code is generalisable
if I have the time, the project has the possibility to be expanded to more shelves
and thus more books.

In practice, goodread website is only willing to show the first 1249 books
so we scrape all of them

We get:
name of book
link to books page
"""

from bs4 import BeautifulSoup
import re
import pandas as pd
import argparse
from math import ceil
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from goodreads_login import login

def complete_url(page):
    """
    Creates a valid url for one page of the search
    """
    to_read = "https://www.goodreads.com/shelf/show/to-read?page="
    return to_read + str(page)

def add_unique(links,names,books):
    """
    adjusts "books" dictionary with added books that are actually NEW
    determination of uniqueness by link
    """
    for (link, name) in zip(links, names):
        if books.get(link):
            pass
        else:
            books[link] = name
    return(books)

def main(output_file_name):
    #setup
    driver = login()
    books = {}
    page = 1
    #loop - only first 25 pages because the others are fake/not avialable to normal users.
    while page < 26:
        print(f"Collecting books:{(page-1)*50}-{page*50}")

        #load website
        url = complete_url(page)
        tic = time.perf_counter()
        driver.get(url)
        toc = time.perf_counter()
        print(f"Loading {url} took {toc-tic:0.4f} seconds.")

        #get soup
        html = driver.page_source
        dom = BeautifulSoup(html, 'html.parser')

        #extract book info from one page and add to result
        links, names = extract_info(dom)
        #add unique results to total dictionary:
        books = add_unique(links,names,books)
        #update counter
        page += 1



    #convert result to dataframe and save to output file
    books_df = pd.DataFrame(books.items(), columns = ["link", "name"])
    books_df.to_csv(output_file_name, index = False)
    #close the driver
    driver.close()

def extract_info(dom):
    """
    From single search page gets for each book:
    name
    link
    """
    #initialize result
    links = []
    names = []

    #get the info
    titles = dom.find_all("a", {"class": "bookTitle"})
    for title in titles:
        #find name and clean of bracket info (Paperback/Hardcover ....)
        name = title.getText().rsplit("(")[0]
        #find link and make full
        link = 'https://www.goodreads.com/' + title["href"]

        #store in page result
        names.append(name)
        links.append(link)

    return links, names



if __name__ == "__main__":
    #setup parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract books from amazon search")

    #Add arguments
    parser.add_argument("output", help = "output file (csv)")

    args = parser.parse_args()
    main(args.output)
