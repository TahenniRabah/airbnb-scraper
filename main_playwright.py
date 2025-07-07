
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta

from price import *



def route_intercept(route):
    """" controler les routes qui contiennent les images pour les bloquer"""
    if route.request.resource_type == "image":
        return route.abort()
    return route.continue_()


def run(pw, destination:str, headless:bool=True):
    print("Connecting to scraping browser")
    url ="https://www.airbnb.fr/"
    #url = "https://www.airbnb.fr/s/Italie/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-01-01&monthly_length=3&monthly_end_date=2025-04-01&price_filter_input_type=0&channel=EXPLORE&place_id=ChIJA9KNRIL-1BIRb15jJFz1LOI&date_picker_type=calendar&checkin=2024-12-27&checkout=2025-01-27&source=structured_search_input_header&search_type=filter_change"

    browser = pw.chromium.launch(headless=headless)

    context  = browser.new_context()
    context.set_default_timeout(30000)

    page = context.new_page()
    """ pour controller toutes les requetes reseau que le site effectue quand on charge la page   """
    #page.route("**/*", route_intercept)

    page.goto(url)
    page.get_by_role("button", name="Uniquement les cookies né").click()
    page_number = 1
    page.get_by_test_id("QA_EXPLORE_HEADER").locator("label").click()
    page.get_by_test_id("structured-search-input-field-query").fill(destination)
    page.get_by_test_id("option-0").click()
    page.get_by_test_id("expanded-searchbar-dates-months-tab").click()
    page.get_by_test_id("monthly-dial-dot-1").click()
    page.get_by_test_id("structured-search-input-search-button").click()


    html_content = page.content()
    soup = BeautifulSoup(html_content,"html.parser")

    #while True:
    # next_page_button = page.get_by_label("Suivant", exact=True)
    #     if next_page_button.get_attribute("aria-disabled") == "true":
    #         break
    #     page_number += 1
    #     page.wait_for_timeout(1000)
    #     print(f"Navigating to page {page_number}")
    #     next_page_button.click()
    #

    today = datetime.today()


    arrivee = today + relativedelta(months=1,day=1)
    arrivee_str = arrivee.strftime("%d/%m/%Y")
    depart = arrivee + relativedelta(months=1,day=1)
    depart_str = depart.strftime("%d/%m/%Y")


    for i in range(1,13):

        page.wait_for_timeout(5000)
        html_content = page.content()
        average_price = get_average_price(html=html_content)
        #page.get_by_test_id("little-search-guests").click()
        page.get_by_test_id("little-search-anytime").click()
        page.wait_for_timeout(500)
        page.get_by_test_id("expanded-searchbar-dates-calendar-tab").click()
        page.wait_for_timeout(500)
        page.get_by_test_id(arrivee_str).click()
        page.wait_for_timeout(500)
        page.get_by_label("Avancez pour passer au mois").click()
        page.wait_for_timeout(500)
        page.get_by_test_id(depart_str).first.click()
        page.get_by_test_id("structured-search-input-search-button").click()
        # while True:
        #     next_page_button = page.get_by_label("Suivant", exact=True)
        #     if next_page_button.get_attribute("aria-disabled") == "true":
        #         break
        #     page_number += 1
        #     page.wait_for_timeout(1000)
        #     print(f"Navigating to page {page_number}")
        #     next_page_button.click()
        #     page.wait_for_timeout(5000)
        #     html_content = page.content()
        #     average_price += get_average_price(html=html_content)
        #
        #     print(f"Page number : {page_number} Average price for date {arrivee_str} to {depart_str} is {get_average_price(html=html_content)}")
        #
        # print(f"Average price for date {arrivee_str} to {depart_str} is {average_price/page_number}")


        print(f"Average price for date {arrivee_str} to {depart_str} is {average_price}")
        arrivee_str = depart_str
        depart = depart + relativedelta(months=1, day=1)
        depart_str = depart.strftime("%d/%m/%Y")


    browser.close()

if __name__=="__main__":
    with sync_playwright() as playwright:
        run(pw=playwright,
            headless=False,
            destination="allemagne")#,headless=False)

        #lancer le debug: PWDEBUG=1 python main.py