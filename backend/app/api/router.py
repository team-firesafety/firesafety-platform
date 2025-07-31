from fastapi import APIRouter
from .endpoints import fire_patrol
from .endpoints.chat import router as chat_router


api_router = APIRouter()

api_router.include_router(fire_patrol.router, prefix="/patrol")

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)