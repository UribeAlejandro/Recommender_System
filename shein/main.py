from selenium.webdriver.common.by import By

from shein.constants import COLLECTION_DETAILS, DATABASE_NAME
from shein.scrapper.utils.database import get_mongo_database
from shein.scrapper.utils.scraper import get_driver

if __name__ == "__main__":
    driver = get_driver()
    mongo_database = get_mongo_database(DATABASE_NAME)
    product_details_collection = mongo_database[COLLECTION_DETAILS]
    pending_urls = product_details_collection.find({"cateogries": {"$exists": False}})

    for url in pending_urls:
        url = url["url"]

        try:
            driver.get(url)
            s = driver.find_element(By.CLASS_NAME, "bread-crumb__inner").get_attribute("innerText")
            s = s.replace("\n", "").split("/")[1:-1]

            product_details_collection.update_one({"url": url}, {"$set": {"cateogries": s}})

        except Exception as e:
            print(e)

    driver.close()

    # download_images(mongo_database)
    # clean_price_column(mongo_database)

    mongo_database.client.close()
