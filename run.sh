#!/bin/bash
python3 scrape.py
git add *
git commit -m "updating the scraping database"
git push