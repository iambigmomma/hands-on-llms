import argparse
import logging
import json
import requests
import gradio as gr
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables from .env file
load_dotenv()

# Configuration of the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parseargs():
    """ Parses command line arguments for the Financial Assistant Bot. """
    parser = argparse.ArgumentParser(description="Financial Assistant Bot")
    return parser.parse_args()

# API Request setup using environment variables
url = f"https://{os.getenv('BEAM_DEPLOYMENT_ID')}.apps.beam.cloud"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Authorization": f"Basic {os.getenv('BEAM_AUTH_TOKEN')}",
    "Connection": "keep-alive",
    "Content-Type": "application/json"
}

def predict(message: str, history: List[List[str]], about_me: str) -> str:
    """ Generates responses from the API endpoint. """
    payload = {"about_me": about_me, "question": message, "to_load_history": history}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"API Error: {response.status_code}")
        return "Sorry, I couldn't fetch a response. Please try again."

# Setup the Gradio interface
demo = gr.ChatInterface(
    fn=predict,
    textbox=gr.Textbox(
        placeholder="Ask me a financial question",
        label="Financial question",
        container=False,
        scale=7,
    ),
    additional_inputs=[
        gr.Textbox(
            "I am a student and I have some money that I want to invest.",
            label="About me",
        )
    ],
    title="Your Personal Financial Assistant",
    description="Ask me any financial or crypto market questions, and I will do my best to answer them.",
    theme="soft",
    examples=[
        [
            "What's your opinion on investing in startup companies?",
            "I am a 30 year old graphic designer. I want to invest in something with potential for high returns.",
        ],
        [
            "What's your opinion on investing in AI-related companies?",
            "I'm a 25 year old entrepreneur interested in emerging technologies. \
             I'm willing to take calculated risks for potential high returns.",
        ],
        [
            "Do you think advancements in gene therapy are impacting biotech company valuations?",
            "I'm a 31 year old scientist. I'm curious about the potential of biotech investments.",
        ],
    ],
    cache_examples=False,
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear",
)

if __name__ == "__main__":
    args = parseargs()
    # demo.queue().launch()
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=True)

