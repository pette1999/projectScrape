from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv
import random
import pickle
import pickle


options = webdriver.ChromeOptions()
ua = UserAgent()
# a random User Agent
userAgent = ua.random
print("User Agent: ", userAgent)
options.add_argument(f'user-agent={userAgent}')
options.add_argument("--user-data-dir=chrome-data")
# Adding the argument --disable-blink-features=AutomationControlled
options.add_argument('--disable-blink-features=AutomationControlled')
# Exclude the collection of enable-automation switches
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# Turn-off useAutomationExtension
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('window-size=1200x600')
browser = webdriver.Chrome(options=options)
# Change the property value of the navigator for webdriver to undefined
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# with open('tokenSniffer.csv', 'w', encoding='UTF8') as f:
#   writer = csv.writer(f)
#   # write the header
#   writer.writerow(header)

def scrape_tokenSniffer():
  # go to the target site
  browser.get("https://tokensniffer.com/tokens/scam")
  print("Connecting to https://tokensniffer.com/tokens/scam...")
  cookies = pickle.load(open("cookies.pkl", "rb"))
  for cookie in cookies:
    browser.add_cookie(cookie)

  time.sleep(1.5)
  
  length = len(browser.find_elements_by_class_name("Home_name__3fbfx"))
  print("length: ", length)
  for i in range(length):
    data = []

    data.append(browser.find_elements_by_class_name("Home_name__3fbfx")[i].text)
    browser.find_elements_by_class_name("Home_name__3fbfx")[i].click()
    # now in the detailed page
    if i % 10 == 0:
      time.sleep(1)
    # grab page source code
    pageSource = browser.page_source
    # using bs4 to parse the html source code
    soup = BeautifulSoup(pageSource, 'html.parser')
    head = soup.find("h2", {"class":"Home_title__3DjR7"})
    data.append(head.find_all("div")[0].text[head.find_all("div")[0].text.find('(')+1:-1])
    data.append(head.find_all("div")[1].text.strip().split(":")[0])
    data.append(head.find_all("div")[1].text.strip().split(":")[1])

    table = soup.find("table", {"class":"Home_section__16Giz"}).tbody
    data.append(table.find_all("tr")[2].text.replace("Deployed","").strip()[:table.find_all("tr")[2].text.replace("Deployed","").strip().find('(')])

    token_addr = "https://bscscan.com/token/" + head.find_all("div")[1].text.strip().split(":")[1]
    data.append(token_addr)

    contract_source = "https://tokensniffer.com/contract/" + head.find_all("div")[1].text.strip().split(":")[1]
    data.append(contract_source)

    data.append(browser.current_url)

    # go to the pooCoin site and grab the information
    pooCopin = "https://poocoin.app/tokens/" + head.find_all("div")[1].text.strip().split(":")[1]
    try:
      browser.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/table/tbody/tr[2]/td/div/div[2]/a').click()
    except:
      data.append("")
      data.append("")
      data.append("")
      data.append("")
      print(i, ": ", data)
      writeToFile("tokenSniffer.csv", data)
      browser.execute_script("window.history.go(-1)")
      continue
    browser.switch_to.window(browser.window_handles[1])
    # browser.get(pooCopin)
    time.sleep(1.5)
    print(browser.current_url)
    

    # price of the token
    try:
      price = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span'))).text
      # price = browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span').text
    except:
      price = ""
      pass
    print("Price: ", price)
    data.append(price[1:])
    # Total supply
    try:
      # supply = browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]').text
      supply = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]'))).text
    except:
      supply = ""
      pass

    print("Supply: ", supply.split('\n'))

    supply_count = 0
    marketCap_count = 0
    for n in range(len(supply.split('\n'))):
      if "total supply" in supply.split('\n')[n].lower():
        data.append(supply.split('\n')[n+1].strip().replace(",",""))
        supply_count += 1
      if "market cap" in supply.split('\n')[n].lower():
        if "$" in supply.split('\n')[n+1].strip():
          data.append(supply.split('\n')[n+1].strip()[1:])
          marketCap_count += 1
        else:
          for i in supply.split('\n')[n+2].strip().split(" "):
            if "$" in i:
              data.append(i[1:-1].replace("$","").replace(",",""))
              marketCap_count += 1
    if supply_count == 0:
      data.append("")
    if marketCap_count == 0:
      data.append("")

    data.append(pooCopin)
    
    print(i, ": ", data)
    writeToFile("tokenSniffer.csv", data)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    browser.execute_script("window.history.go(-1)")

  browser.close()

def scrape_rugScreen():
  # go to the target site
  browser.get("https://www.rugscreen.com/Scan/Certificates")
  print("Connecting to rugscreen.com...")
  # let the site render the javascript
  time.sleep(3)
  # Get the records count
  count = browser.find_element_by_id('certificates_info').text.split(' ')[-2]
  # get how many pages
  pages = int(int(count.replace(',',''))/100+1)

  # change the view to 100 per page
  select = Select(browser.find_element_by_xpath('//*[@id="certificates_length"]/label/select'))
  select.select_by_value('100')
  time.sleep(2)

  count = 1

  for k in range(pages):
    if k%10 == 0:
      time.sleep(random.randint(1000, 5000)/1000)
    time.sleep(1)
    # grab page source code
    pageSource = browser.page_source
    # using bs4 to parse the html source code
    soup = BeautifulSoup(pageSource, 'lxml')
    print(soup)
    # links = []
    table = soup.find("table", {"id": "certificates"})

    temp = []
    for i in table.tbody:
      for j in i:
        temp.append(j.text)
      print(temp)
      writeToFile("certificates.csv", temp)
      temp = []
      print(count, '\n')
      count += 1

    # go to the next page
    try:
      browser.find_element_by_id('certificates_next').click()
    except:
      continue
  
  browser.close()

def writeToFile(filename, data):
  with open(filename, 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)

if __name__ == "__main__":
  # scrape_rugScreen()
  scrape_tokenSniffer()