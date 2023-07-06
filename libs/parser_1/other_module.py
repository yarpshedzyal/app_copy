from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
from pymongo import MongoClient
import datetime 


# new options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-setuid-sandbox")
# other options
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.headless = True


# options = Options()
# options.add_argument("--headless")
# # options.headless = True
# # options.add_argument("--window-size=1920,1200")
# # options.binary_location = 

# urls for test
# url = "https://www.webstaurantstore.com/lancaster-table-seating-french-bistro-black-outdoor-arm-chair/427CAFRBSBLK.html" # multi
# url_1 = "https://www.webstaurantstore.com/spaceman-6235a-c-soft-serve-countertop-ice-cream-machine-with-air-pump-2-hoppers-and-3-dispensers-208-230v/7156235ACV.html" # solo 
# nonstock_url = "https://www.webstaurantstore.com/regency-black-epoxy-5-shelf-angled-stationary-merchandising-rack-18-x-48-x-74/460EB1848SDS.html" # nonstock 


driver = webdriver.Chrome(options=chrome_options)

# driver = webdriver.Chrome(options=options, executable_path="chromedriver_linux64\chromedriver")


def format_price(string):                           # delets $ and /Each from parced price
    formated_string = str(string)
    formated_string = formated_string.replace("$", "")
    formated_string = formated_string.replace("/Each", "")
    return formated_string

def parser_solo(url):
    Price = ''
    Stock = 'In'
    driver.get(url)

    try:
        driver.find_element(By.XPATH, "//div[contains(@class, 'pricing')]/table/tbody/tr/td")
        multi_check_bool = True
    except NoSuchElementException:
        multi_check_bool = False

    try:
        driver.find_element(By.ID, "unavailableContainer")
        stock_check_bool = False
    except NoSuchElementException:
        stock_check_bool = True
    

    if stock_check_bool and multi_check_bool:
        Price = (driver.find_element(By.XPATH, "//div[contains(@class,'pricing')]/table/tbody/tr/td")) # in stock and bulk price
    elif stock_check_bool and not multi_check_bool:
        Price = (driver.find_element(By.CLASS_NAME, "price")) # in stock no bulk price
    elif not stock_check_bool and multi_check_bool:
        Price = (driver.find_element(By.XPATH, "//div[contains(@class,'pricing')]/table/tbody/tr/td")) # out of stock and bulk price
        Stock = 'Out'
    elif not stock_check_bool and not multi_check_bool:
        Price = (driver.find_element(By.CLASS_NAME, "price")) # out of stock no bulk price
        Stock = 'Out'
    driver.quit
    price_text = Price.text
    
    return [format_price(price_text), Stock]


def parse_all():
    print('incoming')


