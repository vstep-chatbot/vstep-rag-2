from typing import List

import gradio as gr
from llama_cpp import ChatCompletionRequestMessage, Llama

from utils.database import get_instance, get_top_k_chunks
from utils.prompt import design_prompt_raft
from utils.setup_chroma_db import setup_chroma_db
from utils.vncorenlp_tokenizer import word_segment

setup_chroma_db()

model = Llama(
    model_path="unsloth.Q8_0.gguf",
    n_ctx=8192,
)


def generate_response_local(chat_history: List[ChatCompletionRequestMessage]):
    return model.create_chat_completion(chat_history, stream=True)


with gr.Blocks() as demo:
    with gr.Row():
        results = gr.State([])

        with gr.Column():
            chroma_db = get_instance()

            gr.Markdown("## Chat with the VSTEP support bot")

            chatbot = gr.Chatbot(type="messages")
            msg = gr.Textbox(label="Ask here", info="Press Shift + ↵ (enter) to send", submit_btn=True, lines=2)
            clear = gr.ClearButton([msg, chatbot])

            def respond(message, chat_history: List[ChatCompletionRequestMessage]):
                chat_history = chat_history or [
                    {
                        "role": "system",
                        "content": "Bạn là nhân viên hỗ trợ cho kỳ thi VSTEP, bạn trả lời câu hỏi và thuyết phục user đăng ký thi VSTEP.",
                    }
                ]

                segmented_input = word_segment(message)

                local_results = get_top_k_chunks(chroma_db, segmented_input, k=5)
                # sorted_results = rerank_results(results, segmented_input)
                prompt = design_prompt_raft(local_results, message)

                temp_history = chat_history + [{"role": "user", "content": prompt}]

                chat_history.append({"role": "user", "content": message})

                chat_history.append({"role": "assistant", "content": ""})
                for chunk in generate_response_local(temp_history):
                    content_piece = chunk["choices"][0]["delta"].get("content", "")
                    if content_piece:
                        chat_history[-1]["content"] += content_piece
                        yield "", chat_history, local_results

            msg.submit(respond, [msg, chatbot], [msg, chatbot, results])

        with gr.Column(variant="panel"):
            gr.Markdown("## Documents used for response")

            @gr.render(inputs=results)
            def show_documents(found_documents):
                gr.Markdown(f"> k={len(found_documents)}", height=50)
                for doc in found_documents:
                    gr.Markdown(doc[0].page_content.strip(), container=True, label=str(doc[1]), max_height=250)


demo.launch()
