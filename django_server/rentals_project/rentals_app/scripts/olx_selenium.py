from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def get_offers_olx(district, town):
    CHROME_DRIVER_PATH = "C:/Users/dmars/Documents/PRACA_INZYNIERSKA/project_python/django_server/rentals_project/rentals_app/scripts/chromedriver.exe"
    options = ChromeOptions()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1230,800')
    options.add_argument('--disable-gpu')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    selenium_service = Service(CHROME_DRIVER_PATH)
    driver_olx = webdriver.Chrome(service=selenium_service, options=options)
    wait = WebDriverWait(driver_olx, 10)

    driver_olx.get("https://www.olx.pl/nieruchomosci/mieszkania/wynajem/")
    wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()
    time.sleep(3)
    search_input = driver_olx.find_element(By.ID, "location-input")

    search_input.click()
    search_input.send_keys(F"{district} {town}")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='suggestion-item']"))).click()
    time.sleep(2)
    offer_list = driver_olx.find_element(By.CSS_SELECTOR, "[data-testid='listing-grid']")
    offers = offer_list.find_elements(By.CSS_SELECTOR, "[data-cy='l-card']")
    info = []
    for offer in offers:
        link_el = offer.find_element(By.TAG_NAME, "a")
        link = link_el.get_attribute("href")
        if "otodom" in link:
            continue
        driver_olx.switch_to.new_window("tab")
        driver_olx.get(link)

        price_element = driver_olx.find_element(By.CSS_SELECTOR, "[data-testid='ad-price-container']")
        price = price_element.find_element(By.TAG_NAME, "h3").text
        price = get_the_price(price)
        offer_details = driver_olx.find_element(By.CLASS_NAME, "css-sfcl1s")
        try:
            image_link = driver_olx.find_element(By.CLASS_NAME, "css-1bmvjcs").get_attribute("src")
        except:
            image_link = "N/A"
        offer_elements = offer_details.find_elements(By.TAG_NAME, "p")
        for offer_tag in offer_elements:
            if "Powierzchnia" in offer_tag.text:
                surface = get_the_surface_olx(offer_tag.text)
            if "Czynsz" in offer_tag.text:
                rent = get_the_rent_olx(offer_tag.text)
            if "pokoi" in offer_tag.text:
                num_of_rooms = get_the_rooms_olx(offer_tag.text)
        info.append({"address": F"{district}, {town}",
                     "surface": surface, "price": price, "rent": rent, "rooms": num_of_rooms,
                     "link": link, "image_link": image_link, "website": "olx"})
        driver_olx.close()
        driver_olx.switch_to.window(driver_olx.window_handles[0])
    driver_olx.quit()
    return info


def get_the_price(price_text):
    split_price = price_text.replace(",", ".").split(" ")
    if len(split_price) > 2:
        return int(float(split_price[0] + split_price[1]))
    return int(float(split_price[0]))


def get_the_surface_olx(surface_text):
    split_surface = surface_text.replace(",", ".").split(" ")
    return int(float(split_surface[1]))


def get_the_rooms_olx(num_of_rooms_text):
    split_rooms = num_of_rooms_text.split(" ")
    if "Kawalerka" in split_rooms[2]:
        return 1
    return int(split_rooms[2])


def get_the_rent_olx(rent_text):
    split_rent = rent_text.replace(",", ".").split(" ")
    if len(split_rent) == 5:
        return int(float(split_rent[2] + split_rent[3]))
    return int(float(split_rent[2]))
