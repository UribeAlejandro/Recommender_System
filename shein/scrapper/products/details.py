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

    pending_urls = products_collection.find({"status": "pending"})

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
            text_price = driver.find_element(By.CLASS_NAME, "ProductIntroHeadPrice").text
            element_description = driver.find_elements(By.CLASS_NAME, "product-intro__description-table-item")
            categories = driver.find_element(By.CLASS_NAME, "bread-crumb__inner").get_attribute("innerText")
            categories = categories.replace("\n", "").split("/")[1:-1]

            description = {
                item.get_property("innerText").split(":")[0].lower().strip(): item.get_property("innerText")
                .split(":")[1]
                .lower()
                .strip()
                for item in element_description
            }

            product_data = {
                "url": url,
                "title": text_title,
                "image_path": "pending",
                "image_url": text_image_url,
                "last_update": datetime.now(),
                "product_id": text_product_id,
                "description_items": description,
                "price": text_price,
                "categories": categories,
            }

            product_details_collection.insert_one(product_data)
            process_reviews(driver, mongo_database, text_product_id)
            products_collection.update_one({"url": url}, {"$set": {"status": "complete"}})
        except Exception as e:
            logger.error("Error processing: %s", url)
            logger.exception("%s", str(e))
            products_collection.update_one({"url": url}, {"$set": {"status": "failed"}})
