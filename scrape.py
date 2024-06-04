import os
import requests
import re
from bs4 import BeautifulSoup
import argparse
from tqdm import tqdm
from pathlib import Path

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def safe_open_w(path):
    create_directory(os.path.dirname(path))
    return open(path, 'wb')

def scrape_fandom(fandom_site):
    base_url = f"https://{fandom_site}.fandom.com"
    nextpage_url = "/wiki/Special:AllPages"
    visited_urls = set([nextpage_url])

    while nextpage_url:
        visited_urls.add(nextpage_url)
        try:
            req = requests.get(base_url + nextpage_url)
            soup = BeautifulSoup(req.content, "html.parser")

            content = soup.find("div", {"class": "mw-allpages-body"})
            entries = content.find_all("li") if content else []

            if entries:
                pages_data = "\n".join(re.sub(r"\(redirect.*?\)", "", entry.text) for entry in tqdm(entries, desc="Scraping"))
                payload = {'catname': '', 'pages': pages_data, 'curonly': '1', 'wpDownload': 1, 'wpEditToken': '+\\',
                           'title': 'Special:Export'}
                response = requests.post(base_url + "/wiki/Special:Export", data=payload)
                data = response.content

                with safe_open_w(f"{fandom_site}_raw/{len(visited_urls)}.xml") as f:
                    f.write(data)

            nextpage = soup.find("div", {"class": "mw-allpages-nav"})
            
            if nextpage and nextpage.find_all("a"):
                nextpage_url = nextpage.find_all("a")[-1].get("href")
            else:
                nextpage_url = ""

            if nextpage_url in visited_urls:
                nextpage_url = ""
        except Exception as e:
            print("Error:", e)

def merge_files(fandom_site):
    with open(Path(f"{fandom_site}.xml"), "w") as output_file:
        for filepath in Path(f"{fandom_site}_raw").glob("*.xml"):
            output_file.write(filepath.read_text() + "\n")

def main():
    parser = argparse.ArgumentParser(description='Scrapes a Fandom page into XML')
    parser.add_argument('input_fandom', help='Fandom name')
    args = parser.parse_args()

    scrape_fandom(args.input_fandom)
    merge_files(args.input_fandom)

if __name__ == "__main__":
    main()
