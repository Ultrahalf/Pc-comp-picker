import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class MDComputers:

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
        self.driver.get(product_url)
        try:
            price_elem = self.driver.find_element_by_id('price-special')
        except NoSuchElementException:
            price_elem = self.driver.find_element_by_id('price-old')
        return price_elem.text

    def get_product_rating(self, product_url) -> str:
        self.driver.get(product_url)
        rating_elem = self.driver.find_element_by_class_name('rating-box')
        stars = rating_elem.find_elements_by_tag_name('span')
        filled_stars = [star for star in stars if star.find_element_by_tag_name('i').
                    get_attribute('class') == 'fa fa-star fa-stack-1x']
        return len(filled_stars)


class VedantComputers:

    def __init__(self, driver):
        self.STORE_URL = 'https://vedantcomputers.com'
        self.driver = driver

    def get_product_url(self, product_name):
        pass

    def get_product_price(self, product_url) -> str:
        self.driver.get(product_url)
        try:
            price_elem = self.driver.find_element_by_class_name('product-price-new')
        except NoSuchElementException:
            price_elem = self.driver.find_element_by_class_name('product-price')
        return price_elem.text

    def get_product_rating(self, product_url) -> str:
        self.driver.get(product_url)
        product_elem = self.driver.find_element_by_id('product')
        rating_elem = product_elem.find_element_by_class_name('rating-stars')
        stars = rating_elem.find_elements_by_tag_name('span')
        filled_stars = [star for star in stars if star.find_element_by_tag_name('i').
                get_attribute('class') == 'fa fa-star fa-stack-1x']
        return len(filled_stars)


class TheITDepot:

    def __init__(self, driver):
        self.STORE_URL = 'https://theitdepot.com'
        self.driver = driver

    def get_product_url(self, product_name):
        pass

    def get_product_price(self, product_url) -> str:
        self.driver.get(product_url)
        page_elem = self.driver.find_element_by_id('Product')
        price_elem = page_elem.find_element_by_class_name('col-md-12')
        price_elem = price_elem.find_element_by_class_name('font-weight-bold')
        return price_elem.text

    def get_product_rating(self, product_url) -> str:
        self.driver.get(product_url)
        rating_elem = self.driver.find_element_by_css_selector('span[itemprop="ratingValue"]')
        if rating_elem.text == 'No ratings':
            return 0
        else:
            return rating_elem.text


class PrimeABGB:

    def __init__(self, driver):
        self.STORE_URL = 'https://primeabgb.com'
        self.driver = driver

    def get_product_url(self, product_name):
        pass

    def get_product_price(self, product_url) -> str:
        self.driver.get(product_url)
        price_elem = self.driver.find_element_by_class_name('price')
        price_elem = price_elem.find_element_by_tag_name('ins')
        return price_elem.text

    def get_product_rating(self, product_url) -> str:
        self.driver.get(product_url)
        try:
            rating_elem = self.driver.find_element_by_css_selector('div[class="star-rating"]')
            rating_string = rating_elem.get_attribute('aria-label')
            return rating_string.split()[1]
        except NoSuchElementException:
            return 0


class Amazon:

    def __init__(self, driver):
        self.STORE_URL = 'https://amazon.in'
        self.driver = driver

    def get_product_url(self, product_name):
        pass

    def get_product_price(self, product_url):
        self.driver.get(product_url)
        try:
            price_elem = self.driver.find_element_by_id('priceblock_ourprice')
        except NoSuchElementException:
            return "Out of stock"
        return price_elem.text

    def get_product_rating(self, product_url):
        self.driver.get(product_url)
        try:
            rating_elem = self.driver.find_element_by_css_selector('span[data-hook="rating-out-of-text"]')
            return rating_elem.text
        except NoSuchElementException:
            return 0
