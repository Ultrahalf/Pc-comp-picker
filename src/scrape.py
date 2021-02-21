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
                driver.get(product_url)
                try:
                        price_elem = driver.find_element_by_id('price-special')
                except NoSuchElementException:
                        price_elem = driver.find_element_by_id('price-old')
                return price_elem.text

        def get_product_rating(self, product_url) -> str:
                driver.get(product_url)
                rating_elem = driver.find_element_by_class_name('rating-box')
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
                driver.get(product_url)
                try:
                        price_elem = driver.find_element_by_class_name('product-price-new')
                except NoSuchElementException:
                        price_elem = driver.find_element_by_class_name('product-price')
                return price_elem.text

        def get_product_rating(self, product_url) -> str:
                driver.get(product_url)
                product_elem = driver.find_element_by_id('product')
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
                driver.get(product_url)
                page_elem = driver.find_element_by_id('Product')
                price_elem = page_elem.find_element_by_class_name('col-md-12')
                price_elem = price_elem.find_element_by_class_name('font-weight-bold')
                return price_elem.text

        def get_product_rating(self, product_url) -> str:
                driver.get(product_url)
                rating_elem = driver.find_element_by_css_selector('span[itemprop="ratingValue"]')
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
                driver.get(product_url)
                price_elem = driver.find_element_by_class_name('price')
                price_elem = price_elem.find_element_by_tag_name('ins')
                return price_elem.text

        def get_product_rating(self, product_url) -> str:
                driver.get(product_url)
                try:
                        rating_elem = driver.find_element_by_css_selector('div[class="star-rating"]')
                        return rating_elem.get_attribute('aria-label')
                except NoSuchElementException:
                        return 0


class Amazon:
        def __init__(self, driver):
                self.STORE_URL = 'https://amazon.in'
                self.driver = driver

        def get_product_url(self, product_name):
                pass

        def get_product_price(self, product_url):
                driver.get(product_url)
                try:
                        price_elem = driver.find_element_by_id('priceblock_ourprice')
                except NoSuchElementException:
                        return "Out of stock"
                return price_elem.text

        def get_product_rating(self, product_url):
                driver.get(product_url)
                try:
                        rating_elem = driver.find_element_by_css_selector('span[data-hook="rating-out-of-text"]')
                        return rating_elem.text
                except NoSuchElementException:
                        return 0


if __name__ == '__main__':
        # pref = webdriver.ChromeOptions()
        chrome_options = Options()

        # disable image loading
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

        # headless mode
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(options=chrome_options)
        amazon = Amazon(driver)
        # print(amazon.get_product_price('https://www.amazon.in/GeForce-GDDR5-192-Bit-Profile-Graphics/dp/B0734YGRZT'))
        # print(amazon.get_product_price('https://www.amazon.in/Cerberus-GeForce-Gaming-Graphics-Cerberus-GTX1050Ti-O4G/dp/B079JSKCW3'))
        # not in stock
        # print(amazon.get_product_price('https://www.amazon.in/MSI-GeForce-RTX-2060-Graphic/dp/B07TZ55K6J'))
        # 4.1 stars
        # print(amazon.get_product_rating('https://www.amazon.in/GeForce-GDDR5-192-Bit-Profile-Graphics/dp/B0734YGRZT'))
        # no stars
        # print(amazon.get_product_rating('https://www.amazon.in/KARIBUTM-Leather-Button-Black-Pendrive/dp/B08H5MBLHV'))
        # 5 stars
        # print(amazon.get_product_rating('https://www.amazon.in/Dragon-Honor-Swivel-Metal-Memory/dp/B08GK9RH3Q'))

        vedant = VedantComputers(driver)
        # print(vedant.get_product_price('https://www.vedantcomputers.com/pc-components/graphics-card/inno3d-geforce-gtx-1660-ti-twin-x2-6gb-gddr6'))
        # 5 stars
        # print(vedant.get_product_rating('https://www.vedantcomputers.com/pc-components/graphics-card/inno3d-geforce-gtx-1660-ti-twin-x2-6gb-gddr6'))
        # 4 stars
        # print(vedant.get_product_rating('https://www.vedantcomputers.com/combo/combo-amd-5-3600-processor-and-msi-x570-a-pro-motherboard?sort=p.price&order=DESC'))
        # no stars
        # print(vedant.get_product_rating('https://www.vedantcomputers.com/zotac-gaming-geforce-gtx-1660-ti-amp-6gb-gddr6'))

        mdcomp = MDComputers(driver)
        # print(mdcomp.get_product_price('https://mdcomputers.in/amd-dual-core-athlon-200ge.html'))
        # print(mdcomp.get_product_rating('https://mdcomputers.in/amd-dual-core-athlon-200ge.html'))

        primeabgb = PrimeABGB(driver)
        # print(primeabgb.get_product_price('https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-gtx-1660-super-oc-6g-gaming-graphic-card-gv-n166soc-6gd/'))
        # 0 stars
        # print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-gtx-1660-super-oc-6g-gaming-graphic-card-gv-n166soc-6gd/'))
        # 5 stars
        # print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/amd-ryzen-5-3600-3rd-gen-desktop-processor/'))

        itdepot = TheITDepot(driver)
        # print(itdepot.get_product_price('https://www.theitdepot.com/details-Gigabyte+Geforce+GT+710+2GB+DDR3+(GV-N710D3-2GL)_C45P30157.html'))
        # print(itdepot.get_product_price('https://www.theitdepot.com/details-Gigabyte+GeForce+GTX+1650+SUPER+WINDFORCE+OC+4GB+DDR6+(GV-N165SWF2OC-4GD)_C45P33816.html'))
        # 0 stars
        # print(itdepot.get_product_rating('https://www.theitdepot.com/details-Gigabyte+GeForce+GTX+1650+SUPER+WINDFORCE+OC+4GB+DDR6+(GV-N165SWF2OC-4GD)_C45P33816.html'))
        # 5 stars
        # print(itdepot.get_product_rating('https://www.theitdepot.com/details-Western+Digital+Blue+1TB+SATA+Internal+Desktop+Hard+Drive+(WD10EZEX)_C12P24121.html'))
