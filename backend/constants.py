import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = "shein-mirror"
COLLECTION_DETAILS = "product_details"
COLLECTION_REVIEWS = "product_reviews"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://database:27017")
