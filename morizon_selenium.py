import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from districs import Gdansk, Gdynia

CHROME_DRIVER_PATH = "C:/Users/dmars/Documents/PRACA_INZYNIERSKA/project_python/chromedriver.exe"
options = webdriver.ChromeOptions()
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument('--no-sandbox')
# options.add_argument('--window-size=1230,800')
# options.add_argument('--disable-gpu')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--headless")
selenium_service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=selenium_service, options=options)

gdansk_controller = Gdansk()
gdynia_controller = Gdynia()
if gdansk_controller.file_present is False or gdynia_controller.file_present is False:
    # Gdansk
    gdansk_controller.create_district_files()

    # Gdynia
    gdynia_controller.create_district_files()

driver.get("https://www.morizon.pl/do-wynajecia/mieszkania/najnowsze/")
search_location_input = driver.find_element(By.ID, "search-location-input")
search_location_input.click()

gdansk_controller.display_districts()
district_input = int(input("Choose one of the districts (provide number): "))
chosen_district = gdansk_controller.districts[district_input - 1]
search_location_input.send_keys(chosen_district + " Gdańsk")
time.sleep(5)
first_listed_district = driver.find_element(By.CSS_SELECTOR, "div li")
first_listed_district.click()
time.sleep(5)
search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Szukaj']")

