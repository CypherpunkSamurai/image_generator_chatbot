# routes.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
# add routes
from server.routes.llm import router as llm_router

# api v1
router = APIRouter(
    prefix="/api/v1",
    tags=["API V1"],
    responses={404: {"description": "Not found"}},
)
# add sub routes
router.include_router(llm_router)

@router.get("/health")
async def health():
    return {"status": "ok"}
