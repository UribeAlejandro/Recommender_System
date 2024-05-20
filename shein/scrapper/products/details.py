import logging
from datetime import datetime

from pymongo.database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By

from shein.constants import COLLECTION_DETAILS, COLLECTION_URLS
from shein.scrapper.products.reviews import process_reviews

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_details(driver: webdriver.Chrome, mongo_database: Database) -> None:
    """
    Get the product details.

    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium driver
    mongo_database : Database
        The MongoDB database
    """
    products_collection = mongo_database[COLLECTION_URLS]
    product_details_collection = mongo_database[COLLECTION_DETAILS]

    pending_urls = products_collection.find({"status": "pending"}).sort("timestamp", 1)

    for url in pending_urls:
        url = url["url"]
        logger.info("Processing: %s", url)

        try:
            products_collection.update_one({"url": url}, {"$set": {"status": "processing"}})
            driver.get(url)

            element_image = driver.find_element(By.CLASS_NAME, "crop-image-container")

            text_image_url = element_image.find_element(By.TAG_NAME, "img").get_attribute("src")
            text_title = driver.find_element(By.CLASS_NAME, "product-intro__head-name").text
            text_product_id = driver.find_element(By.CLASS_NAME, "product-intro__head-sku").text.replace("SKU: ", "")

            product_data = {
                "url": url,
                "title": text_title,
                "image_url": text_image_url,
                "last_update": datetime.now(),
                "product_id": text_product_id,
            }

            product_details_collection.insert_one(product_data)
            process_reviews(driver, mongo_database, text_product_id)
            products_collection.update_one({"url": url}, {"$set": {"status": "done"}})
        except Exception as e:
            logger.error("Error processing: %s", url)
            logger.exception("%s", str(e))
            products_collection.update_one({"url": url}, {"$set": {"status": "failed"}})
