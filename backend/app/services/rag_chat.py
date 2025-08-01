# app/services/rag_chat.py
"""
🔥 RAG(검색 기반 생성) 서비스 모듈
────────────────────────────────────────────────────────────────────────
1) stream_answer(query)  : 글자 단위 SSE 스트림 전송 (Markdown 포함)
2) get_full_answer(query): 완결형 Markdown 문자열 반환 (JSON 응답용)
────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from typing import Generator

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from ..config import settings

# ------------------------------------------------------------------- #
# [1] ❶ FAISS 인덱스 로드 (backend/vectorstore_FAISS)                  #
# ------------------------------------------------------------------- #
BASE_DIR   = Path(__file__).resolve().parents[2]      # …/backend
INDEX_DIR  = BASE_DIR / "vectorstore_FAISS"           # …/backend/vectorstore_FAISS

@lru_cache(maxsize=1)
def _load_vectorstore() -> FAISS:
    """
    최초 1회만 메모리에 인덱스 적재.
    """
    embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
    return FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

# ------------------------------------------------------------------- #
# [2] ❷ 공통 프롬프트 (Markdown 지시 추가)                             #
# ------------------------------------------------------------------- #
SYSTEM_PROMPT_MD = (
    "당신은 **화재·피난·방폭** 등 한국형 소방안전기술을 안내하는 전문 챗봇입니다.\n"
    "아래 '참고 문서'를 최우선으로 활용해 **한국어**로 답하십시오.\n\n"
    "### 마크다운 작성 지침\n"
    "1. 제목/소제목: `##`, `###` 헤더 사용\n"
    "2. 중요한 단어: **굵게**, *기울임* 등 강조\n"
    "3. 표·코드블록( ``` )을 적극 활용해 가독성 향상\n"
    "4. 불필요한 수식어·과장은 삼가고, 정확한 기준·조항을 명시\n"
)

# ------------------------------------------------------------------- #
# [3] ❸ 글자 단위 SSE 제너레이터                                     #
# ------------------------------------------------------------------- #
def stream_answer(query: str) -> Generator[str, None, None]:
    """
    StreamingResponse(media_type='text/event-stream') 용.
    LLM 델타를 한 글자씩 'data: …\\n\\n' 로 분할해 타자기 효과 구현.
    """
    # 3‑1) RAG 검색 (Top‑4)
    retriever   = _load_vectorstore().as_retriever(search_type="similarity", k=4)
    docs        = retriever.invoke(query)
    context     = "\n\n-----\n\n".join(d.page_content for d in docs)

    # 3‑2) OpenAI 스트리밍 호출 (Markdown 지시 포함)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    stream = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0.2,
        stream=True,
        messages=[
            {"role": "system",    "content": SYSTEM_PROMPT_MD},
            {"role": "assistant", "content": f"[참고 문서]\n{context}"},
            {"role": "user",      "content": query},
        ],
    )

    # 3‑3) 한 글자씩 SSE 전송
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        for ch in delta:
            yield f"data: {ch}\n\n"
    yield "data: [DONE]\n\n"

# ------------------------------------------------------------------- #
# [4] ❹ 완결형 Markdown 문자열                                        #
# ------------------------------------------------------------------- #
def get_full_answer(query: str) -> str:
    """
    기능 4를 JSON 한 덩어리로 반환해야 할 때 사용.
    (현재 /chat 엔드포인트는 SSE를 직접 내려주므로 예비용)
    """
    retriever   = _load_vectorstore().as_retriever(search_type="similarity", k=4)
    docs        = retriever.invoke(query)
    context     = "\n\n-----\n\n".join(d.page_content for d in docs)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system",    "content": SYSTEM_PROMPT_MD},
            {"role": "assistant", "content": f"[참고 문서]\n{context}"},
            {"role": "user",      "content": query},
        ],
    )
    return resp.choices[0].message.content
