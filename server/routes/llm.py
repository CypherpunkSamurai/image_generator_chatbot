# llm.py
import os
from openai import AsyncOpenAI
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
# log
from logger import logger

# OpenAI Configurations
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")

# log
logger.debug(f"Base URL: {OPENAI_BASE_URL}")
logger.debug(f"API Key: {OPENAI_API_KEY}")
logger.debug(f"Default Model: {OPENAI_DEFAULT_MODEL}")

# OpenAI Client Instance
async_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)
# Router
router = APIRouter(
    prefix="/chat",
    tags=["Chat", "ChatCompletion", "LLM"],
    responses={404: {"description": "Not found"}},
)
