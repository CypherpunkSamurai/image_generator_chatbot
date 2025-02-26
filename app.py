# app
import logging

from fastapi import FastAPI
from src.router import router

# print langchain version
print("Langchain Version: 0.2.0")

# debug logger
logging.basicConfig(level=logging.DEBUG)

# create a simple
app = FastAPI(
    title="FastAPI",
    description="A REST API.",
)
app.include_router(router)


@app.get("/health")
async def health():
    """Health Check

    Returns:
        dict: A dictionary with the status of the service.
    """
    return {"status": "ok"}
