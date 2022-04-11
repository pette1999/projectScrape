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
from os.path import exists
from tqdm import tqdm
import csv

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

def writeToFile(filename, data):
  with open(filename, 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)
    
def prompt_email_password():
  u = input("Email: ")
  p = getpass.getpass(prompt="Password: ")
  return (u, p)

def page_has_loaded(driver):
  page_state = driver.execute_script('return document.readyState;')
  return page_state == 'complete'

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

def login(driver, email=None, password=None, timeout=10):
  if exists('./cookies.pkl'):
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

def getPageNumber(driver):
  driver.get("https://www.linkedin.com/search/results/people/?keywords=student%20at%20harvard%20university&network=%5B%22S%22%5D&origin=FACETED_SEARCH&page=25&sid=5!C")
  driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
  time.sleep(1)
  driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
  time.sleep(1)
  bs_content = bs(driver.page_source, "html.parser")
  # f = open("page.html","w")
  # f.write(str(bs_content))
  # f.close()
  
  max_page = bs_content.find_all("li", class_="artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view")[-1].span.string
  print(max_page)
  return [max_page,bs_content]
  
def getPeopleUrl(driver,count,search_term):
  link = []
  for c in tqdm(range(int(count))):
    if c%10 == 0:
      time.sleep(5)
    url = "https://www.linkedin.com/search/results/people/?keywords=student%20at%20harvard%20university&origin=SWITCH_SEARCH_VERTICAL&page=" + str(c) + "&sid=jdX"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
    time.sleep(1)
    bs_content = bs(driver.page_source, "html.parser")
    # f = open("page.html","w")
    # f.write(str(bs_content))
    # f.close()
    for i in bs_content.find_all("a", class_="app-aware-link"):
      if i.get('href') not in link and '-' in i.get('href')[27:] and i.get('target') != "_self":
        link.append(i.get('href'))
        writeToFile('./data/link.csv',i.get('href'))
  print(len(link))
  
def main():
  login(browser,email="chenhaifan19991113@gmail.com",password="Meiguo1969")
  getPeopleUrl(browser,getPageNumber(browser)[0],0)


# browser.get("https://www.linkedin.com/search/results/people/?keywords=student%20at%20harvard%20university&origin=SWITCH_SEARCH_VERTICAL&page=1&sid=L-I")
# bs_content = bs(browser.page_source, "lxml")
# f = open("page.html","w")
# f.write(str(bs_content))
# f.close()

main()