import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_TERM = 'Ryzen 7 5800X'
URL = 'https://mdcomputers.in'

# Disable image loading
profile = webdriver.FirefoxProfile()
profile.set_preference('permissions.default.image', 2)

options = Options()
# options.headless = True
driver = webdriver.Firefox(options=options, firefox_profile=profile)


def get_product_url(product) -> str:
        driver.get(URL)
        search_elem = driver.find_element_by_name('search')
        search_elem.clear()
        search_elem.send_keys(product)
        try:
                # waits 7 seconds for dropdown
                dropdown_elem = WebDriverWait(driver, 7).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'media'))
                )
                anchor = dropdown_elem.find_element_by_tag_name('a')
                return anchor.get_attribute('href')
        except:
                return "Product doesn't exist on mdcomputers.in"
        finally:
                driver.close()


def get_product_price(product_url) -> str:
        driver.get(product_url)
        price_elem = driver.find_element_by_id('price-special')
        return price_elem.text


def get_product_rating(product_url) -> str:
        driver.get(product_url)
        rating_elem = driver.find_element_by_class_name('rating-box')
        stars = rating_elem.find_elements_by_tag_name('span')
        return len(stars)


if __name__ == '__main__':
        # print(get_product_url(SEARCH_TERM))
        # print(get_product_price('https://mdcomputers.in/amd-ryzen-7-5800x-100-100000063wof.html'))
        print(get_product_rating('https://mdcomputers.in/amd-ryzen-7-5800x-100-100000063wof.html'))
