import requests
from bs4 import BeautifulSoup

def check_phrase_on_page(url, phrase):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if the page contains the specified phrase
        if phrase in soup.get_text():
            print(f"The phrase '{phrase}' is present on the page.")
        else:
            print(f"The phrase '{phrase}' is not present on the page.")
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")

# Test the function with the URL and the phrase you want to search for
url = "https://www.webstaurantstore.com/avantco-rw60-60-cup-sealed-electric-rice-warmer-120v-103w/177RW60.html"  # Replace this with the URL of the webpage you want to test
phrase_to_search = "Notify me when this product is back in stock"
check_phrase_on_page(url, phrase_to_search)
