import logging
from datetime import datetime

from pymongo.database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def wait_for_review_image_load(driver: webdriver.Chrome, image_element: WebElement, timeout: int = 15) -> None:
    """
    Wait for the review image to load.

    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium driver
    image_element : WebElement
        The image element
    timeout : int (default: 15)
        Time to wait for the image to load
    """
    WebDriverWait(driver, timeout).until_not(lambda d: "sheinsz.ltwebstatic.com" in image_element.get_attribute("src"))


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
    URL_COLLECTION = mongo_database["product_urls"]
    PRODUCT_COLLECTION = mongo_database["products"]
    pending_urls = URL_COLLECTION.find({"status": "pending"}).sort("timestamp", 1)

    for url in pending_urls:
        url = url["url"]
        logger.info("Processing: %s", url)

        try:
            URL_COLLECTION.update_one({"url": url}, {"$set": {"status": "processing"}})
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

            PRODUCT_COLLECTION.insert_one(product_data)
        except Exception as e:
            logger.error("Error processing: %s", url)
            logger.exception("%s", str(e))
            URL_COLLECTION.update_one({"url": url}, {"$set": {"status": "failed"}})
