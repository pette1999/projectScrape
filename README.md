# projectScrape
This project contains two scraping methods to scrpae Rugpull projects from rugscreen.com and tokensniffer.com

### tokensniffer.com
The data scraped from the site is stored in the file `tokenSniffer.csv`. 
The scraper would scrape the following information:
- Project Name (ex. BABYDOS)
- Token symbol (ex. BABYDOS)
- Network (ex. BSC-Binance Smart Chain)
- Address (ex. 0xfa3f07a3de1a193594bb0afeeb7e5edc55bc1830)
- Deployed time (ex. 05 Feb 2022 09:19:53 GMT)
- Token Address (ex. https://bscscan.com/token/0xfa3f07a3de1a193594bb0afeeb7e5edc55bc1830)
- Contract source code
- Detialed info
- Token Price
- Total Supply
- Market Cap
- Chart

### Rugscreen.com
The data scraped from the site is stored in the file `certificates.csv`. **NOTE** (These projects are not identified as rugpull, these are clean projects)
The scraper would scrape the following information:
- Data Time(UTC)
- Token URL
- Contracts Scanned
- Score