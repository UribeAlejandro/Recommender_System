from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def included_in_string(string, word_list):
    """Check if any word in the list is in the string."""
    for word in word_list:
        if word in string:
            return True
    return False


def get_driver():
    """Get a headless Firefox driver."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={}, options=options)
    driver.delete_all_cookies()
    return driver
