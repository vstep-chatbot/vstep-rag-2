import json

import gradio as gr


def load_output():
    with open("evaluation/output_raft_sgu.json", "r") as f:
        return json.loads("[" + f.read()[:-2] + "]")


with gr.Blocks(fill_width=True) as demo:
    full_data = gr.State(load_output())
    current_example = gr.State({})
    current_index = gr.State(-1)

    with gr.Row():
        with gr.Column(scale=2):

            @gr.render(inputs=current_example)
            def show_question_and_answer(current_set):
                input = current_set.get("input", "")
                full_ans_1 = current_set.get("full_ans_1", "")
                gold_ans_1 = current_set.get("gold_ans_1", "")
                gold_ans_2 = current_set.get("gold_ans_2", "")

                gr.Markdown("## " + input)
                gr.TextArea(full_ans_1, container=True, label="RAFT Full answer")
                gr.Markdown("### RAFT Answer\n" + gold_ans_1, container=True, label="gold_ans_1")
                gr.Markdown("### Llama 3.2 3B\n" + gold_ans_2, container=True, label="gold_ans_2")

        with gr.Column(variant="panel", scale=2):
            gr.Markdown("## Documents used for response")

            @gr.render(inputs=current_example)
            def show_documents(example):
                chunks = example.get("chunks", [])
                gr.Markdown(f"> k={len(chunks)}", height=50)
                for doc in chunks:
                    gr.Textbox(str(doc[1]), label=str(doc[0]), max_lines=10)

        with gr.Column(scale=1):
            with gr.Blocks():

                def to_index(index, full_data):
                    index = max(0, min(index, len(full_data) - 1))
                    return [index - 1, full_data[index - 1]]

                num_input = gr.Number(label="Go to example", minimum=1)
                gr.Button("To index").click(to_index, [num_input, full_data], [current_index, current_example])

            with gr.Blocks():

                @gr.render(inputs=[current_index, full_data])
                def show_index(current_index, full_data):
                    gr.Markdown(f"Example **{current_index + 1}** of **{len(full_data)}**", height=50)

            with gr.Column():

                def to_start(current_index, current_example, full_data):
                    return [0, full_data[0]]

                def to_end(current_index, current_example, full_data):
                    return [len(full_data) - 1, full_data[-1]]

                def next_example(current_index, current_example, full_data):
                    next_index = (current_index + 1) % len(full_data)
                    return [next_index, full_data[next_index]]

                def prev_example(current_index, current_example, full_data):
                    prev_index = (current_index - 1) % len(full_data)
                    return [prev_index, full_data[prev_index]]

                gr.Button("<| First").click(
                    to_start, [current_index, current_example, full_data], [current_index, current_example]
                )
                gr.Button("<< Previous").click(
                    prev_example, [current_index, current_example, full_data], [current_index, current_example]
                )
                gr.Button("Next >>").click(
                    next_example, [current_index, current_example, full_data], [current_index, current_example]
                )
                gr.Button("Last |>").click(
                    to_end, [current_index, current_example, full_data], [current_index, current_example]
                )

demo.launch()
