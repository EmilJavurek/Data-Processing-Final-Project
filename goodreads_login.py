#Emil Javurek
#13331124
"""
Creates driver session and logs into goodreads
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

def login():
    """
    initiates driver and logs into goodreads
    returns open driver
    """
    email = 'emil.javurek@student.uva.nl'
    password = 'FinalProject6666'
    url = 'https://www.goodreads.com'

    #initialize driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #homepage
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="signIn"]/div/div/a').click()
    #sign in with email
    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="choices"]/div/a[2]/button').click()
    #put in credentials
    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="ap_email"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()

    #not a robot check == 15 SECONDS TO HUMANLY INPUT LOGIN
    try:
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//*[@id="ap_password"]').send_keys(password)
        time.sleep(15)
        driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
    except Exception as e:
        pass


    return driver
