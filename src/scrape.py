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


class MdComputers:
        def __init__(self, driver):
                self.STORE_URL = 'https://mdcomputers.in'
                self.driver = driver

        def get_product_url(self, product_name) -> str:
                driver.get(self.STORE_URL)
                search_elem = driver.find_element_by_name('search')
                search_elem.clear()
                search_elem.send_keys(product_name)
                try:
                        # waits 7 seconds for dropdown
                        dropdown_elem = WebDriverWait(driver, 7).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'media'))
                        )
                        anchor = dropdown_elem.find_element_by_tag_name('a')
                        return anchor.get_attribute('href')
                except:
                        return f"Product doesn't exist on {self.STORE_URL}"
                finally:
                        driver.close()

        def get_product_price(self, product_url) -> str:
                driver.get(product_url)
                price_elem = driver.find_element_by_id('price-special')
                return price_elem.text

        def get_product_rating(self, product_url) -> str:
                driver.get(product_url)
                rating_elem = driver.find_element_by_class_name('rating-box')
                stars = rating_elem.find_elements_by_tag_name('span')
                filled_stars = [star for star in stars if star.find_element_by_tag_name('i').
                                get_attribute('class') == 'fa fa-star fa-stack-1x']
                return len(filled_stars)


class VedantComputers:
        def __init__():
                self.STORE_URL = 'https://vedantcomputers.com'

        def get_product_url(self, product_name):
                pass

        def get_product_price(self, product_name):
                pass

        def get_product_rating(self, product_name):
                pass


class TheITDepot:
        def __init__():
                self.STORE_URL = 'https://theitdepot.com'

        def get_product_url(self, product_name):
                pass

        def get_product_price(self, product_name):
                pass

        def get_product_rating(self, product_name):
                pass


class PrimeABGB:
        def __init__():
                self.STORE_URL = 'https://primeabgb.com'

        def get_product_url(self, product_name):
                pass

        def get_product_price(self, product_name):
                pass

        def get_product_rating(self, product_name):
                pass


class Amazon:
        def __init__():
                self.STORE_URL = 'https://amazon.in'

        def get_product_url(self, product_name):
                pass

        def get_product_price(self, product_name):
                pass

        def get_product_rating(self, product_name):
                pass


class Flipkart:
        def __init__():
                self.STORE_URL = 'https://flipkart.com'

        def get_product_url(self, product_name):
                pass

        def get_product_price(self, product_name):
                pass

        def get_product_rating(self, product_name):
                pass


if __name__ == '__main__':
        # Disable image loading
        SEARCH_TERM = 'Ryzen 7 5800X'
        profile = webdriver.FirefoxProfile()
        profile.set_preference('permissions.default.image', 2)
        options = Options()
        # options.headless = True
        driver = webdriver.Firefox(options=options, firefox_profile=profile)

        mdcomp = MdComputers(driver)
        # print(mdcomp.get_product_url(SEARCH_TERM))
        # print(mdcomp.get_product_price('https://mdcomputers.in/amd-ryzen-7-5800x-100-100000063wof.html'))
        # print(mdcomp.get_product_rating('https://mdcomputers.in/amd-dual-core-athlon-200ge.html'))
