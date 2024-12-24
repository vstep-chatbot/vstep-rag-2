from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from os import getenv

load_dotenv()

app = FirecrawlApp(api_key=getenv("FIRECRAWL_API_KEY"))

# Scrape a website:
scrape_result = app.scrape_url('firecrawl.dev', params={'formats': ['markdown']})
print(scrape_result)
