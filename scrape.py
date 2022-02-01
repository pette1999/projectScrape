import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
url = "https://www.rugscreen.com/Scan/Certificates"
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.content, 'lxml')
links = []
for link in soup.find("table", {"id": "certificates"}):
  try:
    print(link)
  except:
      continue
