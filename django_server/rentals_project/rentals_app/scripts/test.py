import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

import time

def get_offers(district, town):
    CHROME_DRIVER_PATH = "C:/Users/dmars/Documents/PRACA_INZYNIERSKA/project_python/django_server/rentals_project/rentals_app/scripts/chromedriver.exe"
    options = ChromeOptions()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1230,800')
    options.add_argument('--disable-gpu')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--headless")
    selenium_service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=selenium_service, options=options)
    driver.get("https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska")
    time.sleep(5)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    search_confirm_button = driver.find_element(By.CSS_SELECTOR, "[data-cy='search.submit-form.default']")
    driver.find_element(By.ID, "location").click()
    search_place_input = driver.find_element(By.CSS_SELECTOR, "[data-cy='location-picker-input']")

    search_place_input.send_keys(f"{district} {town}")
    time.sleep(3)
    suggestion_item = driver.find_element(By.CSS_SELECTOR, "[data-cy='checkboxButton']")
    suggestion_item.click()
    search_confirm_button.click()
    time.sleep(2)
    all_offers = driver.find_elements(By.CSS_SELECTOR, "[data-cy='search.listing.organic'] [data-cy='listing-item']")
    info = []
    for offer in all_offers:
        link_el = offer.find_element(By.CSS_SELECTOR, "[data-cy='listing-item-link']")
        link = link_el.get_attribute("href")
        driver.switch_to.new_window("tab")
        driver.get(link)
        offer_title = driver.find_element(By.CSS_SELECTOR, "[data-cy='adPageAdTitle']").text
        offer_address = driver.find_element(By.CSS_SELECTOR, "[aria-label='Adres']").text
        offer_price = driver.find_element(By.CSS_SELECTOR, "[data-cy='adPageHeaderPrice']").text.split(" ")
        offer_price_int = int(offer_price[0] + offer_price[1])
        offer_surface = driver.find_element(By.CSS_SELECTOR, "[data-testid='table-value-area']").text
        try:
            offer_rent = int(driver.find_element(By.CSS_SELECTOR, "[data-testid='table-value-rent']").text.split(" ")[0])
        except :
            offer_rent = "N/A"
        info.append({"title": offer_title, "address": offer_address,
                     "surface": offer_surface, "price": offer_price_int, "rent": offer_rent})
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return info

