from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_function() -> HuggingFaceEmbeddings:
    embeddings = HuggingFaceEmbeddings(
        model_name="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base",
    )
    return embeddings
