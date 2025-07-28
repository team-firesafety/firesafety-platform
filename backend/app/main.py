from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import api_router

app = FastAPI(title="Fire Safety Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
