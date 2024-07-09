from scraper.constants import COLLECTION_INDEX, DATABASE_NAME
from scraper.shein.products.details import get_details
from scraper.shein.products.images import download_images
from scraper.shein.products.list import list_products
from scraper.shein.utils.database import (
    clean_price_column,
    create_collection_index,
    get_categories,
    get_mongo_database,
)
from scraper.shein.utils.driver import get_driver

if __name__ == "__main__":
    driver = get_driver()
    mongo_database = get_mongo_database(DATABASE_NAME)
    create_collection_index(mongo_database, COLLECTION_INDEX)

    list_products(driver, mongo_database)
    get_details(driver, mongo_database)
    driver.close()

    download_images(mongo_database)
    clean_price_column(mongo_database)
    get_categories(mongo_database)

    mongo_database.client.close()
