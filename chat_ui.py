from re import I
from typing import List
import gradio as gr
from llama_cpp import ChatCompletionRequestMessage, Llama

from utils.database import get_instance, get_top_k_chunks
from utils.prompt import design_prompt_raft

model = Llama(
    model_path="models/unsloth.Q8_0.gguf",
    n_ctx=8192,
)


def generate_response_local(chat_history: List[ChatCompletionRequestMessage]):
    response = model.create_chat_completion(chat_history)
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

                local_results = get_top_k_chunks(chroma_db, message, 3)
                prompt = design_prompt_raft(local_results, message)

                chat_history.append({"role": "user", "content": prompt})

                response = generate_response_local(chat_history)

                output = response["choices"][0]["message"]

                if output is not None:
                    chat_history.pop()
                    chat_history.append({"role": "user", "content": message})
                    chat_history.append(output)

                return "", chat_history, local_results

            msg.submit(respond, [msg, chatbot], [msg, chatbot, results])

        with gr.Column(variant="panel"):
            gr.Markdown("## Documents used for response")

            @gr.render(inputs=results)
            def show_documents(found_documents):
                gr.Markdown(f"> k={len(found_documents)}", height=50)
                for doc in found_documents:
                    gr.Markdown(doc[0].page_content.strip(), container=True, label=str(doc[1]), max_height=250)


demo.launch()
