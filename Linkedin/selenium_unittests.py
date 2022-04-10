from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Remote( command_executor='http://192.168.1.108:4444', desired_capabilities={'browserName': 'chrome', 'platformName': 'MAC', 'javascriptEnabled': True})
driver.get("https://github.com")
print(driver.title)
assert "GitHub" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("testname")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()