from dataclasses import dataclass
import logging
import re
from typing import Optional


import requests
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# settings:

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
}


SEARCH_STRING = "grocery store macau"

URL = "https://www.google.com/maps"


# Making selenium singleton
class WebDriverSingleton:
    instance: Optional[webdriver.Chrome] = None
    options: Options = Options()

    @classmethod
    def get_instance(cls) -> webdriver.Chrome:
        if cls.instance is None:
            cls.options.add_argument("--headless")
            cls.instance = webdriver.Chrome(options=cls.options)

        return cls.instance


class Store:
    name: str
    rating: float
    address: str
    website: None | str
    phone: None | str
    geotag: str


# 1
def enter_search_string(driver: webdriver.Chrome, search_string: str) -> None:
    pass


# 2
def scroll_down(driver: webdriver.Chrome) -> str:
    pass
    # scroll until "no results" appears, then return html plain


# 3
def get_html_from_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as error:
        print("An error has occurred:", error)
        raise

    return response.text


# 4
def parse_single_instance(page: str) -> Store:
    pass
    # collect instances with every html


if __name__ == "__main__":
    chrome_driver = WebDriverSingleton.get_instance()
    with chrome_driver as session:
        pass
