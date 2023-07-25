import requests
from bs4 import BeautifulSoup
import re

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

        if minimum_buy:
            price = str(float(price) * minimum_buy)

    return [price, stock]

# Test the function with the URL
url = "https://www.webstaurantstore.com/lavex-janitorial-13-qt-3-gallon-brown-rectangular-wastebasket-trash-can/475WC13BR.html"
result = parser_solo(url)
print(result)
