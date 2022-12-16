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

def main(input_file_name, output_file_name):
    #SETUP
    driver = webdriver.Chrome(ChromeDriverManager().install())


    #read input file with links
    df = pd.read_csv(input_file_name)

    #initialize output
    books_df = pd.DataFrame()

    #iterate over books
    for index, row in df.iterrows():
        name = row["name"]
        link = row["link"]

        #check
        print(f"Now running: {link}")

        one_book = scrape(link,driver)
        books_df = pd.concat([books_df, one_book])

    #save to file
    books_df.to_csv(output_file_name, index = False)

    #end driver session
    # driver.quit()


def scrape(link,driver):
    #load page and get html
    driver.get(link)
    html = driver.page_source
    sel = Selector(text = html)

    #name
    name_xpath = '//*[@id="bookTitle"]/text()'
    name = sel.xpath(name_xpath).extract()[0].strip()
    print(name)

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

    ################### TODO
    # review
    # review_rating
    # review_text

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
    #"reviews": reviews
    }

    output = pd.DataFrame(data, index = [0])
    return output




    return None

def formatting(link,scraped):
    """
    INPUT:
    not clean name,
    link to books page
    scraped data:

    OUTPUT:
    one row dataframe:
    """
    pass
















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
