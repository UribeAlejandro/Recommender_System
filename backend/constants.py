import os

DATABASE_NAME = "shein"
COLLECTION_DETAILS = "product_details"
COLLECTION_REVIEWS = "product_reviews"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://database:27017")
