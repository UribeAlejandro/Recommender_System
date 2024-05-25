import os

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
DATABASE_URL = f"mongodb://{MONGO_HOST}:27017/"
DATABASE_NAME = "shein"
COLLECTION_URLS = "product_urls"
COLLECTION_DETAILS = "product_details"
COLLECTION_REVIEWS = "product_reviews"
IMG_DIRECTORY = "img/products"
ROW_SIZE = 5
