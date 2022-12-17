#Emil Javurek
#13331124
"""
The individual pages use javascript so we need to use
the selenium package to scrape data properly
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import argparse
from scrapy import Selector
import re
import time

from goodreads_login import login

def main(input_file_name, output_file_name):
    #SETUP
    driver = login()
    #read input file with links
    df = pd.read_csv(input_file_name)
    #initialize output
    books_df = pd.DataFrame()

    #iterate over books
    for index, row in df.iterrows():
        name = row["name"]
        link = row["link"]

        #scrape book
        print(f"Now running: {link}")
        tic = time.perf_counter()
        try:
            one_book = scrape(link,driver,index)
        except Exception as e:
            #if fail, emergency save and retry
            print(f"LOAD FAILED, EMERGENCY SAVE AND RETRY")
            books_df.to_csv("safety_saves/emergency_save_till_" + str(index-1) + "_index.csv", index = False)
            one_book = scrape(link,driver,index)
        toc = time.perf_counter()
        print(f"Scraping {name} took {toc-tic:0.4f} seconds. \n")

        books_df = pd.concat([books_df, one_book])

        #safety saving each 100 books just in case:
        if index % 100 == 0:
            books_df.to_csv("safety_saves/first_"+str(index)+"_books.csv", index = False)

    #save to file
    books_df.to_csv(output_file_name, index = False)

    #end driver session
    driver.close()


def scrape(link,driver,index):
    #load page and get html
    driver.implicitly_wait(10)
    driver.get(link)
    html = driver.page_source
    sel = Selector(text = html)

    #name
    name_xpath = '//*[@id="bookTitle"]/text()'
    name = sel.xpath(name_xpath).extract()[0].strip()

    #author
    author_xpath = '//*[@id="bookAuthors"]/span[2]/div/a/span/text()'
    author = sel.xpath(author_xpath).extract()[0]

    # description
    description_xpath = '//*[@id="description"]/span[2]/text()'
    description_list = sel.xpath(description_xpath).extract()
    description = ' '.join(description_list)

    # rating
    rating_xpath = '//*[@id="bookMeta"]/span[2]/text()'
    rating = sel.xpath(rating_xpath).extract()[0].replace("\n","").strip()

    # number_of_ratings
    number_of_ratings_xpath = '//*[@id="bookMeta"]/a[2]/text()'
    number_of_ratings_dirty = sel.xpath(number_of_ratings_xpath).extract()
    number_of_ratings = "".join(number_of_ratings_dirty).replace("\n","").strip(" ratings").replace(",","")

    # number_of_reviews
    number_of_reviews_xpath = '//*[@id="bookMeta"]/a[3]/text()'
    number_of_reviews_dirty = sel.xpath(number_of_reviews_xpath).extract()
    number_of_reviews = "".join(number_of_reviews_dirty).replace("\n","").strip(" reviews").replace(",","")

    # genres
    genres = sel.xpath('//div[contains(@class, "bigBoxBody")]//a[contains(@href, "genres")]/text()').extract()


    #format output
    data = {
    "link": link,
    "name": name,
    "author": author,
    "description": description,
    "rating": rating,
    "number_of_ratings": number_of_ratings,
    "number_of_reviews": number_of_reviews,
    "genres": str(genres)
    }

    output = pd.DataFrame(data, index = [0])
    return output



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
