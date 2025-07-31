# app/api/endpoints/chat.py
from fastapi import APIRouter, HTTPException
from ...schemas.chat_request import ChatRequest
from ...schemas.chat_response import ChatResponse
from ...services.function_caller import call_llm_and_route

router = APIRouter()

@router.post(
    "", 
    response_model=ChatResponse, 
    summary="LLM Function Calling 기반 챗팅 라우터"
)
async def route_chat(req: ChatRequest):
    """
    POST /chat
    - body: {"query": "..."}
    - LLM이 4개 기능 중 하나를 호출 → 내부 서비스 실행 → 결과 반환
    """
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query는 비어 있을 수 없습니다.")
    fn_no, data = await call_llm_and_route(req.query)
    return {"functionNo": fn_no, "data": data}
