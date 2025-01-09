import logging
from uuid import uuid4

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker

from phoBERT.embedding_func import get_embedding_function
from utils.vncorenlp_tokenizer import word_segment

chunker = SemanticChunker(embeddings=get_embedding_function())


def split_document(document: Document) -> list[Document]:
    if document.metadata["source"] is None or document.metadata["source"] == "":
        logging.error("Document must have a source.")
        return []

    annotated_text = word_segment(document.page_content)

    documents = chunker.create_documents([annotated_text])

    for chunk in documents:
        chunk.metadata["id"] = str(uuid4())
        chunk.metadata["source"] = document.metadata["source"]

    return documents
