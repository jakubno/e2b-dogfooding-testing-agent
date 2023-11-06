```python
from playwright.sync_api import sync_playwright
import json
from reddit_scraper import RedditScraper

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        reddit_scraper = RedditScraper(page)
        reddit_url = "https://www.reddit.com"  # Replace with the actual Reddit URL
        data = reddit_scraper.scrape(reddit_url)
        browser.close()

    with open('data.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
```