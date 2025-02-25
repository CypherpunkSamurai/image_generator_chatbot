# app
from fastapi import FastAPI

# create a simple
app = FastAPI(
    title="FastAPI",
    description="A REST API.",
)

@app.get("/health")
async def health():
    """Health Check

    Returns:
        dict: A dictionary with the status of the service.
    """
    return {"status": "ok"}
