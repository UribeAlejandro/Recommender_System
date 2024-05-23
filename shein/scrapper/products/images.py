import logging
import os
from copy import copy

import requests
from pymongo.database import Database

from shein.constants import COLLECTION_DETAILS, IMAGE_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def __download_image(url: str, download_path: str) -> None:
    """
    Download an image.

    Parameters
    ----------
    url : str
        The image URL
    download_path : str
        The download path
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img_data = requests.get(url).content
        with open(download_path, "wb") as handler:
            handler.write(img_data)
    except (OSError, requests.RequestException) as e:
        logger.info("Error downloading %s: %s", url, e)


def download_images(mongo_database: Database) -> None:
    """
    Download the images for the products.

    Parameters
    ----------
    mongo_database : Database
        The MongoDB database
    """
    product_details = mongo_database[COLLECTION_DETAILS]
    products = product_details.find({"image_path": "pending"})
    os.makedirs(IMAGE_DIR, exist_ok=True)

    n_images = int(len(list(copy(products))))

    logger.info("Downloading %s images", n_images)

    for product in products:
        image_url = copy(product["image_url"])
        download_path = os.path.join(IMAGE_DIR, image_url.split("/")[-1])
        __download_image(image_url, download_path)

        product_details.update_one(filter={"_id": product["_id"]}, update={"$set": {"image_path": download_path}})
