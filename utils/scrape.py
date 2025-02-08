import logging
import os
from os import getenv
from typing import Optional

from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from langchain_core.documents import Document

from langchain_text_splitters import MarkdownTextSplitter
from config import CACHE_PATH

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

firecrawlApp = FirecrawlApp(api_key=getenv("FIRECRAWL_API_KEY"))


def writeCache(filename: str, content: str) -> None:
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)

    with open(os.path.join(CACHE_PATH, filename), "w") as file:
        file.write(content)


def scrape_website(url, id=0, use_firecrawl=False) -> Optional[Document]:
    logger.info("Scraping: " + url)

    converter = DocumentConverter()
    web_document = None

    try:
        if use_firecrawl:
            raise Exception("Forcing Firecrawl")

        if os.path.exists(f"{CACHE_PATH}/{id}.md"):
            logger.info("Using cache")
            with open(f"{CACHE_PATH}/{id}.md", "r") as file:
                content = file.read()
                web_document = Document(page_content=content, metadata={"source": url})
                return web_document

        result = converter.convert(url)
        markdown = result.document.export_to_markdown(strict_text=True, image_placeholder="").replace(
            "<missing-text>\n", ""
        )
        writeCache(f"{id}.md", markdown)
        web_document = Document(page_content=markdown, metadata={"source": url})
    except Exception as e:
        logger.error(f"Error Scraping Docling: {e}")

        if os.path.exists(f"{CACHE_PATH}/{id}-firecrawl.md"):
            logger.info("Using cache")
            with open(f"{CACHE_PATH}/{id}-firecrawl.md", "r") as file:
                content = file.read()
                web_document = Document(page_content=content, metadata={"source": url})
                return web_document

        try:
            scrape_result = firecrawlApp.scrape_url(url, params={"formats": ["markdown"]})
            if "markdown" not in scrape_result:
                raise Exception("No markdown content in scrape result")
            writeCache(f"{id}-firecrawl.md", scrape_result["markdown"])

            web_document = Document(page_content=scrape_result["markdown"], metadata={"source": url})

        except Exception as e:
            logger.error(f"Error Firecrawl: {e}")
            return None

    return web_document


def scrape_file(file_path) -> Optional[Document]:
    logger.info("Scraping file: " + file_path)

    document = None
    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        markdown = result.document.export_to_markdown(strict_text=True, image_placeholder="").replace(
            "<missing-text>\n", ""
        )
        document = Document(page_content=markdown, metadata={"source": f"file://{file_path}"})
    except Exception as e:
        logger.error(f"Error Scraping Docling: {e}")
        return None

    return document
