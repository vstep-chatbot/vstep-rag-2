from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    # credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        # model_name="vinai/phobert-base",
    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings
