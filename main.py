from dataclasses import dataclass
import logging
import re
from typing import Optional


import requests
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Making selenium singleton


class WebDriverSingleTone:
    instance: Optional[webdriver.Chrome] = None
    options: Options = Options()

    @classmethod
    def get_instance(cls) -> webdriver.Chrome:
        if cls.instance is None:
            cls.options.add_argument("--headless")
            cls.instance = webdriver.Chrome(options=cls.options)

        return cls.instance
