# Standard library imports
import re
import json
import time
import csv
from datetime import datetime
import time
# Third-party imports for data handling
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from contextlib import contextmanager

# Third-party imports for concurrent execution
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party imports for web scraping with Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Local application/library specific imports
import params


def setup_driver():
    """Configura el driver de Selenium con opciones para Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

@contextmanager
def webdriver_context():
    driver = setup_driver()
    try:
        yield driver
    finally:
        driver.quit()

def wait_for_elements(driver, selector, timeout=params.TIMEOUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
