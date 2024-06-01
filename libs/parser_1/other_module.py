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
        phrase_unavailable_2 = "This product is no longer available"
        phrase_out_of_stock = "Notify me when this product is back in stock"
        phrase_works_with = 'Works With'
        product_from_line = 'Other Products from this Line'
        selector_for_sale = '#priceBox > div.pricing > p.sale-price > span.text-black.font-bold.bg-yellow-400.rounded-sm.antialiased.mr-1.mt-0\.5.px-3\/4.py-0\.5.text-sm'

        if svg_element or (phrase_unavailable in soup.get_text()) or (phrase_out_of_stock in soup.get_text()) or (phrase_unavailable_2 in soup.get_text()):
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
            price_element = soup.select_one("#priceBox > div.pricing > p > span")
            if price_element and not table_element:
                price = price_element.text.strip().replace("$", "").replace(",", "")
                filtered_price = re.sub(r'[^\d.]', '', price)
                price = clean_price_string(filtered_price)
            # else:
            #     return "Price element not found."
            
        if phrase_works_with in soup.get_text() and not table_element:
            price_element = soup.select_one('#priceBox > div.pricing > p > span')
            if price_element:
                price = price_element.text.strip().replace("$", "").replace(",", "")
                filtered_price = re.sub(r'[^\d.]', '', price)
                price = clean_price_string(filtered_price)
            # else:
            #     return "Price element not found."
        
        sale_element = soup.select_one('#priceBox > div.pricing > p.sale-price > span.text-black.font-bold.bg-yellow-400.rounded-sm.antialiased.mr-1.mt-0\.5.px-3\/4.py-0\.5.text-sm')
        if sale_element and not table_element:
            price_element = soup.select_one('#priceBox > div.pricing > p.sale-price > span:nth-child(2)')
            if price_element:
                price = price_element.text.strip().replace("$", "").replace(",", "")
                filtered_price = re.sub(r'[^\d.]', '', price)
                price = clean_price_string(filtered_price)
            # else:
            #     return 'Price element not found'
            
        # if product_from_line in soup.get_text():
        #     price_element = soup.select_one('#priceBox > div.pricing > p > span')

        p_r_error_text = 'Contact us or '
        if p_r_error_text in soup.get_text() and not table_element:
            price_element = soup.select_one('#priceBox > div.pricing > div > p.leading-none.mb-0')
            if price_element:
                price = price_element.text.strip().replace("$", "").replace(",", "")
                filtered_price = re.sub(r'[^\d.]', '', price)
                price = clean_price_string(filtered_price)
            # else:
            #     return 'Price element not found'
     
        was_price_element = soup.select_one("p.was-price")
        if was_price_element and not table_element:
            price = was_price_element.text.strip().replace("$", "").replace(",", "")
            filtered_price = re.sub(r'[^\d.]', '', price)
            price = clean_price_string(filtered_price)

        buybox_new_14_05_2024 = soup.select_one('#priceBox > div.pricing > div.plus-member.plus-member-override.plus-member--plus > div > div.plus-member__text.plus-member__price > p > span')
        if buybox_new_14_05_2024 and not table_element:
            price = buybox_new_14_05_2024.text.strip().replace('$', '').replace(',', '')
            filtered_price = re.sub(r'[^\d.]', '', price)
            price = clean_price_string(filtered_price)

        bug_01_06_2024 = soup.select_one('#priceBox > div.pricing > table > tbody > tr > td')
        if bug_01_06_2024:
            price_el = soup.select_one('#priceBox > div.pricing > p > span')
            price = price_el.text.strip().replace('$', '').replace(',','')
            filtered_price = re.sub(r'[^\d.]', '', price)
            price = clean_price_string(filtered_price)

        if minimum_buy:
            price = str(float(price) * minimum_buy)
        if 'search' in url:
            stock = 'Out'
    return [price, stock]


def count():
    client = MongoClient('mongodb+srv://user_yarpshe:Q1w2e3r4_0@cluster0.aktya2j.mongodb.net/')
    db = client['test_1506']
    collection = db['test']
    count = collection.count_documents({})
    return count

# print(parser_solo('https://www.webstaurantstore.com/backyard-pro-weekend-series-30-qt-turkey-fryer-kit-with-stainless-steel-stock-pot-and-accessories-55-000-btu/554BP16SSKIT.html'))
# print(parser_solo('https://www.webstaurantstore.com/regency-48-x-20-x-8-aluminum-dunnage-rack-1300-lb-capacity/600DUN2048.html'), 'other products from this line')
# print(parser_solo('https://www.webstaurantstore.com/avantco-cpo16ts-stainless-steel-countertop-pizza-snack-oven-with-adjustable-thermostatic-control-120v-1700w/177CPO16TS.html'), 'no price')
# print(parser_solo('https://www.webstaurantstore.com/choice-32-x-16-x-38-black-3-shelf-utility-bus-cart/109CARTBUSBK.html'), 'multi eror ulr')
# print(parser_solo('https://www.webstaurantstore.com/national-public-seating-tfxs48482432c02-transfix-48-x-48-adjustable-portable-stage-with-gray-carpet-24-to-32-height/386TF4824C02.html'), 'p-r error')
# print(parser_solo('https://www.webstaurantstore.com/avantco-chsme24a-24-countertop-electric-cheese-melter-120v-1600w/177CHSME24A.html'), 'end-of-sell')
# print(parser_solo('https://www.webstaurantstore.com/avantco-chsme23m-23-electric-countertop-cheese-melter-208-240v-1800-2400w/177CHSME23M.html'), 'end-of-sell')
# print(parser_solo('https://www.webstaurantstore.com/avantco-cnvyov10a-countertop-conveyor-oven-with-10-1-2-belt-120v-1700w/177CNVYOV10A.html'), 'end-of-sell')
# print(parser_solo('https://www.webstaurantstore.com/avantco-cnvyov10a-countertop-conveyor-oven-with-10-1-2-belt-120v-1700w/177CNVYOV10A.html'), 'end-of-sell')
# print(parser_solo('https://www.webstaurantstore.com/search/442pltcube12.html'), 'zalupa vmesto linka')
# print(parser_solo('https://www.webstaurantstore.com/avantco-gdc-23-hc-28-3-8-white-swing-glass-door-merchandiser-refrigerator-with-led-lighting/178GDC23HCW.html'), 'webstore update buybox bug 14 05 2024')
