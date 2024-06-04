# Fandom Scraper
Fandom provides wiki data at https://examplename.fandom.com/wiki/Special:Statistics, but most fandoms are either out of date or completely missing wiki dumps.

This script scrapes the data of a provided fandom(s) and provides it in .jsonl format with the source url and text on that page. This data is useful for many downstream NLP tasks.

## How It Works

Fandom.com provides a list of all pages on the `Special:AllPages` page. This script goes through each link on that page and uses Pandas, BeautifulSoup4, and WikiExtractor to scrape the data.

## Instructions
1. Install dependencies by running `pip install -r requirements.txt`
2. Run the scraper by providing wiki names as command line arguments in run.py (`python run.py wiki1 wiki2 ...`)

Example
```sh
python run.py genshin-impact hibike-euphonium
```
