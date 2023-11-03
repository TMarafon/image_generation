import os
import random # remove this line after removing the example

import openai

import gradio as gr


def init_auth():
    global authenticated
    globals()['authenticated'] = False

async def generate_image(prompt:str):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        
        result = response['data']
        print(result)
        return [result[0]['url']]
    except Exception as e:
        gr.Warning(e)
        return ["Error"]

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

async def generate_text(text_system, text_prompt, max_tokens: int, text_model: str, temperature: float):
    if not globals()['authenticated']:
        gr.Warning("Please enter a valid API key")
        return
    
    if not text_prompt:
        gr.Warning("Please enter your prompt")
        return

    print()
    print("Inference parameters:")
    print(text_system, text_prompt, max_tokens, text_model, temperature)
    print()
    print()

    try:
        creation = openai.ChatCompletion.create(
            model=text_model,
            messages=get_prompt(text_system, text_prompt),
            temperature=temperature,
            max_tokens=max_tokens,
        )

        print(creation)
        return creation.choices[0].message.content
    except Exception as e:
        gr.Warning(e)
        return "Error"

async def save_key(api_key):
    try:
        openai.api_key = api_key
        openai.Model.list()
        globals()['authenticated'] = True
        print(globals()['authenticated'])
    except Exception as e:
        gr.Warning("Invalid API key")

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

with gr.Blocks(title="Generate Text and Images", theme=theme) as demo:
    with gr.Column(variant="panel"):
        with gr.Row():
            gr.Label("Generate Text and Images", container=False,)
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
                        interactive=True
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

                with gr.Row():
                    api_key = gr.Textbox(
                        type="password",
                        label="OpenAI API Key",
                        scale=5,
                        container=True,
                    )
                with gr.Row():
                    save_key_btn = gr.Button(
                        value="Save",
                        size="sm",
                        scale=1,
                    )
            

    try: 
        btn_img.click(generate_image, output, gallery)
        btn_txt.click(
            fn=generate_text,
            inputs=[text_system,text_prompt,max_tokens, text_model, temperature], 
            outputs=output,
            batch=False,
            trigger_mode="once",
            show_progress=True,
        )
        save_key_btn.click(
            fn=save_key,
            inputs=[api_key], 
            outputs=None,
            batch=False,
            trigger_mode="once",
            show_progress=True,
        )
    except Exception as e:
        gr.Warning(e)

if __name__ == "__main__":
    init_auth()
    demo.launch()