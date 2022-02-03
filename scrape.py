from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
url = "https://www.rugscreen.com/Scan/Certificates"
# r = requests.get(url, headers=headers)

session = HTMLSession()
r = session.get(url)

time.sleep(5)


# soup = BeautifulSoup(r.content, 'lxml')
# links = []
# for link in soup.find("table", {"id": "certificates"}):
#   try:
#     print(link)
#   except:
#       continue
r.html.render()

print(r.content)