import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_TERM = 'Ryzen 5 3600X'
URL = 'https://mdcomputers.in'

options = Options()
# options.headless = True

driver = webdriver.Firefox(options=options)


def get_product_url(product):
        driver.get(URL)

        search_elem = driver.find_element_by_name('search')
        search_elem.send_keys(product)

        try:
                # waits 5 seconds for dropdown
                dropdown_elem = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'media'))
                )
                anchor = dropdown_elem.find_element_by_tag_name('a')
                return anchor.get_attribute('href')
        except:
                return "Product doesn't exist on mdcomputers.in"
        finally:
                driver.close()


print(get_product_url(SEARCH_TERM))
