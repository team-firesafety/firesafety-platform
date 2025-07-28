from fastapi import APIRouter
from .endpoints import fire_patrol


api_router = APIRouter()

api_router.include_router(fire_patrol.router, prefix="/patrol")