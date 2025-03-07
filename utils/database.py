import logging
import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CACHE_PATH, CHROMA_PATH
from phoBERT.embedding_func import get_embedding_function

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chroma_db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=get_embedding_function(),
    collection_metadata={"hnsw:space": "cosine"},
)


def get_instance():
    return chroma_db


def add_chunks_to_chroma(chroma_db: Chroma, chunks: list[Document]):
    # Embed the chunks and add them to the database
    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)  # You can use a similar function as before

    # Add or Update the documents.
    existing_items = chroma_db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    logger.info(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        logger.info(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        chroma_db.add_documents(new_chunks, ids=new_chunk_ids)
        # chroma_db.persist()
    else:
        logger.info("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    # This will create IDs like "https://example.com/:6:2"
    # Page Source : Chunk Index
    counter = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")

        chunk_id = f"{source}:{counter}"

        counter += 1

        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    try:
        os.system(f"rm -rf {CHROMA_PATH}")
        os.system(f"rm -rf {CACHE_PATH}")
        logger.info("Database cleared.")

    except Exception as e:
        logger.error(f"Error clearing database: {e}", exc_info=True)
        return False

    return True


def get_top_k_chunks(chroma_db: Chroma, query_text, k=5) -> list[tuple[Document, float]]:
    results = chroma_db.similarity_search_with_score(query_text, k=k)

    logging.info(f"Top {k} chunks retrieved.")
    for doc, score in results:
        logging.info(f"Score: {score}")
        logging.info(f"Page Content: {doc.page_content[:80]}")

    return results


# Check if ChromaDB is empty
def is_chroma_db_empty(chroma_db: Chroma):
    # Check if Chroma has any documents
    existing_items = chroma_db.get(include=[])

    return len(existing_items["ids"]) == 0
