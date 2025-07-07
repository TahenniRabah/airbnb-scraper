import re
from bs4 import BeautifulSoup



def get_average_price(html: str) -> int:
    prices = []
    soup = BeautifulSoup(html,"html.parser")
    divs = soup.find_all("div",{"data-testid" : "card-container"})
    for div in divs:
        price = div.find("span",class_="_11jcbg2")
        # if not price:
        #     logger.warning(f"couldn't find price in div {div}")
        price = re.sub(r"\D","",price.text)
        # if price.isdigit():
        #     logger.debug(f"Price found : {price}")
        prices.append(int(price))
        # else:
        #     logger.warning(f"Price {price} is not a digit.")
    return  max(prices)#round(sum(prices)/len(prices)) if len(prices) else 0
