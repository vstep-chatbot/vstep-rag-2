import logging
from uuid import uuid4

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker

from phoBERT.embedding_func import get_embedding_function
from utils.vncorenlp_tokenizer import word_segment

chunker = SemanticChunker(embeddings=get_embedding_function(), min_chunk_size=100, breakpoint_threshold_amount=60)


def split_document(document: Document) -> list[Document]:
    if document.metadata["source"] is None or document.metadata["source"] == "":
        logging.error("Document must have a source.")
        raise ValueError("Document must have a source.")

    annotated_text = word_segment(document.page_content)

    documents = chunker.create_documents([annotated_text])
    
    documents = [remove_underscore(doc) for doc in documents]

    logging.info(f"Split document into {len(documents)} chunks.")

    for doc in documents:
        doc.metadata["id"] = str(uuid4())

    return documents

def remove_underscore(doc: Document) -> Document:
    doc.page_content = doc.page_content.replace("_", " ")
    return doc