import os
import random # remove this line after removing the example

import openai

import gradio as gr

openai.api_key = os.environ["OPENAI_API_KEY"]

def fake_gan():
    images = [
        (random.choice(
            [
                "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
                "https://images.unsplash.com/photo-1554151228-14d9def656e4?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=386&q=80",
                "https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8aHVtYW4lMjBmYWNlfGVufDB8fDB8fA%3D%3D&w=1000&q=80",
                "https://images.unsplash.com/photo-1546456073-92b9f0a8d413?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80",
                "https://images.unsplash.com/photo-1601412436009-d964bd02edbc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=464&q=80",
            ]
        ), f"label {i}" if i != 0 else "label" * 50)
        for i in range(3)
    ]
    return images

def get_prompt(text_system: str, query: str) -> list:
    return [
        {
            "role": "system",
            "content": f"""{text_system}""",
        },
        {
            "role": "user",
            "content": f"""{query}""",
        }
    ]

def generate_text(text_system, text_prompt, max_tokens: int, text_model: str, temperature: float):
    print(text_system, text_prompt, max_tokens, text_model, temperature)

    creation = openai.ChatCompletion.create(
        model=text_model,
        messages=get_prompt(text_system, text_prompt),
        temperature=temperature,
        max_tokens=max_tokens,
    )

    print(creation)
    return creation.choices[0].message.content

# APP
theme = gr.themes.Monochrome(
    font=[gr.themes.GoogleFont("Kanit"), "sans-serif"],
)

system_examples = [
    "You are a exceptional artist who can express special moments in words and images.",
]

prompt_examples = [
    "Generate an image about soccer and kids.",
    "Describe an image about soccer and kids.",
]

text_models = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-4",
]

with gr.Blocks(title="Fake Gan", theme=theme) as demo:
    with gr.Column(variant="panel"):
        with gr.Row():
            with gr.Column(variant="panel", scale=3):
                with gr.Row():
                    text_system = gr.Textbox(
                        label="Enter your system",
                        max_lines=10,
                        placeholder="Enter your system",
                        container=False,
                        lines=3,
                    )
                    text_prompt = gr.Textbox(
                        label="Enter your prompt",
                        max_lines=10,
                        placeholder="Enter your prompt",
                        container=False,
                        lines=3,
                    )
                with gr.Row():
                    output = gr.Textbox(
                        max_lines=10,
                        container=False,
                        lines=10,
                    )

                gallery = gr.Gallery(
                    label="Generated images", show_label=False, elem_id="gallery"
                , columns=[2], rows=[2], object_fit="contain", height="auto")

            with gr.Column(variant="panel"):  
                with gr.Row():  
                    btn_txt = gr.Button("Generate text", scale=0)
                    btn_img = gr.Button("Generate image", scale=0)
                with gr.Row():
                    gr.Examples(
                        examples=system_examples,
                        inputs=[text_system],
                        label="System examples",
                    )
                with gr.Row():
                    gr.Examples(
                        examples=prompt_examples,
                        inputs=[text_prompt],
                        label="Prompt examples",
                    )
                with gr.Row():
                    text_model = gr.Dropdown(
                        label="Text model",
                        choices=text_models,
                        value="gpt-3.5-turbo",
                        container=True,
                    )

                with gr.Row():
                    max_tokens = gr.Number(
                        label="Max tokens",
                        value=200,
                        minimum=1,
                        maximum=500,
                        step=10,
                        container=True,
                        precision=0,
                    )

                with gr.Row():
                    temperature = gr.Slider(
                        label="Temperature",
                        value=1,
                        minimum=0,
                        maximum=1,
                        step=0.1,
                        container=True,
                    )

    btn_img.click(fake_gan, None, gallery)
    btn_txt.click(
        fn=generate_text,
        inputs=[text_system,text_prompt,max_tokens, text_model, temperature], 
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()