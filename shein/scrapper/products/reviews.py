import logging
import time
from datetime import datetime

from pymongo.database import Database
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from shein.constants import COLLECTION_REVIEWS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_reviews(driver: webdriver.Chrome, mongo_database: Database, product_id: str) -> None:
    """
    Process the reviews.

    Parameters
    ----------
    driver : webdriver.Chrome
        Selenium driver
    mongo_database : Database
        The MongoDB database
    product_id : str
        The product ID
    """
    pagination_disabled = "disabled" in driver.find_element(By.CLASS_NAME, "sui-pagination__next").get_attribute(
        "class"
    )
    while not pagination_disabled:
        time.sleep(1)
        reviews = driver.find_elements(By.CLASS_NAME, "j-expose__common-reviews__list-item")
        for review in reviews:
            nickname = review.find_element(By.CLASS_NAME, "nikename").get_property("innerText")
            date = review.find_element(By.CLASS_NAME, "bottom-container").get_property("innerText")
            rating = review.find_element(By.CLASS_NAME, "rate-star").get_attribute("aria-label").replace("Rating", "")
            review = review.find_element(By.CLASS_NAME, "rate-des").get_property("innerText")

            review_data = {
                "date": date,
                "rating": int(rating),
                "review": review,
                "nickname": nickname,
                "product_id": product_id,
                "timestamp": datetime.now(),
            }
            collection = mongo_database[COLLECTION_REVIEWS]
            collection.insert_one(review_data)

        next_page = driver.find_element(By.CLASS_NAME, "sui-pagination__next")
        ActionChains(driver).move_to_element(next_page).click(next_page).perform()

        pagination_disabled = "disabled" in driver.find_element(By.CLASS_NAME, "sui-pagination__next").get_attribute(
            "class"
        )
