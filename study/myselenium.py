from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
elem = driver.find_element_by_name("wd")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
html = driver.page_source
html = html.replace('\u25b6','')
print(html)