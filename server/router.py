# routes.py
from fastapi import APIRouter

# api v1
router = APIRouter(
    prefix="/api/v1",
    tags=["API V1"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health")
async def health():
    return {"status": "ok"}
