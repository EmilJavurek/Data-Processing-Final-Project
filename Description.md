# Topic modelling from book descriptions
### "Can we use book descriptions to group books by topic?"
### "How does it compare to book genres?"

The goal of this project is to scrape book descriptions and genres from goodreads.com and see if we can use an LDA model to group books into topics and how well these topics compare to book genres of books listed on the website.

My personal learning goal from this is to get introduced into natural language processing, specifically using the spaCy library and Gensim LDA model. Additionaly (a major part of the project was spent on this), I want to learn how to scrape data from a non-static website that uses javascript (as is the case for goodreads.com), using Selenium, Chrome webdriver and Scrapy.

#### So what did I do in this project?
First, I scraped the "to-read" shelf of books from goodreads.com. Supposedly, it is the largest one (over 2bn books) but in reality goodreads only shows the top 1249 books for any given shelf. That is, if you are logged in, otherwise, only the top 50 shows. To do this a wrote a goodreads_login.py script that initiates the driver and logs me into the goodreads website (using an account created specifically for this project). Next, scrape_shelf.py scrapes the shelf to obtain the name and link of each book. The code is specific to the "to-read" page in just the url variable, it could be easily generalised to scraping multiple shelves, however, the crawling of said shelf already takes around an hour so I decided it is enough for this project.
