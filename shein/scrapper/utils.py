import logging
import re
from datetime import datetime

import chromedriver_autoinstaller
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from shein.constants import DATABASE_URL, DEBUG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def included_in_string(string: str, word_list: list[str]) -> bool:
    """Check if any word in the list is in the string.

    Parameters
    ----------
        string (str): The string to check
        word_list (List[str]): The list of words to check
    Returns:
        bool: True if any word in the list is in the string, False otherwise
    """
    for word in word_list:
        if word in string:
            return True
    return False


def get_driver() -> webdriver.Chrome:
    """Get a headless Selenium driver.

    Returns
    -------
        webdriver.Chrome: Selenium driver
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    chromedriver_autoinstaller.install()

    # driver = webdriver.Remote(
    # command_executor="http://localhost:4444/wd/hub",
    # desired_capabilities={},
    # options=options
    # )

    driver = webdriver.Chrome()
    driver.delete_all_cookies()
    return driver


def get_max_pagination(driver: webdriver.Chrome, url: str) -> int:
    """
    Get the maximum number of pages for a category.

    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium driver
    url : str
        The category

    Returns
    -------
    int
        The maximum number of pages
    """
    driver.get(url)
    max_pages = 1

    if not DEBUG:
        pagination_text = driver.find_element(By.CLASS_NAME, "sui-pagination__total").text
        pagination_number = re.findall(r"\b\d{1,2}\b", pagination_text)

        max_pages = int(pagination_number[0])
        logger.info("Found %s pages", max_pages)

    return max_pages


def write_in_database(parent_url: str, product_urls: list[str]) -> None:
    """
    Write the product URLs in MongoDB.

    Parameters
    ----------
    parent_url : str
        The parent URL
    product_urls : List[str]
        The product URLs
    """
    MONGO_CLIENT = MongoClient(DATABASE_URL)
    DATABASE = MONGO_CLIENT["shein"]
    COLLECTION = DATABASE["product_urls"]

    try:
        COLLECTION.create_index("url", unique=True)
        logger.info("Index created")
    except Exception as e:
        logger.warning("Index already exists")
        logger.exception(e)

    for cleaned_url in product_urls:
        if COLLECTION.find_one({"url": cleaned_url}):
            logger.exception("URL already exists in MongoDB")

        logger.info("Adding " + cleaned_url + " to MongoDB")
        COLLECTION.insert_one(
            {"url": cleaned_url, "parent_url": parent_url, "status": "pending", "timestamp": datetime.now()}
        )

    MONGO_CLIENT.close()
