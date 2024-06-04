import argparse
import os
import shutil
from subprocess import run


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Scrapes and processes fandom wiki data")
    parser.add_argument("fandoms", nargs="+", help="Fandoms to process")
    args = parser.parse_args()

    # Loop through values
    for fandom in args.fandoms:
        print(f"Scraping fandom {fandom}")

        # Call scrapeFandom.py
        run(["python3", "scrape.py", fandom])

        # Call wikiextractor
        run(["python", "-m", "wikiextractor.WikiExtractor", f"{fandom}.xml", "--no-templates", "-l", "--json", "-o", fandom])
        
        # Call dataProcessing.py
        run(["python3", "dataProcessing.py", f"{fandom}/", os.path.join("data", f"{fandom}.jsonl")])

        print(f"Successfully outputted data, cleaning up files...")
        # Remove directories and files
        shutil.rmtree(f"{fandom}")
        shutil.rmtree(f"{fandom}_raw")
        os.remove(f"{fandom}.xml")


if __name__ == "__main__":
    main()