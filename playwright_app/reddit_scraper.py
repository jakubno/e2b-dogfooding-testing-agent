```python
from playwright.sync_api import sync_playwright
import json

REDDIT_URL = "https://www.reddit.com"

def scrape_reddit():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(REDDIT_URL)

        # Define the data schema
        data_schema = {
            "title": "",
            "author": "",
            "date": ""
        }

        # Extract the data
        data_schema["title"] = page.query_selector("h1").inner_text()
        data_schema["author"] = page.query_selector(".author").inner_text()
        data_schema["date"] = page.query_selector(".date").inner_text()

        browser.close()

        return data_schema

def store_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    data = scrape_reddit()
    store_data(data)
```