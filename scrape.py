from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv
import random
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
# service = Service("./chromedriver2")

browser = webdriver.Chrome(options=options)
# Change the property value of the navigator for webdriver to undefined
browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


def scrape_nftHolders_parsec(username,password,nft):
  id = []
  address = []
  portfolio_value = []
  nft_collection = []
  collection_value = []
  holding_balance = []
  opensea = []
  explore = []

  browser.get("https://app.parsec.finance/login")
  print("Connecting to parsec App...")
  time.sleep(1)

  field = browser.find_element(By.XPATH, '//*[@id="username"]')
  field.send_keys(username)
  browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/span[1]').click()
  field = browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[1]/input')
  field.send_keys(password)
  browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div[2]/button').submit()

  time.sleep(5)
  browser.find_element(By.XPATH, '//*[@id="root"]/div/header/div[1]/div[1]').click()
  browser.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/button[2]').click()
  browser.find_element(By.XPATH, '/html/body/div[2]/div[4]').click()
  browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/button[1]').click()
  browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div[2]').click()
  field = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div[2]/span[2]/div/input')
  field.send_keys(nft)
  browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/button').click()
  browser.find_element(By.XPATH, '//*[@id="nft-holders-table"]/div/div[1]/div[2]').click()
  browser.find_element(By.XPATH, '//*[@id="nft-holders-table"]/div/div[2]/div/div[1]/button').click()
  browser.find_element(By.XPATH, '//*[@id="nft-holders-table"]/div/div[2]/div/div[2]/div/div[2]/select/option[3]').click()
  browser.find_element(By.XPATH, '//*[@id="nft-holders-table"]/div/div[2]/div/div[2]/button').click()
  time.sleep(5)
  for i in range(0,300):
    print(i)
    id_input = browser.find_elements(By.CLASS_NAME, 'AddressLabelPreview_text')[i].text
    id.append(id_input)
    browser.find_elements(By.CLASS_NAME, 'AddressLabelPreview_text')[i].click()
    time.sleep(5)
    portfolio_value_input = browser.find_elements(By.CLASS_NAME, 'ParsecSpan')[1].text.replace('$','')
    portfolio_value.append(portfolio_value_input)
    nft_collection.append(nft)
    collection_value_input = browser.find_elements(By.CLASS_NAME, 'ParsecSpan')[4].text.replace('(','').replace(')','').replace('$','')
    collection_value.append(collection_value_input)
    opensea_input = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/a[1]').get_attribute('href')
    opensea.append(opensea_input)
    explore_input = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/a[2]').get_attribute('href')
    explore.append(explore_input)
    address_input = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/a[2]').get_attribute('href').replace('https://etherscan.io/address/','')
    address.append(address_input)
    j = i+1
    balance = f'//*[@id="nft-holders-table"]/div/div[2]/div/div[2]/div[2]/div[{j}]/div/div[2]'
    holding_balance_input = browser.find_element(By.XPATH, balance).text
    holding_balance.append(holding_balance_input)
    browser.find_element(By.XPATH, '/html/body/div[2]/button').click()

    print(id_input,', ',address_input,', ',portfolio_value_input,', ',nft,', ',collection_value_input,', ',holding_balance_input,', ',opensea_input,', ',explore_input)
  
  print(id, address, portfolio_value, nft_collection, collection_value, holding_balance, opensea, explore)


  # browser.find_element(By.XPATH, '//*[@id="nft-holders-table"]/div/div[2]/div/div[2]/div[2]/div[2]/div').click()
  
  # for i in range(1000):
  #   print(f'//*[@id="nft-holders-table"]/div/div[2]/div/div[2]/div[2]/div[{i}]/div')

def scrape_tokenSniffer():
  # go to the target site
  browser.get("https://tokensniffer.com/tokens/scam")
  print("Connecting to https://tokensniffer.com/tokens/scam...")
  cookies = pickle.load(open("cookies.pkl", "rb"))
  for cookie in cookies:
    browser.add_cookie(cookie)

  time.sleep(1.5)
  
  length = len(browser.find_elements(By.CLASS_NAME, "Home_name__3fbfx"))
  print("length: ", length)
  for i in range(length):
    data = []

    data.append(browser.find_elements(By.CLASS_NAME, "Home_name__3fbfx")[i].text)
    browser.find_elements(By.CLASS_NAME, "Home_name__3fbfx")[i].click()
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
      browser.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/table/tbody/tr[2]/td/div/div[2]/a').click()
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
    writeToFile("./data/tokenSniffer.csv", data)
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
      writeToFile("./data/certificates.csv", temp)
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
  # scrape_tokenSniffer()
  scrape_nftHolders_parsec("haichen1999", "Meiguo1969", "Bored Ape Yacht Club")