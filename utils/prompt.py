import logging
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether

from config import PROMPT_TEMPLATE
from utils.scrape import writeCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def design_prompt(results: List[Tuple[Document, float]], user_input: str):
    result_docs = [doc.page_content for doc, _ in results]

    context_text = ""
    for doc in result_docs:
        context_text += "#######" + doc.strip() + "\n"
    context_text += "#######"

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(context=context_text, question=user_input)

    writeCache(".prompt", prompt)
    return prompt


# generate response
def generate_response(prompt):
    model = ChatTogether(
        # model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
        # model="meta-llama/Llama-Vision-Free-Form-2B",
        model="meta-llama/Llama-Vision-Free",
        # model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        # model="google/gemma-2b-it",
        temperature=0.8,
        max_tokens=1024,
    )

    # response = model.invoke(prompt)
    response = model.invoke(prompt).content
    return response


def design_prompt_raft(results: List[Tuple[Document, float]], user_input) -> str:
    prompt = ""

    for tuple in results:
        prompt += "<DOCUMENT>" + tuple[0].page_content.strip() + "</DOCUMENT>"

    prompt += user_input

    return prompt
