#!/usr/bin/env python

import unittest
import store

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()

# disable image loading
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

# headless mode
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

amazon = store.Amazon(driver)
vedant = store.VedantComputers(driver)
mdcomp = store.MDComputers(driver)
primeabgb = store.PrimeABGB(driver)
itdepot = store.TheITDepot(driver)


class MDComputersTest(unittest.TestCase):

    def test_price(self):
        print("MDComputers price: ", end='')
        print(mdcomp.get_product_price('https://mdcomputers.in/amd-dual-core-athlon-200ge.html'))

    def test_rating_4(self):
        print("MDComputers rating 4 stars: ", end='')
        print(mdcomp.get_product_rating('https://mdcomputers.in/amd-dual-core-athlon-200ge.html'))

    def test_rating_5(self):
        print("MDComputers rating 5 stars: ", end='')
        print(mdcomp.get_product_rating('https://mdcomputers.in/asus-27-inch-gaming-vg278qr.html'))

    def test_rating_0(self):
        print("MDComputers rating 0 stars: ", end='')
        print(mdcomp.get_product_rating('https://mdcomputers.in/dell-g3-d560319.html'))


class VedantComputersTest(unittest.TestCase):

    def test_price(self):
        print("VedantComputers price: ", end='')
        print(vedant.get_product_price('https://www.vedantcomputers.com/pc-components/graphics-card/inno3d-geforce-gtx-1660-ti-twin-x2-6gb-gddr6'))

    def test_rating_4(self):
        print("VedantComputers rating 4 stars: ", end='')
        print(vedant.get_product_rating('https://www.vedantcomputers.com/combo/combo-amd-5-3600-processor-and-msi-x570-a-pro-motherboard?sort=p.price&order=DESC'))

    def test_rating_5(self):
        print("VedantComputers rating 5 stars: ", end='')
        print(vedant.get_product_rating('https://www.vedantcomputers.com/pc-components/graphics-card/inno3d-geforce-gtx-1660-ti-twin-x2-6gb-gddr6'))

    def test_rating_0(self):
        print("VedantComputers rating 0 stars: ", end='')
        print(vedant.get_product_rating('https://www.vedantcomputers.com/zotac-gaming-geforce-gtx-1660-ti-amp-6gb-gddr6'))


class AmazonTest(unittest.TestCase):

    def test_price(self):
        print("Amazon price: ", end='')
        print(amazon.get_product_price('https://www.amazon.in/GeForce-GDDR5-192-Bit-Profile-Graphics/dp/B0734YGRZT'))

    def test_rating_4(self):
        print("Amazon rating 4.1 stars: ", end='')
        print(amazon.get_product_rating('https://www.amazon.in/GeForce-GDDR5-192-Bit-Profile-Graphics/dp/B0734YGRZT'))

    def test_rating_5(self):
        print("Amazon rating 5 stars: ", end='')
        print(amazon.get_product_rating('https://www.amazon.in/Dragon-Honor-Swivel-Metal-Memory/dp/B08GK9RH3Q'))

    def test_rating_0(self):
        print("Amazon rating 0 stars: ", end='')
        print(amazon.get_product_rating('https://www.amazon.in/KARIBUTM-Leather-Button-Black-Pendrive/dp/B08H5MBLHV'))


class PrimeABGBTest(unittest.TestCase):

    def test_price(self):
        print("PrimeABGB price: ", end='')
        print(primeabgb.get_product_price('https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-gtx-1660-super-oc-6g-gaming-graphic-card-gv-n166soc-6gd/'))

    def test_rating_4(self):
        print("PrimeABGB rating 4 stars: ", end='')
        print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/amd-ryzen-3-3200g-with-radeon-vega-8-graphics-3rd-gen-desktop-processor/'))

    def test_rating_5(self):
        print("PrimeABGB rating 5 stars: ", end='')
        print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/amd-ryzen-5-3600-3rd-gen-desktop-processor/'))

    def test_rating_0(self):
        print("PrimeABGB rating 0 stars: ", end='')
        print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-gtx-1660-super-oc-6g-gaming-graphic-card-gv-n166soc-6gd/'))


class PrimeABGBTest(unittest.TestCase):

    def test_price(self):
        print("PrimeABGB price: ", end='')
        print(primeabgb.get_product_price('https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-gtx-1660-super-oc-6g-gaming-graphic-card-gv-n166soc-6gd/'))

    def test_rating_4(self):
        print("PrimeABGB rating 4 stars: ", end='')
        print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/amd-ryzen-3-3200g-with-radeon-vega-8-graphics-3rd-gen-desktop-processor/'))

    def test_rating_5(self):
        print("PrimeABGB rating 5 stars: ", end='')
        print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/amd-ryzen-5-3600-3rd-gen-desktop-processor/'))

    def test_rating_0(self):
        print("PrimeABGB rating 0 stars: ", end='')
        print(primeabgb.get_product_rating('https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-gtx-1660-super-oc-6g-gaming-graphic-card-gv-n166soc-6gd/'))


class TheITDepotTest(unittest.TestCase):

    def test_price(self):
        print("TheITDepot price: ", end='')
        print(itdepot.get_product_price('https://www.theitdepot.com/details-Gigabyte+Geforce+GT+710+2GB+DDR3+(GV-N710D3-2GL)_C45P30157.html'))

    def test_rating_5(self):
        print("TheITDepot rating 5 stars: ", end='')
        print(itdepot.get_product_rating('https://www.theitdepot.com/details-Western+Digital+Blue+1TB+SATA+Internal+Desktop+Hard+Drive+(WD10EZEX)_C12P24121.html'))

    def test_rating_0(self):
        print("TheITDepot rating 0 stars: ", end='')
        print(itdepot.get_product_rating('https://www.theitdepot.com/details-Gigabyte+GeForce+GTX+1650+SUPER+WINDFORCE+OC+4GB+DDR6+(GV-N165SWF2OC-4GD)_C45P33816.html'))


if __name__ == '__main__':
    unittest.main()
