from typing import List

import gradio as gr
from llama_cpp import ChatCompletionRequestMessage
from together import Together
from together.types.chat_completions import ChatCompletionChoicesData

from utils.database import get_instance, get_top_k_chunks
from utils.prompt import design_prompt_raft
from utils.setup_chroma_db import setup_chroma_db
from utils.vncorenlp_tokenizer import word_segment

setup_chroma_db()


client = Together()

def create_chat_completion(chat_history: List[ChatCompletionRequestMessage]) -> ChatCompletionChoicesData:
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=chat_history,
        max_tokens=512,
        temperature=0.95,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=True
    )
    return response

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
                for chunk in create_chat_completion(temp_history):
                    if hasattr(chunk, 'choices'):
                      content_piece = chunk.choices[0].delta.content
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
