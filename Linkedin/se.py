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
import random

options = webdriver.ChromeOptions()
ua = UserAgent()
userAgent = ua.random
print("User Agent: ", userAgent)
# options.add_argument(f'user-agent={userAgent}')
# options.add_argument("--user-data-dir=chrome-data")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")
options.add_argument("--incognito")
browser = webdriver.Chrome(options=options)
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def writeToFile(filename, data):
  with open(filename, 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)
    
def readCol(filename, colName):
  id = []
  file = csv.DictReader(open(filename, 'r'))
  for col in file:
    id.append(col[colName])

  return id

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
  # print(cookies)
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
  python_button.send_keys(email)
  python_button = browser.find_element(By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[2]/input')
  python_button.send_keys(password)
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
  
def getPeopleUrl(driver,count,filename,url1,url2):
  link = readCol(filename,'urls')
  for c in tqdm(range(int(count))):
    if c%10 == 0 and c>0:
      for _ in tqdm(range(random.randrange(20, 60, 2)),desc="waiting 10 ..."):
        time.sleep(1)
    if c%15 == 0 and c>0:
      for _ in tqdm(range(random.randrange(20, 60, 2)),desc="waiting 15 ..."):
        time.sleep(1)
    url = url1 + str(c+1) + url2
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
        writeToFile(filename,[i.get('href')])
  print(len(link))
  
def getPeople(driver, url):
  driver.get(url)
  root = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
      (
        By.CLASS_NAME,
        "pv-top-card",
      )
    )
  )
  driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
  time.sleep(1)
  driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
  time.sleep(1)
  bs_content = bs(driver.page_source, "html.parser")
  f = open("page2.html","w")
  f.write(str(bs_content))
  f.close()
  
  # get name
  name = root.find_element(By.CLASS_NAME, 'text-heading-xlarge').text.strip()
  print("name: ", name)
  # get about
  # check if the person has the about section
  if len(driver.find_elements(By.ID, 'about')) > 0:
    # has the section
    about = bs_content.find("div", class_="display-flex ph5 pv3").div.div.div.span.text
  else:
    about = None
  print("about: ", about)
  # get experience
  section = bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")
  # check if the person has the experience section
  experience = []
  if len(driver.find_elements(By.ID, 'experience')) > 0:
    for i in range(len(section)):
      if section[i].div.get('id') == "experience":
        for j in bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")[i].select("div:nth-of-type("+str(3)+")"):
          # each j is an experience
          # check if has the show all button
          try:       
            if "Show all" in j.find("span", class_="pvs-navigation__text").text.strip():
              # has the show all button
              driver.get(url + "details/experience/")
              time.sleep(3)
              detail_content = bs(driver.page_source, "html.parser")
              # scrape all experiences
              for x in detail_content.find_all("ul", class_="pvs-list"):
                for y in x.find_all("span", class_="visually-hidden"):
                  if y.text.strip() not in experience:
                    experience.append(y.text.strip())
              driver.back()
            else:
              for k in j.find_all("span", class_="visually-hidden"):
                if k.text.strip() not in experience:
                  experience.append(k.text.strip())
          except:
            for k in j.find_all("span", class_="visually-hidden"):
              if k.text.strip() not in experience:
                experience.append(k.text.strip())
  else:
    experience = None
  print("experience: ", experience)
  # get education
  # check if person has the education section
  education = []
  if len(driver.find_elements(By.ID, 'education')) > 0:
    for i in range(len(section)):
      if section[i].div.get('id') == "education":
        for j in bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")[i].select("div:nth-of-type("+str(3)+")"):
          for k in j.find_all('span', class_="visually-hidden"):
            if k.text.strip() not in education:
              education.append(k.text.strip())
  else:
    education = None
  print("education: ", education)
  # get volunteering
  volunteering = []
  if len(driver.find_elements(By.ID, 'volunteering_experience')) > 0:
    for i in range(len(section)):
      if section[i].div.get('id') == "volunteering_experience":
        for j in bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")[i].select("div:nth-of-type("+str(3)+")"):
          # check if has the show all button
          try:  
            if "Show all" in j.find("span", class_="pvs-navigation__text").text.strip():
              driver.get(url + "details/volunteering-experiences/")
              time.sleep(3)
              detail_content = bs(driver.page_source, "html.parser")
              # scrape all volunteering experiences
              for x in detail_content.find_all("ul", class_="pvs-list"):
                for y in x.find_all("span", class_="visually-hidden"):
                  if y.text.strip() not in volunteering:
                    volunteering.append(y.text.strip())
              driver.back()
            else:
              for k in j.find_all('span', class_="visually-hidden"):
                if k.text.strip() not in volunteering:
                  volunteering.append(k.text.strip())
          except:
            for k in j.find_all('span', class_="visually-hidden"):
              if k.text.strip() not in volunteering:
                volunteering.append(k.text.strip())
  else:
    volunteering = None
  print("volunteering: ", volunteering)
  # get licenses and certificates
  licenses = []
  if len(driver.find_elements(By.ID, 'licenses_and_certifications')) > 0:
    for i in range(len(section)):
      if section[i].div.get('id') == "licenses_and_certifications":
        for j in bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")[i].select("div:nth-of-type("+str(3)+")"):
          for k in j.find_all('span', class_="visually-hidden"):
            if k.text.strip() not in licenses:
              licenses.append(k.text.strip())
  else:
    licenses = None
  print("Licenses: ", licenses)
  # get Honors & awards
  honors = []
  if len(driver.find_elements(By.ID, 'honors_and_awards')) > 0:
    for i in range(len(section)):
      if section[i].div.get('id') == "honors_and_awards":
        for j in bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")[i].select("div:nth-of-type("+str(3)+")"):
          for k in j.find_all('span', class_="visually-hidden"):
            if k.text.strip() not in honors:
              honors.append(k.text.strip())
  else:
    honors = None
  print("Hornors: ", honors)
  # get skills
  skills = []
  if len(driver.find_elements(By.ID, 'skills')) > 0:
    for i in range(len(section)):
      if section[i].div.get('id') == "skills":
        for j in bs_content.find_all("section", class_="artdeco-card ember-view break-words pb3 mt4")[i].select("div:nth-of-type("+str(3)+")"):
          # check if has the show all button
          try:  
            if "Show all" in j.find("span", class_="pvs-navigation__text").text.strip():
              driver.get(url + "details/skills/")
              time.sleep(3)
              detail_content = bs(driver.page_source, "html.parser")
              # scrape all skills experiences
              for x in detail_content.find_all("ul", class_="pvs-list"):
                for y in x.find_all("span", class_="visually-hidden"):
                  if y.text.strip() not in skills and '·' not in y.text.strip():
                    skills.append(y.text.strip())
              driver.back()
            else:
              for k in j.find_all('span', class_="visually-hidden"):
                if k.text.strip() not in skills and '·' not in y.text.strip():
                  skills.append(k.text.strip())
          except:
            for k in j.find_all('span', class_="visually-hidden"):
              if k.text.strip() not in skills and '·' not in y.text.strip():
                skills.append(k.text.strip())
  else:
    skills = None
  print("Skills: ", skills)
  writeInfo("./data/info.csv",name,about,experience,education,volunteering,licenses,honors,skills)
  
def writeInfo(file,name,about,experience,education,volunteering,Licenses,Hornors,Skills):
  about_info = about
  experience_info = ""
  education_info = ""
  volunteering_info = ""
  Licenses_info = ""
  Hornors_info = ""
  Skills_info = ""
  
  if experience != None:
    for i in experience:
      experience_info += i
      experience_info += '\n'
  else:
    experience_info = None
  if education != None:
    for j in education:
      education_info += j
      education_info += '\n'
  else:
    education_info = None
  if volunteering != None:
    for k in volunteering:
      volunteering_info += k
      volunteering_info += '\n'
  else:
    volunteering_info = None
  if Licenses != None:
    for x in Licenses:
      Licenses_info += x
      Licenses_info += '\n'
  else:
    Licenses_info = None
  if Hornors != None:
    for y in Hornors:
      Hornors_info += y
      Hornors_info += '\n'
  else:
    Hornors_info = None
  if Skills != None:
    for z in Skills:
      Skills_info += z
      Skills_info += '\n'
  else:
    Skills_info = None
  
  writeToFile(file, [name,about_info,experience_info,education_info,volunteering_info,Licenses_info,Hornors_info,Skills_info])
  
def main():
  login(browser,email="",password="")
  # getPeopleUrl(browser,100,'./data/mit.csv',
  #              'https://www.linkedin.com/search/results/people/?currentCompany=%5B%221503%22%5D&keywords=student%20at%20MIT&origin=FACETED_SEARCH&page=',
  #              '&schoolFilter=%5B%2218494%22%5D&sid=puP')
  url1 = ['https://www.linkedin.com/search/results/people/?currentCompany=%5B%22157313%22%5D&keywords=student%20at%20Princeton%20university&origin=FACETED_SEARCH&page=']
  url2 = ['&schoolFilter=%5B%2218867%22%5D&sid=Aea']
  for i in tqdm(range(len(url1)),desc="total process..."):
    getPeopleUrl(browser,100,'./data/princeton.csv',url1[i],url2[i])
main()