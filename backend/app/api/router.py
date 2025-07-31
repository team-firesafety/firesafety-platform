from fastapi import APIRouter
from .endpoints import fire_patrol
from .endpoints.chat import router as chat_router
from .endpoints.pdf_download import router as pdf_router


api_router = APIRouter()

api_router.include_router(fire_patrol.router, prefix="/patrol")

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)

# PDF 다운로드 기능
api_router.include_router(
    pdf_router,
    prefix="/pdf",
    tags=["PDF"],
)
