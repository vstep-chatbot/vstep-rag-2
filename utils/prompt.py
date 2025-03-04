import logging
import os
from typing import List, Tuple

from huggingface_hub import hf_hub_download
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from llama_cpp import CreateChatCompletionResponse, Llama

from config import PROMPT_TEMPLATE
from utils.scrape import writeCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def design_prompt(results: List[Tuple[Document, float]], user_input: str):
    result_docs = [doc.page_content for doc, _ in results]

    context_text = ""
    for doc in result_docs:
        context_text += "#######\n" + doc.strip() + "\n"
    context_text += "#######"

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(context=context_text, question=user_input)

    writeCache(".prompt", prompt)
    return prompt


local_model_name = os.getenv("LOCAL_MODEL")
if local_model_name and not os.path.exists(local_model_name):
    hf_hub_download(repo_id=local_model_name, filename="unsloth.Q8_0.gguf", local_dir=".")
local_model = Llama("unsloth.Q8_0.gguf", n_ctx=16384) if local_model_name else None

online_model = ChatTogether(
    # model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    # model="meta-llama/Llama-Vision-Free-Form-2B",
    model="meta-llama/Llama-Vision-Free",
    # model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
    # model="google/gemma-2b-it",
    temperature=0.8,
    max_tokens=1024,
)


# generate response
def generate_response(prompt) -> str:
    if local_model:
        chat_history = [
            {
                "role": "system",
                "content": "Sau đây là một cuộc trò chuyện với một trợ lý AI. Trợ lý này hữu ích, thông minh, thân thiện và trả lời súc tích, chuẩn xác.",
            },
            {"role": "user", "content": prompt},
        ]
        response: CreateChatCompletionResponse = local_model.create_chat_completion(
            chat_history, temperature=1.5, min_p=0.1
        )
        if response and "choices" in response and response["choices"]:
            return response["choices"][0].get("message", {}).get("content", "") or ""
        return ""
    else:
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
        response_online = model.invoke(prompt).content
        return response_online


def design_prompt_raft(results: List[Tuple[Document, float]], user_input) -> str:
    context = ""

    for tuple in results:
        context += "<DOCUMENT>" + tuple[0].page_content.strip() + "</DOCUMENT>\n"

    context += user_input

    return context
