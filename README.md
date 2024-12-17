---
title: Hexagrams
emoji: ⚡
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
short_description: HexagramAI. Support multiple Languages
---

TEST : https://huggingface.co/spaces/NetRoller/8Trigrams



☯️ Hexagram.AI - I Ching AI Interpretation ☯️
Introduction
Hexagram.AI is an AI-based I Ching platform that interprets divination results using OpenAI API. Built with Gradio, users can ask questions, draw hexagrams, and receive detailed interpretations.

🚀 How to Run
Install Dependencies
Ensure Python version >= 3.8. Run the following command:

bash

pip install -r requirements.txt
Set API Key
Add your OpenAI API key in app3.py:

python

openai.api_key = "YOUR_API_KEY_HERE"
Launch the Application
Run the following command:

bash

python app3.py
Access the App
A local URL (or public shareable link) will be provided. Open it in your browser.

📂 Project Structure
app3.py: Main application with Gradio UI and interpretation logic.
hexagrams.py: Database of I Ching hexagrams.
requirements.txt: List of required dependencies.

🌟 Features
Hexagram Generation: Generate I Ching hexagrams randomly.
Interpretation: Use GPT-4 to provide detailed hexagram explanations.
Language Detection & Translation: Supports multiple languages for explanations.
📸 Preview
Interface includes:

plaintext

Hexagram Generation → Interpretation Display → Auto Language Detection & Translation
