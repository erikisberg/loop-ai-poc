import requests
from bs4 import BeautifulSoup
import os
import json
from urllib.parse import urljoin

def scrape_website(base_url):
    data = []
    urls_to_scrape = [base_url]
    scraped_urls = set()

    while urls_to_scrape:
        url = urls_to_scrape.pop(0)
        scraped_urls.add(url)

        # Send a request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all text content
        text_content = soup.get_text(strip=True)

        # Split text into chunks (e.g., paragraphs)
        chunks = text_content.split('\n\n')

        # Add text chunks to the data list
        for chunk in chunks:
            if chunk.strip():
                data.append({'content': chunk.strip(), 'url': url})

        # Find and add new URLs to the list to scrape
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                new_url = urljoin(base_url, href)
                if new_url.startswith(base_url) and new_url not in scraped_urls and new_url not in urls_to_scrape:
                    urls_to_scrape.append(new_url)

    return data

def save_data(data, filename):
    # Create the output directory if it doesn't exist
    output_dir = 'scraped_data'
    os.makedirs(output_dir, exist_ok=True)

    # Save the data as a JSON file
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Data saved to {output_path}")

# Example usage
base_url = 'https://impactloop.se'
filename = 'impactloop_data.json'

data = scrape_website(base_url)
save_data(data, filename)