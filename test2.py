import requests
from bs4 import BeautifulSoup

url_nice = "https://www.webstaurantstore.com/scotsman-cu3030sw-1a-prodigy-series-30-water-cooled-undercounter-small-cube-ice-machine-347-lb/720CU3030SW1.html" #
url_non_exist = "https://www.webstaurantstore.com/snap-drape-bst630blk-72-x-30-black-table-with-stretch-cover/757BST630BLK.html"       #
url_2 = "https://www.webstaurantstore.com/choice-17-1-4-aluminum-pot-pan-cover/471SPC60.html" #
url_3 = "https://www.webstaurantstore.com/wastecan-19-gal-square-bl/475SQ19BK.html" #
url_4 = "https://www.webstaurantstore.com/lavex-janitorial-23-gallon-brown-slim-trash-can/475WH23BR.html"#
url_if_minimum_4 = "https://www.webstaurantstore.com/lancaster-table-seating-white-resin-folding-chair-with-vinyl-seat/427FCRVINWHT.html"#
url_if_minimum_10 = "https://www.webstaurantstore.com/lancaster-table-seating-white-resin-folding-chair-with-slatted-seat/427FCRSLTWHT.html"#
url_if_dropdown = "https://www.webstaurantstore.com/lavex-packaging-32-x-32-x-32-kraft-corrugated-rsc-shipping-box-bundle/442BOX32CUBE.html" #
url_no_longer_avaible = "https://www.webstaurantstore.com/avantco-rw60-60-cup-sealed-electric-rice-warmer-120v-103w/177RW60.html"      #
url_out_of_stock = "https://www.webstaurantstore.com/lavex-janitorial-13-qt-3-gallon-brown-rectangular-wastebasket-trash-can/475WC13BR.html" #

def parser_solo():
    url = url_non_exist
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            table_element = soup.select_one("table.table.table-bordered")
            is_table = True
        except AttributeError:
            is_table = False

        print(is_table)

    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")

parser_solo()