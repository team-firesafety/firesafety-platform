import json
from fastapi import HTTPException
from openai import OpenAI
from ..config import settings
from ..core.constants import FeatureID
from ..core.function_setup import TOOLS, SYSTEM_PROMPT
from .features import (
    feature_1_visualization,
    feature_2_doc_pdf,
    feature_3_map_predict,
    feature_4_general_chat,
)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def call_llm_and_route(query: str):
    chat_resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0,
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

    tool_call = msg.tool_calls[0]
    tool_name = tool_call.function.name
    try:
        tool_args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError:
        tool_args = {}

    user_query = tool_args.get("query", query)

    if tool_name == "visualize_data":
        return int(FeatureID.VISUALIZATION), feature_1_visualization(user_query)
    elif tool_name == "generate_official_doc_pdf":
        return int(FeatureID.DOC_PDF), feature_2_doc_pdf(user_query)
    elif tool_name == "predict_fire_risk_map":
        return int(FeatureID.MAP_PREDICT), feature_3_map_predict(user_query)
    else:
        return int(FeatureID.GENERAL_CHAT), feature_4_general_chat(user_query)
