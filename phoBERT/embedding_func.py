from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_function():
    embeddings = HuggingFaceEmbeddings(
        model_name="vinai/phobert-large",
    )
    return embeddings
