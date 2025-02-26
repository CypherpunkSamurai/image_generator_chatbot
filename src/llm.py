import json
import os
# logger
from logging import getLogger

from fastapi.responses import JSONResponse, StreamingResponse
from langchain.agents import Tool, initialize_agent, load_tools
# langchain tools
from langchain.agents.initialize import initialize_agent
from langchain.schema import HumanMessage
# Langchain History Provider
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.runnables.history import RunnableWithMessageHistory
# Add these imports at the top of llm.py
from langchain_openai import ChatOpenAI

# Models for FastAPI Compatibility
from .models import ChatMessage

# create a logger
logger = getLogger(__name__)

# Configure OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chats.db")

# check env
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY environment variable is not set")
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# tools
search_tool_1 = DuckDuckGoSearchResults()
search_tool_1 = Tool(
    name="DuckDuck search tool",
    description="A web search engine. Use this to search the internet for general queries.",
    func=search_tool_1.run,
)
# Load all tools
# TODO: Figure Out Streaming Tools
LlmToolkit = load_tools(
    ["dalle-image-generator"]
)
LlmToolkit.append(search_tool_1)


async def init_llm(message: ChatMessage, session_id: str):
    # Create a new instance of the LLM
    llm = ChatOpenAI(
        model=message.model,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        temperature=0.7,
        streaming=message.stream
    )

    # Add tools to the llm
    agent = initialize_agent(
        LlmToolkit,
        llm,
        agent="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True
    )

    # Create a message history provider
    chain = RunnableWithMessageHistory(
        agent,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id, connection_string="sqlite:///sqlite.db"
        ),
        connection_string=DATABASE_URL,
        table_name="messages",
    )

    # Configure the agent
    config = {"configurable": {"session_id": session_id}}

    return agent, chain, config


async def generate_stream_response(message: ChatMessage, session_id: str):
    """Generate a stream response for the chat message on the fly"""

    # Initialize the LLM, agent, and message history
    agent, chain, config = await init_llm(message, session_id)

    # Create a human message from the input
    human_message = HumanMessage(content=message.message)

    # Stream the agent's responses with proper message format
    async for chunk in chain.astream(human_message, config=config):
        # Handle different types of agent outputs
        content = None
        if isinstance(chunk, dict) and 'output' in chunk:
            content = chunk['output']
        elif hasattr(chunk, 'content'):
            content = chunk.content
        elif isinstance(chunk, str):
            content = chunk

        if content:
            yield f"data: {json.dumps({'content': content})}\n\n"

    # After streaming is complete, save to history
    logger.info(f"Completed stream response for session {session_id}")


async def generate_complete_response(message: ChatMessage, session_id: str):
    """Generate a complete response for the chat message"""
    # Create a new instance of the LLM
    agent, chain, config = await init_llm(message, session_id)

    # Create a human message from the input
    human_message = HumanMessage(content=message.message)

    # Get the response from the chain with proper message format
    response = await chain.ainvoke(human_message, config=config)

    # Return the response content (adjust based on actual response format)
    if isinstance(response, dict) and 'output' in response:
        return response['output']
    return response


async def chat_complete(message: ChatMessage, session_id: str) -> JSONResponse | StreamingResponse:
    """
    Handle chat completion.
    If streaming is requested, returns a StreamingResponse.
    Otherwise, returns a JSONResponse.
    """
    if message.stream:
        # If it's a streaming response, create and return a StreamingResponse
        return StreamingResponse(
            generate_stream_response(message, session_id),
            media_type="text/event-stream"
        )
    else:
        # If it's not streaming, await the complete response and return as JSON
        response = await generate_complete_response(message, session_id)
        return JSONResponse(content=response)
