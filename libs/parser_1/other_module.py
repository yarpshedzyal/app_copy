# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options 
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
import json
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re
import datetime

# import requests
# from bs4 import BeautifulSoup
# import re

def clean_price_string(price_str):
    parts = price_str.split(".", 1)
    if len(parts) == 2:
        cleaned_price = f"{parts[0]}.{parts[1][:2]}"
    else:
        cleaned_price = price_str.replace(".", "")
    cleaned_price = re.sub(r"[^\d.]", "", cleaned_price)
    return cleaned_price

def get_minimum_buy_number(soup):
    min_must_text_element = soup.find("p", {"class": "min-must-text"})
    if min_must_text_element:
        minimum_buy_number = re.search(r"\d+", min_must_text_element.text)
        if minimum_buy_number:
            return int(minimum_buy_number.group())
    return None

def parser_solo(url):
    response = requests.get(url)
    stock = "Out"
    price = "0"

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        svg_element = soup.find("svg", {"class": "block mx-auto align-middle"})
        phrase_unavailable = "This Product is no longer available"
        phrase_out_of_stock = "Notify me when this product is back in stock"

        if svg_element or phrase_unavailable in soup.get_text() or phrase_out_of_stock in soup.get_text():
            stock = "Out"
        else:
            stock = "In"

        min_must_text_element = soup.find("p", {"class": "min-must-text"})
        minimum_buy = get_minimum_buy_number(soup)

        table_element = soup.select_one("table.table.table-bordered")
        if table_element:
            rows = table_element.select("tbody tr")
            last_th = None
            last_td = None
            for row in rows:
                th = row.select_one("th").text
                td = row.select_one("td").text.strip()
                last_th = th
                last_td = td

            if last_th and last_td:
                filtered_td = re.sub(r'[^\d.]', '', last_td)
                price = clean_price_string(filtered_td)
            else:
                return "Table has no rows or data."
        else:
            price_element = soup.select_one("p.price")
            if price_element:
                price = price_element.text.strip().replace("$", "").replace(",", "")
                filtered_price = re.sub(r'[^\d.]', '', price)
                price = clean_price_string(filtered_price)
            else:
                return "Price element not found."

        was_price_element = soup.select_one("p.was-price")
        if was_price_element:
            price = was_price_element.text.strip().replace("$", "").replace(",", "")
            filtered_price = re.sub(r'[^\d.]', '', price)
            price = clean_price_string(filtered_price)

        if minimum_buy:
            price = str(float(price) * minimum_buy)

    return [price, stock]

# # new options
# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--disable-setuid-sandbox")
# # other options
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument('--ignore-certificate-errors')
# # chrome_options.headless = True


# options = Options()
# options.add_argument("--headless")
# # options.headless = True
# # options.add_argument("--window-size=1920,1200")
# # options.binary_location = 

# urls for test
# url = "https://www.webstaurantstore.com/lancaster-table-seating-french-bistro-black-outdoor-arm-chair/427CAFRBSBLK.html" # multi
# url_1 = "https://www.webstaurantstore.com/spaceman-6235a-c-soft-serve-countertop-ice-cream-machine-with-air-pump-2-hoppers-and-3-dispensers-208-230v/7156235ACV.html" # solo 
# nonstock_url = "https://www.webstaurantstore.com/regency-black-epoxy-5-shelf-angled-stationary-merchandising-rack-18-x-48-x-74/460EB1848SDS.html" # nonstock 


# driver = webdriver.Chrome(options=chrome_options)

# driver = webdriver.Chrome(options=options, executable_path="chromedriver_linux64\chromedriver")


# def format_price(string):                           # delets $ and /Each from parced price
#     formated_string = str(string)
#     formated_string = formated_string.replace("$", "")
#     formated_string = formated_string.replace("/Each", "")
#     formated_string = formated_string.replace("/Case", "")
#     formated_string = formated_string.replace("/Pack", "")
#     formated_string = formated_string.replace("/Bundle", "")
#     formated_string = formated_string.replace(",","")
#     number_match = re.search(r'\d+(\.\d+)?', formated_string)
#     if number_match:
#         number = float(number_match.group())
#     else:
#         number = None
#     formated_string = number
#     return formated_string

# def parser_solo(url):
#     Price = ''
#     Stock = 'In'
#     driver.get(url)

#     try:
#         driver.find_element(By.XPATH, "//div[contains(@class, 'pricing')]/table/tbody/tr/td")
#         multi_check_bool = True
#     except NoSuchElementException:
#         multi_check_bool = False

#     try:
#         driver.find_element(By.ID, "unavailableContainer")
#         stock_check_bool = False
#     except NoSuchElementException:
#         stock_check_bool = True
    
#     try:
#         driver.find_element(By.CLASS_NAME, 'product-subhead')
#         item_exist = True
#     except NoSuchElementException:
#         item_exist = False

#     if not item_exist:
#         Price =  Price = (driver.find_element(By.CLASS_NAME, "price")) # in stock and bulk price ,,, copied because string cant have .text attribute
#         Stock = 'Out'
#     elif stock_check_bool and multi_check_bool:
#         Price = (driver.find_element(By.XPATH, "//div[contains(@class,'pricing')]/table/tbody/tr/td")) # in stock and bulk price
#     elif stock_check_bool and not multi_check_bool:
#         Price = (driver.find_element(By.CLASS_NAME, "price")) # in stock no bulk price
#     elif not stock_check_bool and multi_check_bool:
#         Price = (driver.find_element(By.XPATH, "//div[contains(@class,'pricing')]/table/tbody/tr/td")) # out of stock and bulk price
#         Stock = 'Out'
#     elif not stock_check_bool and not multi_check_bool:
#         Price = (driver.find_element(By.CLASS_NAME, "price")) # out of stock no bulk price
#         Stock = 'Out'
#     driver.quit()
#     price_text = Price.text
    
#     return [format_price(price_text), Stock]




def count():
    client = MongoClient('mongodb+srv://user_yarpshe:Q1w2e3r4_0@cluster0.aktya2j.mongodb.net/')
    db = client['test_1506']
    collection = db['test']
    count = collection.count_documents({})
    return count

print(parser_solo('https://www.webstaurantstore.com/backyard-pro-weekend-series-30-qt-turkey-fryer-kit-with-stainless-steel-stock-pot-and-accessories-55-000-btu/554BP16SSKIT.html'))


