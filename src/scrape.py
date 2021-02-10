import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get('https://mdcomputers.in')

search_elem = driver.find_search_element_by_name('search')
search_elem.clear()
search_elem.send_keys('Ryzen 3 2200G')
search_elem.send_keys(Keys.RETURN)

# required as we have to wait for the search results to load
time.sleep(5)

product = driver.find_element_by_class_name('product-image-container')
product.click()

# wait for the product page to load
time.sleep(5)

price = driver.find_element_by_id('price-old')

print(f"Price: {price.get_attribute('content')}")
print(f"Url: {driver.current_url}")
driver.close()
