from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import time
import getpass
import json
import pickle

options = webdriver.ChromeOptions()
ua = UserAgent()
userAgent = ua.random
print("User Agent: ", userAgent)
# options.add_argument(f'user-agent={userAgent}')
# options.add_argument("--user-data-dir=chrome-data")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--headless")
options.add_argument("--incognito")
browser = webdriver.Chrome(options=options)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def prompt_email_password():
  u = input("Email: ")
  p = getpass.getpass(prompt="Password: ")
  return (u, p)

def page_has_loaded(driver):
  page_state = driver.execute_script('return document.readyState;')
  return page_state == 'complete'

def login(driver, email=None, password=None, cookie=None, timeout=10):
  if cookie is not None:
    loadcookie(driver)
    driver.get("https://www.linkedin.com")
    return
  if not email or not password:
    email, password = prompt_email_password()
  driver.get("https://www.linkedin.com/login")
  python_button = browser.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[1]/input')
  python_button.send_keys("chenhaifan19991113@gmail.com")
  python_button = browser.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[2]/input')
  python_button.send_keys("Meiguo1969")
  python_button.submit()
  
  try:
    if driver.url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
      remember = driver.find_element_by_id(c.REMEMBER_PROMPT)
      if remember:
        remember.submit()
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, c.VERIFY_LOGIN_ID)))
  except: pass
  
  savecookies(browser)
  
def loadcookie(driver):
  driver.get("https://www.linkedin.com/login")
  print("loading cookie")
  cookies = pickle.load(open("cookies.pkl", "rb"))
  print(cookies)
  driver.add_cookie(cookies)
  print('loaded cookie')
  
def savecookies(driver):
  time.sleep(5)
  cookies=driver.get_cookies()
  for cookie in cookies:
      if(cookie['name']=='li_at'):
          cookie['domain']='.linkedin.com'
          x={
          'name': 'li_at',
          'value': cookie['value'],
          'domain': '.linkedin.com'
          }
          break
  pickle.dump(x , open("cookies.pkl","wb"))
  print('cookies saved')
  
login(browser,email="chenhaifan19991113@gmail.com",password="Meiguo1969",cookie='0')
# # python_button.send_keys(Keys.RETURN)
# print("Logging in...")
# time.sleep(3)
# browser.get("https://www.linkedin.com/search/results/people/?keywords=student%20at%20harvard%20university&origin=SWITCH_SEARCH_VERTICAL&page=1&sid=L-I")
# time.sleep(10)
# bs_content = bs(browser.page_source, "lxml")
# f = open("page.html","w")
# f.write(str(bs_content))
# f.close()
# browser.close()