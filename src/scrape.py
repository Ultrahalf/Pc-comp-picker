from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = 'https://mdcomputers.in'
SEARCH_TERM = 'Ryzen 3 2200G'

driver = webdriver.Firefox()
driver.get(URL)

search_elem = driver.find_element_by_name('search')
search_elem.clear()
search_elem.send_keys(SEARCH_TERM)
search_elem.send_keys(Keys.RETURN)

# required as we have to wait for the search results to load
sleep(5)

product = driver.find_element_by_class_name('product-image-container')
product.click()

# wait for the product page to load
sleep(5)

price = driver.find_element_by_id('price-old')

print(f"Price: {price.get_attribute('content')}")
print(f"Url: {driver.current_url}")
driver.close()
