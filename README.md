# Vineyard Recipe Scraper #

Scrapes recipes from chosen top recipe websites to be used in the Vineyard application.


# Setup

## Initial Setup

1. Navigate to [repo](https://github.com/emilany/recipe-scraper)
2. Clone locally using
   `git clone https://github.com/emilany/recipe-scraper.git`

## Scraping

The scraping process applies to one website at a time.

1. First change the output filename, rendered in json format, in pipelines.py to desired filename.
2. To scrape the first website, go to the project’s top level directory and run scrapy crawl spidername.
3. The output file will then be stored in the project’s top level directory along with other folders.

## Final Notes

1. After scraping all needed data, format them manually through Sublime Text or other text editors by enclosing all recipe data in brackets “[]”. This step is important for uploading the data in Firebase.
