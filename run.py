from fastapi import FastAPI
from server.router import router

app = FastAPI(
    title="AI Chatbot",
    description="A Basic Chatbot with Image Generation",
    version="1.0.0"
)

# Include the router from routes.py
app.include_router(router)

# Root endpoint
@app.get("/")
async def root():
    # list all routes
    return {"routes": app.routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
