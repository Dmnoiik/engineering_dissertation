from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time



def get_offers_otodom(district, town):
    CHROME_DRIVER_PATH = "C:/Users/dmars/Documents/PRACA_INZYNIERSKA/project_python/django_server/rentals_project/rentals_app/scripts/chromedriver.exe"
    chrome_options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1230,800')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    selenium_service = Service(CHROME_DRIVER_PATH)
    options = chrome_options
    driver_otodom = webdriver.Chrome(service=selenium_service, options=options)
    driver_otodom.get("https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/cala-polska")
    driver_otodom.find_element(By.ID, "onetrust-accept-btn-handler").click()
    search_confirm_button = driver_otodom.find_element(By.CSS_SELECTOR, "[data-cy='search.submit-form.default']")
    driver_otodom.find_element(By.ID, "location").click()
    search_place_input = driver_otodom.find_element(By.CSS_SELECTOR, "[data-cy='location-picker-input']")

    search_place_input.send_keys(f"{district} {town}")
    time.sleep(0.5)
    suggestion_item = driver_otodom.find_element(By.CSS_SELECTOR, "[data-cy='checkboxButton']")
    suggestion_item.click()
    search_confirm_button.click()

    time.sleep(0.8)
    all_offers = driver_otodom.find_elements(By.CSS_SELECTOR,
                                             "[data-cy='search.listing.organic'] [data-cy='listing-item']")
    info = []
    for offer in all_offers:
        article_element = offer.find_element(By.TAG_NAME, "article")
        offer_title = offer.find_element(By.CSS_SELECTOR, "[data-cy='listing-item-title']").text
        offer_link = offer.find_element(By.CLASS_NAME, "e1dfeild2").get_attribute("href")
        offer_id = offer_link.split("-")[-1]
        price, num_of_rooms, surface = article_element.find_elements(By.CLASS_NAME, "ei6hyam2")
        price, num_of_rooms, surface = price.text, num_of_rooms.text, surface.text
        surface = get_the_surface_otodom(surface)
        price = get_the_price(price)
        image_link = offer.find_element(By.CLASS_NAME, "e10oxrv20").get_attribute("src")
        num_of_rooms = int(num_of_rooms.split(" ")[0])
        rent = article_element.find_element(By.CLASS_NAME, "ei6hyam4").text
        try:
            rent = int(rent.split(" ")[2])
        except:
            rent = -1
        address = article_element.find_element(By.CSS_SELECTOR, "div + p").text
        info.append({"title": offer_title, "address": address,
                     "surface": surface, "price": price, "rent": rent, "rooms": num_of_rooms,
                     "link": offer_link, "image_link": image_link, "website": "otodom", "offer_id": offer_id})
    driver_otodom.quit()
    return info


def get_the_price(price_text):
    split_price = price_text.replace(",", ".").split(" ")
    if len(split_price) > 2:
        return int(float(split_price[0] + split_price[1]))
    return int(float(split_price[0]))


def get_the_surface_otodom(surface_text):
    split_surface = surface_text.replace(",", ".").split(" ")
    return int(float(split_surface[0]))


