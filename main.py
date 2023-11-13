import io
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from districs import Gdansk, Gdynia
import pandas as p

is_running = True
CHROME_DRIVER_PATH = "C:/Users/dmars/Documents/PRACA_INZYNIERSKA/project_python/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
selenium_service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=selenium_service, options=options)

gdansk_controller = Gdansk()
gdynia_controller = Gdynia()
# while is_running:
if gdansk_controller.file_present is False or gdynia_controller.file_present is False:
    # Gdansk
    gdansk_controller.create_district_files()

    # Gdynia
    gdynia_controller.create_district_files()

driver.get("https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska")
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
search_confirm_button = driver.find_element(By.CSS_SELECTOR, "[data-cy='search.submit-form.default']")
driver.find_element(By.ID, "location").click()
search_place_input = driver.find_element(By.CSS_SELECTOR, "[data-cy='location-picker-input']")
gdansk_controller.display_districts()
district_input = int(input("Choose one of the districts (provide number): "))
chosen_district = gdansk_controller.districts[district_input - 1]
search_place_input.send_keys(chosen_district)
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "[data-testid='suggestions-item']").click()
search_confirm_button.click()

time.sleep(2)
all_offers = driver.find_elements(By.CSS_SELECTOR, "[data-cy='search.listing.organic'] [data-cy='listing-item']")
print(len(all_offers))
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
        offer_rent = driver.find_element(By.CSS_SELECTOR, "[data-testid='table-value-rent']").text.split(" ")
    except:
        offer_rent = "N/A"
    info.append({"Title": offer_title, "Address": offer_address,
                 "Surface": offer_surface, "Price (in zł)": offer_price_int, "Rent": offer_rent})
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
print(info)
df = pd.DataFrame.from_dict(info)
df.to_csv(f"{chosen_district}.csv", index=False, header=True)
#
# list_of_all_offers = all_offers_container.find_elements(By.CSS_SELECTOR, "[data-cy='listing-item']")
# print(len(list_of_all_offers))
