import logging
from uuid import uuid4

from chonkie import SemanticChunker
from langchain_core.documents import Document

chunker = SemanticChunker(
    embedding_model="BAAI/bge-m3",
    threshold=0.5,  # Similarity threshold (0-1)
    chunk_size=80,  # Maximum tokens per chunk
    similarity_window=1,  # Initial sentences per chunk
)

# chunker = MarkdownTextSplitter(chunk_size=450)

# chunker = SemanticChunker(
#     embeddings=SentenceTransformerEmbeddings("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
# )

def split_document(document: Document) -> list[Document]:
    if "source" not in document.metadata or document.metadata["source"] is None or document.metadata["source"] == "":
        logging.error("Document must have a source.")
        return []

    chunks = chunker.chunk(document.page_content)
    return [Document(page_content=chunk.text, metadata={"source": document.metadata["source"]}, id=uuid4()) for chunk in chunks]
    # chunks = chunker.create_documents([document.page_content])
    logging.info(f"Split document into {len(chunks)} chunks.")
    # return chunks
