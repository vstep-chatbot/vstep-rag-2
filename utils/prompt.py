import logging
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether

from config import PROMPT_TEMPLATE
from utils.scrape import writeFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def design_prompt(results : List[Tuple[Document, float]], user_input):
    result_docs = [doc.page_content for doc, _ in results]
    context_text = "\n########".join(result_docs)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(context=context_text, question=user_input)

    writeFile(".prompt", prompt)
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
