import time
from selenium import webdriver

brower = webdriver.Chrome()

brower.get("http://www.shuaia.net/")

# time.sleep(5)
# brower.find_element_by_xpath('//div[@id="header"]/div[@class="menu-bar"]/div[@class="nav-link-icon"]').click()
brower.find_element_by_class_name("nav-link-icon").click()
url_list=brower.find_elements_by_css_selector("#header ul li a")

for url in url_list:
    name = url.text
    href = url.get_attribute("href")
