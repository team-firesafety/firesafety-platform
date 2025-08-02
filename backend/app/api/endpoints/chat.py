# app/api/endpoints/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from ...schemas.chat_request import ChatRequest
from ...core.constants import FeatureID
from ...services.function_caller import call_llm_and_route
from ...services.rag_chat import stream_answer     # ← SSE 제너레이터

router = APIRouter()

@router.post("", summary="LLM Function Calling 기반 챗팅 라우터")
async def route_chat(req: ChatRequest):
    """
    POST /chat
    ───────────────────────────────────────────────
    · 기능 1·2·3  → application/json  (한 덩어리)
    · 기능 4      → text/event-stream (SSE 글자 단위)
    ⇒ 프런트는 response.headers['content-type'] 만 보고 분기
    """
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query는 비어 있을 수 없습니다.")

    # LLM에게 기능 분류 + 1·2·3 결과(필요 시)까지 받아옴
    fn_no, data = await call_llm_and_route(req.query)

    # ── 기능 4 : SSE 스트리밍 응답 ──────────────────────────
    if fn_no == int(FeatureID.GENERAL_CHAT):
        return StreamingResponse(
            stream_answer(req.query),
            media_type="text/event-stream",
        )

    # ── 기능 1·2·3 : JSON 한 덩어리 응답 ───────────────────
    return JSONResponse(
        status_code=200,
        content={
            "functionNo": fn_no,
            "data": data,
        },
    )
