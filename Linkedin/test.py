from playwright.sync_api import sync_playwright
import os
from bs4 import BeautifulSoup as bs

with sync_playwright() as p:
  browser = p.chromium.launch(channel="chrome",headless=True)
  context = browser.new_context()
  page = context.new_page()
  page.goto("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
  page.fill('input[id="username"]', "chenhaifan19991113@gmail.com")
  page.fill('input[id="password"]', "Meiguo1969")
  page.click('button[type="submit"]')
  # Save storage state into the file.
  storage = context.storage_state(path="state.json")
  # Create a new context with the saved storage state.
  context = browser.new_context(storage_state="state.json")
  
  # Get session storage and store as env variable
  session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
  os.environ["SESSION_STORAGE"] = session_storage

  # Set session storage in a new context
  session_storage = os.environ["SESSION_STORAGE"]
  context.add_init_script("""(storage => {
    if (window.location.hostname === 'example.com') {
      const entries = JSON.parse(storage)
      for (const [key, value] of Object.entries(entries)) {
        window.sessionStorage.setItem(key, key)
      }
    }
  })('""" + session_storage + "')")
  page.wait_for_load_state()
  page.goto("https://www.linkedin.com/search/results/people/?keywords=student%20at%20harvard%20university&origin=SWITCH_SEARCH_VERTICAL&page=1&sid=L-I")
  page.wait_for_load_state()
  print(page.content())
  bs_content = bs(page.content(), "html.parser")
  
  f = open("page.html","w")
  f.write(str(bs_content))
  f.close()

  browser.close()