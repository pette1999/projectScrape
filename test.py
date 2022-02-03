from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import random

options = webdriver.ChromeOptions()
options.add_argument('window-size=1200x600')
browser = webdriver.Chrome(options=options)

def scrape():
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
    # links = []
    table = soup.find("table", {"id": "certificates"})

    temp = []
    for i in table.tbody:
      for j in i:
        temp.append(j.text)
      print(temp)
      writeToFile(temp)
      temp = []
      print(count, '\n')
      count += 1

    # go to the next page
    time.sleep(0.5)
    browser.find_element_by_id('certificates_next').click()
  
  browser.close()

def writeToFile(data):
  with open('certificates.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the data
    writer.writerow(data)

if __name__ == "__main__":
  scrape()