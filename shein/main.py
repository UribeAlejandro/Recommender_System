from shein.constants import COLLECTION_INDEX, DATABASE_NAME
from shein.scrapper.products.details import get_details
from shein.scrapper.products.list import list_products
from shein.scrapper.utils.database import create_collection_index, get_mongo_database
from shein.scrapper.utils.scraper import get_driver

if __name__ == "__main__":
    driver = get_driver()
    mongo_database = get_mongo_database(DATABASE_NAME)
    create_collection_index(mongo_database, COLLECTION_INDEX)

    list_products(driver, mongo_database)
    get_details(driver, mongo_database)

    driver.close()
    mongo_database.client.close()
