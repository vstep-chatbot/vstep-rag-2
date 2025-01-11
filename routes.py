import logging

from flask import jsonify, request

from utils.database import get_instance, get_top_k_chunks, is_chroma_db_empty
from utils.prompt import design_prompt, generate_response
from utils.vncorenlp_tokenizer import word_segment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_routes(app):
    chroma_db = get_instance()

    @app.route("/query_llm", methods=["POST"])
    def query_llm():
        if not (request.json):
            return jsonify({"error": "Request must be in JSON format"}), 400

        user_input = request.json.get("query")

        if not user_input:
            return jsonify({"error": "No query provided"}), 400

        segmented_input = word_segment(user_input)

        results = get_top_k_chunks(chroma_db, segmented_input, 5)
        # sorted_results = rerank_results(results, segmented_input)

        prompt = design_prompt(results, user_input)

        response = generate_response(prompt)

        if response:
            return jsonify(
                {
                    "input": segmented_input,
                    "response": response,
                    "chunks": [[doc.page_content, eval(str(score))] for doc, score in results],
                }
            ), 200
        else:
            return jsonify({"error": "Không thể sinh ra câu trả lời."}), 500

    @app.route("/get_chunks", methods=["GET"])
    def get_chunks():
        """
        Retrieves all chunks from the nested list of Document objects and returns them as a list of strings.
        """
        # Get data from the Chroma database
        if is_chroma_db_empty(chroma_db):
            print("Chroma database is empty.")
            return jsonify({"error": "Chroma database is empty."}), 500

        data = chroma_db.get(include=["documents"])

        # Extract the documents from the data
        documents = data["documents"]

        # Extract the page content from each document
        chunks = [doc for doc in documents]

        return jsonify(chunks), 200
