import json
import logging
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By

from shein.constants import BLACKLISTED_WORDS, DOMAIN, PATH_OUT_JSON, URLS, USE_DB
from shein.scrapper.utils import get_driver, get_max_pagination, included_in_string, write_in_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_pages(driver: webdriver.Chrome, max_pages: int, url: str) -> list[str]:
    """
    Process the pages of a category.

    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium driver
    max_pages : int
        The maximum number of pages
    url : str
        The category

    Returns
    -------
    List[str]
        The product URLs
    """
    product_urls = []
    for i in range(1, max_pages + 1):
        try:
            logger.info("Processing page %s of %s", i, max_pages)
            driver.get(url + "&page=" + str(i))

            products_section = driver.find_element(By.CLASS_NAME, "product-list-v2__container")
            product_elements = products_section.find_elements(By.CLASS_NAME, "product-list__item")
            for product in product_elements:
                href = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                if not href or included_in_string(href, BLACKLISTED_WORDS):
                    logger.info("Skipping %s", href)

                parsed_url = urlparse(href)
                cleaned_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                if DOMAIN in parsed_url.netloc and cleaned_url not in product_urls:
                    product_urls.append(cleaned_url)
        except Exception as e:
            logger.exception("Error processing page: %s", str(e))
            continue

    return product_urls


def run() -> None:
    """Extract product URLs from categories."""
    driver = get_driver()

    for i, url in enumerate(URLS):
        url = url.strip()
        logger.info("Processing %s", url)

        max_pages = get_max_pagination(driver, url)
        product_urls = process_pages(driver, max_pages, url)

        if USE_DB:
            write_in_database(url, product_urls)
        else:
            products = {"parent_url": url, "product_urls": product_urls}
            with open(f"{i}-{PATH_OUT_JSON}", "w") as outfile:
                json.dump(products, outfile)

    driver.quit()
