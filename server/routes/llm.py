# llm.py
import os
from openai import OpenAI

# OpenAI Configurations
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")

# OpenAI Client Instance
client = OpenAI(
  base_url=OPENAI_BASE_URL,
  api_key=OPENAI_API_KEY,
)

def chat_completion_llm(messages: any, model: str=OPENAI_DEFAULT_MODEL):
    """chat completion"""
    return client.chat.completions.create(
        model=model,
        messages=messages
    )
