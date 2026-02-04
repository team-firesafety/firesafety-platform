# app/services/function_caller.py
import json
from openai import AsyncOpenAI
from fastapi import HTTPException
from openai import OpenAI
from ..config import settings
from ..core.constants import FeatureID
from ..core.function_setup import TOOLS, SYSTEM_PROMPT
from .features import (
    feature_1_visualization,
    feature_2_doc_pdf,
    feature_3_map_predict,
)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def call_llm_and_route(query: str):
    """
    LLM에 '어떤 기능을 쓸지'만 판단시킨 뒤 결과 리턴.
    - 기능 1·2·3: 실제 데이터까지 계산해서 반환
    - 기능 4    : 데이터 계산 X (RAG + 스트림을 엔드포인트에서 처리)
    """
    chat_resp = await client.chat.completions.create(  # await 사용
        model=settings.OPENAI_MODEL,
        temperature=0,
        timeout=50,
        tool_choice="auto",
        tools=TOOLS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )
    msg = chat_resp.choices[0].message

    if not msg.tool_calls:
        raise HTTPException(status_code=500, detail="LLM이 어떤 기능도 선택하지 않았습니다.")

    tool_call  = msg.tool_calls[0]
    tool_name  = tool_call.function.name
    try:
        tool_args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError:
        tool_args = {}

    user_query = tool_args.get("query", query)

    # ───────── 기능 분기 ─────────
    if tool_name == "visualize_data":
        return int(FeatureID.VISUALIZATION), feature_1_visualization(user_query)

    elif tool_name == "generate_official_doc_pdf":
        return int(FeatureID.DOC_PDF), feature_2_doc_pdf(user_query)

    elif tool_name == "predict_fire_risk_map":
        data = await feature_3_map_predict(user_query)
        return int(FeatureID.MAP_PREDICT), data

    # 기능 4 : JSON 데이터는 만들지 않고, 번호만 돌려줍니다.
    return int(FeatureID.GENERAL_CHAT), None
