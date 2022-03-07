# projectScrape
This project contains three scraping methods to scrpae Rugpull projects from [rugscreen.com](#Rugscreen.com), [tokensniffer.com](#tokensniffer.com) and [Parsec.finance](#Parsec.finance)

## Parsec.finance
The data scraped from the site is stored in the file `nftHolders.csv`. 
The scraper would scrape the following information:
- Parsec ID
- NFT holder wallet address
- Portfolio Value
- NFT collection
- Collection Value
- Holding Balance
- Opensea url
- Explore url
- Twitter username (if found on opensea)
- Twitter profile url (if found on opensea)

## tokensniffer.com
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

## Rugscreen.com
The data scraped from the site is stored in the file `certificates.csv`. **NOTE** (These projects are not identified as rugpull, these are clean projects)
The scraper would scrape the following information:
- Data Time(UTC)
- Token URL
- Contracts Scanned
- Score

## How to use it
1. Clone this Project `git clone https://github.com/pette1999/projectScrape.git`
2. Check your `Chrome` Browser version `Settings->About Chrome`
3. Download the corresponding version of [chromedriver](https://chromedriver.chromium.org/downloads) and replace the one in the project directory
4. in your terminal, run the `initialize.sh` file by typing `sh initialize.sh`
5. You can run the project with `python3 scrape.py` after the fist initial set up