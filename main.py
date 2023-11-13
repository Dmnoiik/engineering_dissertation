import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from districs import Gdansk, Gdynia
is_running = True
gdansk_controller = Gdansk()
gdynia_controller = Gdynia()
while is_running:
    if gdansk_controller.file_present is False or gdynia_controller.file_present is False:
        # Gdansk
        gdansk_controller.create_district_files()

        # Gdynia
        gdynia_controller.create_district_files()
    else:
        print("this one")
        gdansk_controller.display_districts()
        gdynia_controller.display_districts()
        is_running = False


# CHROME_DRIVER_PATH = "C:/Users/dmars/Documents/PRACA_INZYNIERSKA/projekt/chromedriver.exe"
# options = webdriver.ChromeOptions()
# options.add_experimental_option('detach', True)
# selenium_service = Service(CHROME_DRIVER_PATH)
# driver = webdriver.Chrome(service=selenium_service, options=options)
#
# driver.get("https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska")
# driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
# search_confirm_button = driver.find_element(By.CSS_SELECTOR, "[data-cy='search.submit-form.default']")
# driver.find_element(By.ID, "location").click()
# search_place_input = driver.find_element(By.CSS_SELECTOR, "[data-cy='location-picker-input']")
# search_place_input.send_keys("Orunia")
