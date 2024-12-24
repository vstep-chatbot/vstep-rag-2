
import logging
from os import getenv
import os
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from langchain_core.documents import Document

from config import CACHE_PATH, WEB_URL

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

firecrawlApp = FirecrawlApp(api_key=getenv("FIRECRAWL_API_KEY"))

def writeFile(filename: str, content: str) -> None:

    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)

    with open(os.path.join(CACHE_PATH, filename), "w") as file:
        file.write(content)


def scrape_website(url=WEB_URL, id = 0):
    logger.info("Scraping: " + url)

    converter = DocumentConverter()
    web_document = None

    try:
        result = converter.convert(url)
        writeFile(f"{id}.md", result.document.export_to_markdown(strict_text=True))
        web_document = Document(page_content=result.document.export_to_markdown(strict_text=True), metadata={"source": url})
    except Exception as e:
        logger.error(f"Error Scraping Docling: {e}")

        try:
            scrape_result = firecrawlApp.scrape_url(url, params={"formats": ["markdown"]})
            if "markdown" not in scrape_result:
                raise Exception("No markdown content in scrape result")
            writeFile(f"{id}-firecrawl.md", scrape_result['markdown'])

            web_document = Document(page_content=scrape_result['markdown'], metadata={"source": url})

        except Exception as e:
            logger.error(f"Error Firecrawl: {e}")
            return None

    return web_document
