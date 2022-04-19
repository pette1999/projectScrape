from requests import Session
from bs4 import BeautifulSoup as bs

with Session() as s:
    site = s.get("https://www.linkedin.com/login/zh-cn?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name": "loginCsrfParam"})["value"]
    login_data = {"username": "chenhaifan19991113@gmail.com",
                  "password": "Meiguo1969", "loginCsrfParam": token}
    s.post("https://www.linkedin.com/login", login_data)
    home_page = s.get("https://www.linkedin.com/")
    home_page_content = bs(home_page.content, 'html.parser')
    print(home_page_content)