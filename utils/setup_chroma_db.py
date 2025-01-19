import logging
import os

from config import CHROMA_PATH, FORCE_FIRECRAWL_URLS, LOCAL_SOURCES_PATH, WEB_URLS
from phoBERT.chunking import split_document
from utils.database import get_instance, is_chroma_db_empty
from utils.scrape import scrape_file, scrape_website

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_chroma_db():
    logger.info("Setting up Chroma database...")
    logger.info("CHROMA_PATH: " + CHROMA_PATH)

    chroma_db = get_instance()

    if is_chroma_db_empty(chroma_db):
        for index, source in enumerate(WEB_URLS):
            logger.info(f"Scraping {index}: {source[7:80]}")

            web_document = scrape_website(source, index)

            if not web_document:
                logger.error(f"Error scraping: {source}")
                continue

            chunks = split_document(web_document)

            chroma_db.add_documents(chunks)

        for index, source in enumerate(FORCE_FIRECRAWL_URLS):
            logger.info(f"Scraping Firecrawl {index}: {source[7:80]}")

            web_document = scrape_website(source, index, use_firecrawl=True)

            if not web_document:
                logger.error(f"Error scraping: {source}")
                continue

            chunks = split_document(web_document)

            chroma_db.add_documents(chunks)

        for root, dirs, files in os.walk(LOCAL_SOURCES_PATH):
            for file in files:
                if file.endswith('.pdf') or file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    logger.info(f"Processing file: {file_path}")

                    doc = scrape_file(file_path)
                    if doc is None:
                        logger.error(f"Error processing file: {file_path}")
                        continue

                    chunks = split_document(doc)

                    chroma_db.add_documents(chunks)

    logger.info("Chroma database setup complete with " + str(len(chroma_db.get()['documents'])) + " documents.")
