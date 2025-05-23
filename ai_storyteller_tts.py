# -*- coding: utf-8 -*-
"""AI_STORYTELLER_TTS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I1o8NMZ8t7H-ygzeDFZjt4HaYO8a-1_G
"""

!pip install gradio edge-tts

import gradio as gr
import requests
import edge_tts
import tempfile
import asyncio

# ========= CONFIGURATION =========
GROQ_API_KEY = "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"
MODEL_NAME = "llama3-70b-8192"

ENGLISH_SPEAKERS = {
    "Jenny": "en-US-JennyNeural",
    "Guy": "en-US-GuyNeural",
    "Aria": "en-US-AriaNeural"
}

# ========= STORY GENERATION =========
def generate_story(plot: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a master storyteller. Create vivid, imaginative, emotional, and captivating stories."},
            {"role": "user", "content": f"Write a detailed story based on this plot: {plot}"}
        ],
        "temperature": 0.9,
        "max_tokens": 1500
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ========= TEXT TO SPEECH =========
async def edge_tts_async(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        await communicate.save(tmp_file.name)
        return tmp_file.name

def generate_story_and_audio(plot, speaker_name):
    voice = ENGLISH_SPEAKERS[speaker_name]
    story = generate_story(plot)
    audio_path = asyncio.run(edge_tts_async(story, voice))
    return story, audio_path

# ========= UI =========
with gr.Blocks(title="AI Storyteller") as demo:
    gr.Markdown("# ✨ LoreLoom – Weaves tales of old and new, just like a magical loom ")
    gr.Markdown("From a simple plot to a spellbinding story – hear your dreams come alive!")

    with gr.Row():
        with gr.Column():
            plot = gr.Textbox(label="Enter Your Plot", placeholder="e.g. A child finds a dragon egg in their backyard...", lines=5)
            speaker = gr.Dropdown(choices=list(ENGLISH_SPEAKERS.keys()), value="Jenny", label="Choose Voice")
            generate_btn = gr.Button("Generate Story & Narration 🎙️")
        with gr.Column():
            story_output = gr.Textbox(label="🧚‍♀️ The Fantasy You Wrote", lines=12, interactive=False)
            audio_output = gr.Audio(label="🔮 Narration from the LoomaRealm", type="filepath")

    gr.Examples(
        examples=[
            ["A young inventor builds a time machine in their garage.", "Aria"],
            ["An astronaut gets stranded on an alien planet full of surprises.", "Guy"],
            ["A talking cat leads a girl on a magical treasure hunt.", "Jenny"]
        ],
        inputs=[plot, speaker],
        label="Example Prompts"
    )

    generate_btn.click(fn=generate_story_and_audio, inputs=[plot, speaker], outputs=[story_output, audio_output])

demo.launch()