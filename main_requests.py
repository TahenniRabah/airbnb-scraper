import logging
from pathlib import Path
import re
import sys

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

FILEPATH = Path(__file__).parent / "airbnb.html"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)


def fetch_content(url: str, from_disk: bool = False) -> str:
    if from_disk and FILEPATH.exists():
        return _read_from_file()

    try:
        logger.debug(f"Making request to {url}")
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url)#,headers=headers)
        response.raise_for_status()
        html_content = response.text
        _write_to_file(content=html_content)
        return html_content
    except RequestException as e:
        logger.error(f"couldn't fetch content from {url} due to {str(e)}")
        raise e


def get_average_price(html: str) -> int:
    prices = []
    soup = BeautifulSoup(html,"html.parser")
    divs = soup.find_all("div",{"data-testid" : "card-container"})
    for div in divs:
        price = div.find("span",class_="_11jcbg2")
        if not price:
            logger.warning(f"couldn't find price in div {div}")
        price = re.sub(r"\D","",price.text)
        if price.isdigit():
            logger.debug(f"Price found : {price}")
            prices.append(int(price))
        else:
            logger.warning(f"Price {price} is not a digit.")
    # data-testid="card-container"
    # _11jcbg2
    return  round(sum(prices)/len(prices)) if len(prices) else 0

def _write_to_file(content: str) -> bool:
    logger.debug("Writing content to file")
    with open(FILEPATH, "w", encoding="utf-8") as f:
        f.write(content)

    return FILEPATH.exists()


def _read_from_file() -> str:
    logger.debug("reading content from file")

    with open(FILEPATH, "r", encoding="utf-8") as f:
        content = f.read()

    return content


if __name__ == "__main__":
    url ="https://www.airbnb.fr/"
    url = sys.argv[-1]
    #url="https://www.airbnb.fr/s/Italie/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-01-01&monthly_length=3&monthly_end_date=2025-04-01&price_filter_input_type=0&channel=EXPLORE&place_id=ChIJA9KNRIL-1BIRb15jJFz1LOI&date_picker_type=calendar&checkin=2024-12-27&checkout=2025-01-27&source=structured_search_input_header&search_type=filter_change"
    content = fetch_content(url=url, from_disk=False)
    average_price = get_average_price(content)
    print(average_price)

