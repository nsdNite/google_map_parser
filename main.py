import csv
import time
from dataclasses import dataclass, fields, astuple

import logging
import re
from datetime import datetime
from typing import Optional


from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# Settings
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
}
SEARCH_STRING = "grocery store macau"
BASE_URL = "https://www.google.com/maps"


class WebDriverSingleton:
    instance: Optional[webdriver.Chrome] = None
    options: Options = Options()

    @classmethod
    def get_instance(cls) -> webdriver.Chrome:
        if cls.instance is None:
            cls.options.add_argument("--window-size=1200x600")
            #  cls.options.add_argument("--headless")
            cls.instance = webdriver.Chrome(options=cls.options)

        return cls.instance


@dataclass
class Store:
    name: str
    url_map: str
    category: str
    address: str
    phone: None | str
    website: None | str


CSV_FIELDS = [field.name for field in fields(Store)]


def get_urls_for_places() -> [str]:
    driver = WebDriverSingleton.get_instance()
    driver.get(BASE_URL)
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(SEARCH_STRING)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    result_element = driver.find_element(By.CLASS_NAME, "fontTitleLarge")
    print(result_element.text)
    webdriver.ActionChains(driver).move_to_element(result_element).click().perform()
    counter = 0

    while counter <= 10:
        webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        counter += 1

    href_blocks = driver.find_elements(By.XPATH, "//a[@aria-label]")[1:-1]

    return [href.get_attribute("href") for href in href_blocks]


def get_category() -> str:
    driver = WebDriverSingleton.get_instance()

    try:
        category = driver.find_element(By.XPATH, "//span/button").text
    except NoSuchElementException as e:
        category = "Unknown or Closed Forever"

    return category


def get_name() -> str:
    driver = WebDriverSingleton.get_instance()

    return driver.find_element(By.XPATH, "//h1").text


def get_address_with_regex(info: str) -> str:
    pattern = r"\|([^\|]+)\|"

    return re.findall(pattern, info)[0]


def get_phone_with_regex(info: str) -> str:
    pattern = r"\|\+(.+?)\|"
    try:
        phone = re.findall(pattern, info)[0]
    except IndexError:
        phone = "Unknown"

    return phone


def get_website() -> str:
    driver = WebDriverSingleton.get_instance()

    try:
        website = driver.find_element(By.XPATH, "//a[@data-item-id='authority']").text
    except NoSuchElementException as e:
        website = "Unknown"

    return website


def parse_single_instance(url: str) -> Store:
    driver = WebDriverSingleton.get_instance()

    driver.get(url)

    info_block = "|".join(
        [
            info.text
            for info in driver.find_elements(
                By.XPATH, "//button//div[contains(@class, 'fontBodyMedium')]"
            )
        ]
    )

    name = get_name()
    category = get_category()
    address = get_address_with_regex(info_block)
    phone = get_phone_with_regex(info_block)
    website = get_website()

    return Store(
        name=name,
        url_map=url,
        category=category,
        address=address,
        phone=phone,
        website=website,
    )


def csv_output(stores: [Store], csv_name: str) -> None:
    filename = csv_name + ".csv"

    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_FIELDS)
        writer.writerows([astuple(store) for store in stores])
        logging.info(
            f"Wrote {len(results)} instances to {filename}. "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )


if __name__ == "__main__":
    results = []
    csv_name = "stores"
    chrome_driver = WebDriverSingleton.get_instance()

    with chrome_driver as session:
        urls = get_urls_for_places()
        for url in urls:
            results.append(parse_single_instance(url))

    csv_output(results, csv_name)
