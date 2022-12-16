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

from bs4 import BeautifulSoup
import re
import pandas as pd
import argparse
from math import ceil

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
            print("new book!")
            books[link] = name
    return(books)

def main(output_file_name):
    #setup
    driver = login()

    #output dict
    books = {}

    #loop through pages until last page=25
    page = 1

    while page < 26:
        print(f"Collecting books:{(page-1)*50}-{page*50}")

        #load website
        url = complete_url(page)
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source
        dom = BeautifulSoup(html, 'html.parser')


        #extract book info from one page and add to result
        links, names = extract_info(dom)
        print(names)

        #add unique results to total dictionary:
        books = add_unique(links,names,books)
        #update counter
        page += 1



    #convert result to dataframe
    books_df = pd.DataFrame(books.items(), columns = ["link", "name"])

    #save result to output file
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
