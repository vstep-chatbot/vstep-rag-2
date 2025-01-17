import json
import logging
import os

from datasets import load_dataset
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from utils.database import get_instance, get_top_k_chunks
from utils.prompt import design_prompt_raft
from utils.reranker import rerank_results
from utils.setup_chroma_db import setup_chroma_db
from utils.vncorenlp_tokenizer import word_segment

# Setup the database and dataset
setup_chroma_db()
chroma_db = get_instance()

ds = load_dataset("hainam2410/vstep_raft", split="test")
logging.info(f"Loaded dataset with {len(ds)} examples.")


# Setup the model
local_model_name = os.getenv("LOCAL_MODEL")
if local_model_name and not os.path.exists(local_model_name):
    hf_hub_download(repo_id=local_model_name, filename="unsloth.Q8_0.gguf", local_dir=".")
local_model = Llama("unsloth.Q8_0.gguf", n_ctx=16392)


outfile = open("output.json", "w")

# Main loop
iter= ds.iter(batch_size=1)
for ex in iter:
    chat_history = [
        {
            "role": "system",
            "content": "Bạn là nhân viên hỗ trợ cho kỳ thi VSTEP, bạn trả lời câu hỏi và thuyết phục user đăng ký thi VSTEP.",
        }
    ]
    input = ex["messages"][0][1].get("content", None).split("</DOCUMENT>\n")[-1]
    print(input)

    segmented_input = word_segment(input)
    search_results = get_top_k_chunks(chroma_db, segmented_input, k=10)

    sorted_results = rerank_results(search_results, segmented_input)
    sorted_results = sorted_results[:5]

    prompt = design_prompt_raft(sorted_results, input)

    print([r[1] for r in sorted_results])

    chat_history.append({"role": "user", "content": prompt})

    print(chat_history)
    response = local_model.create_chat_completion(chat_history)
    output = {
          "input": input,
          "chunks": [[r[1], r[0].page_content] for r in sorted_results],
          "response": response.get("choices",[{}])[0].get("message", {}).get("content", ""),
          "gold_ans": ex["messages"][1][1].get("content", None).split("<ANSWER>: ")[-1]
        }
    outfile.write(json.dumps(output, indent=2) + ",\n")
    print(response, '\n')
