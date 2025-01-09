from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

MODEL_ID = "itdainb/PhoRanker"
MAX_LENGTH = 256

model = CrossEncoder(MODEL_ID, max_length=MAX_LENGTH)

# For fp16 usage
model.model.half()


def rerank_results(
    query_results: list[tuple[Document, float]], segmented_user_input: str
) -> list[tuple[Document, float]]:
    scores = model.predict([(doc.page_content, segmented_user_input) for doc, _ in query_results])
    sorted_results = sorted(zip(query_results, scores), key=lambda x: x[1], reverse=True)

    return [(doc, score) for (doc, _), score in sorted_results]
