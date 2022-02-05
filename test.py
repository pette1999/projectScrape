from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv
import random

options = webdriver.ChromeOptions()
ua = UserAgent()
# a random User Agent
userAgent = ua.random
print("User Agent: ", userAgent)
options.add_argument(f'user-agent={userAgent}')
# options.add_argument('window-size=1200x600')
browser = webdriver.Chrome(options=options)
# Name,Symbol,Network,Address,Deployed,Token Address,Contract Source,Detailed Info

def scrape_tokenSniffer():
  # go to the target site
  browser.get("https://tokensniffer.com/tokens/scam")
  print("Connecting to https://tokensniffer.com/tokens/scam...")

  time.sleep(3)
  
  length = len(browser.find_elements_by_class_name("Home_name__3fbfx"))
  count = 0
  for i in range(length):
    data = []

    data.append(browser.find_elements_by_class_name("Home_name__3fbfx")[i].text)
    browser.find_elements_by_class_name("Home_name__3fbfx")[i].click()
    # now in the detailed page
    if count % 10 == 0:
      time.sleep(10)
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

    print(count, ": ", data)
    writeToFile("tokenSniffer.csv", data)
    count += 1

    time.sleep(1)
    browser.execute_script("window.history.go(-1)")

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