import os
import re
import argparse
import pandas as pd
from tqdm import tqdm

def initial_preprocess(text):
    # Regular expression to remove URLs from the text field
    url_regex = r'&lt;a href="(.*?)"&gt;(.*?)&lt;/a&gt;'

    # Remove URLs
    text = re.sub(url_regex, r'\2', text)

    # Remove unnecessary parentheses
    text = re.sub(r'\(\s+', '(', text)
    text = text.replace('()', '').replace("\u00a0", " ").replace(" , ", ", ")

    return text

def clean_wikitext(text):
    """
    Removes the # markdown token in text and newline tokens.
    """
    return text.replace('\n', ' ').replace('  ', ' ')


def process_files(input_dir, output):
    # Get all directories in input_dir
    directories = os.listdir(input_dir)

    # Open the output file
    with open(output, 'w') as output_file:
        # Iterate through directories
        for directory in tqdm(directories):
            # Iterate through files in the directory
            for filename in tqdm(os.listdir(os.path.join(input_dir, directory)), desc="Processing " + directory):
                # Skip files not starting with 'wiki'
                if not filename.startswith('wiki'):
                    continue

                path = os.path.join(input_dir, directory, filename)
                # Read the JSON file into a DataFrame
                df = pd.read_json(path, lines=True)

                # Skip if DataFrame is empty or 'text' field is empty
                if df.empty or 'text' not in df.columns:
                    continue

                df = df.drop_duplicates()

                # Text processing
                df['text'] = df['text'].apply(initial_preprocess)
                df = df[~df['text'].str.contains("Image Gallery &lt;tabber&gt")]  # Drop all image gallery pages
                df = df.dropna(subset=['text'])  # Drops all rows with None type
                df = df[df['text'].str.strip() != '']  # Drops all rows with empty string
                df['text'] = df['title'] + " " + df['text']
                df['text'] = df['text'].apply(clean_wikitext)
                
                # Write processed data to output file
                df[['url', 'text']].to_json(output_file, orient='records', lines=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Directory with raw data')
    parser.add_argument('output', help='Processed data file output')
    args = parser.parse_args()
    
    process_files(args.input_dir, args.output)