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
import os
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
        one_book = scrape_shell(books_df,name, link, driver, index, output_file_name)

        #add to output
        books_df = pd.concat([books_df, one_book])

        #safety saving just in case:
        safety_save(books_df, index, output_file_name, 100)

    #save to file
    books_df.to_csv(output_file_name, index = False)

    #end driver session
    driver.close()

def remove_file(file_path):
    """
    for removing files in "safety_saves" folder
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        pass

def safety_save(books_df, index, output_file_name, frequency = 100):
    """
    After every "frequency" number of books we do a safety save
    Each time we do a safety save we also remove the previous one
    and also all previous emergency saves.
    We do the removals to minimize safety files with overlap information
    (it doesnt create any extra safety)
    """
    number = index + 1
    if number % frequency == 0:
        #save
        books_df.to_csv("safety_saves/" + output_file_name[:-4] + "_first_" + str(number) + "_books.csv", index = False)
        #remove previous safety save, we only want the latest one
        previous_path = "safety_saves/" + output_file_name[:-4] + "_first_" + str(number-frequency) + "_books.csv"
        remove_file(previous_path)
        #remove previous emergency saves, we dont need them anymore:
        for i in range(index):
            path = "safety_saves/" + output_file_name[:-4] + "_emergency_till_" + str(i-1) + "_index.csv"
            remove_file(path)

def scrape_shell(books_df,name,link,driver,index,output_file_name):
    """
    Shell of actuall scrape function:
    prints progress statements
    covers scrape function in try block that includes emergency save
    """
    print(f"Now running book #{index + 1}: {link}")
    tic = time.perf_counter()

    try:
        one_book = scrape(link,driver)
    except Exception as e:
        #if fail, emergency save and retry
        print(f"LOAD FAILED, EMERGENCY SAVE AND RETRY")
        books_df.to_csv("safety_saves/" + output_file_name[:-4] + "_emergency_till_" + str(index-1) + "_index.csv", index = False)
        one_book = scrape(link,driver)

    toc = time.perf_counter()
    print(f"Scraping {name} took {toc-tic:0.4f} seconds. \n")
    return one_book

def scrape(link,driver):
    """
    Actuall data retrieval through scraping
    Loads page, gets data using xpaths
    returns one row dataframe
    """
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
