import json
import logging
import re
from datetime import datetime
from urllib.parse import urlparse

from pymongo import MongoClient
from selenium.webdriver.common.by import By

from shein.constants import BLACKLISTED_WORDS, DATABASE_URL, DEBUG, DOMAIN, URLS, USE_DB
from shein.scrapper.utils import get_driver, included_in_string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_list():
    """Extract URLs from file."""
    with open(URLS) as file:
        urls = file.readlines()
    return urls


def run():
    """Extract product URLs from categories."""
    if USE_DB:
        MONGO_CLIENT = MongoClient(DATABASE_URL)
        DATABASE = MONGO_CLIENT["shein"]
        COLLECTION = DATABASE["product_urls"]
        try:
            COLLECTION.create_index("url", unique=True)
            logger.info("Index created")
        except Exception:
            logger.warning("Index already exists")

    driver = get_driver()
    urls = extract_list()
    for j, url in enumerate(urls):
        url = url.strip()
        print("Processing " + url)

        driver.get(url)

        try:
            pagination_text = driver.find_element(By.CLASS_NAME, "sui-pagination__total").text
            pagination_number = re.sub("\D", "", pagination_text)
            max_pages = int(pagination_number)
            if DEBUG:
                max_pages = min(1, max_pages)  # Limit to 1 page in debug mode
            logger.info("Found %spages", max_pages)
        except Exception as e:
            print("Error getting pagination: " + str(e))
            max_pages = 1  # If no pagination, assume 1 page of product
            pass

        for i in range(1, max_pages + 1):
            product_urls = []
            try:
                print(f"Processing page {i} of {max_pages}")  # Progress update
                driver.get(url + "?page=" + str(i))
                # driver.get(url)

                product_elements = driver.find_elements(By.CLASS_NAME, "product-list__item")
                for product in product_elements:
                    href = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if not href or included_in_string(href, BLACKLISTED_WORDS):
                        logger.info("Skipping %s", href)

                    parsed_url = urlparse(href)
                    cleaned_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                    if DOMAIN in parsed_url.netloc and cleaned_url not in product_urls:
                        try:
                            if USE_DB:
                                if COLLECTION.find_one({"url": cleaned_url}):
                                    print("URL already exists in MongoDB")
                                    continue
                                print("Adding " + cleaned_url + " to MongoDB")
                                COLLECTION.insert_one(
                                    {"url": cleaned_url, "status": "pending", "timestamp": datetime.now()}
                                )
                            else:
                                product_urls.append(cleaned_url)
                        except Exception as e:
                            print("Error adding URL to MongoDB: " + str(e))
                            pass
            except Exception as e:
                print("Error processing page: " + str(e))
                continue

            if not USE_DB:
                print("Writing to JSON file")
                with open(f"product_urls-{j}-{i}.json", "w") as outfile:
                    json.dump(product_urls, outfile)

    driver.quit()
    if USE_DB:
        MONGO_CLIENT.close()
