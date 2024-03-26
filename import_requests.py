import requests
from bs4 import BeautifulSoup
import pandas as pd
import os  # For file handling

def savescraped_data(data, filename):
    """Saves scraped data to a CSV file, handling potential errors."""
    try:
        # Create the directory if it doesn't exist
        os.makedirs('scraped_data', exist_ok=True)  # Optional: Create a directory

        # Create the DataFrame and save as CSV
        df = pd.DataFrame({'Text': data})
        df.to_csv(f'scraped_data/{filename}.csv', index=False)
        print(f"Scraped data saved to: scraped_data/{filename}.csv")
    except Exception as e:
        print(f"Error saving data: {e}")

def scrape_jansatta_cricket(start_page=1, end_page=873):
    """Scrapes news article texts from Jansatta Cricket pages and saves them."""
    scraped_texts = []

    for page_num in range(start_page, end_page + 1):
        url = f'https://www.jansatta.com/national/page/{page_num}'
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, features="html.parser")
        target_divs = [div for div in soup.find_all('div') if div.get('class') == ['article_details']]

        for div in target_divs:
            anchor_tag = div.find('a')
            if anchor_tag:
                text = anchor_tag.text.strip()  # Extract and trim text content
                scraped_texts.append(text)

        if page_num % 100 == 0:  # Print progress every 100 pages
            print(f"Scraped page {page_num}/{end_page}")

    # Save scraped content to a CSV file
    savescraped_data(scraped_texts, f"jansatta_national_news{start_page}{end_page}")

if __name__ == "__main__":
    scrape_jansatta_cricket()