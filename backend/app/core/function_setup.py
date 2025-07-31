# OpenAI Function Calling 도구 정의
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "visualize_data",
            "description": "기능 1) 데이터 시각화: NL2SQL→DB조회→차트/표/3D 시각화 흐름.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "사용자 원문 요청"},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_official_doc_pdf",
            "description": "기능 2) 공문서 제작: 양식 이미지+텍스트→레이아웃 매핑→PDF 생성.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "사용자 원문 요청"},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "predict_fire_risk_map",
            "description": "기능 3) 화재 발생 구간 예측 지도: 현위치 기반 핫스팟/최단경로 추천.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "사용자 원문 요청"},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "general_fire_chat",
            "description": "기능 4) 일반 대화: 소방 일반 지식/RAG 기반 응답.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "사용자 원문 요청"},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]

SYSTEM_PROMPT = """
너는 '소방안전 빅데이터 활용 챗봇'의 라우팅 에이전트야.
사용자의 한국어 질의(query)를 보고 아래 4개 기능 중 '정확히 하나'의 function만 호출해.
- visualize_data: 데이터 시각화 관련 요청
- generate_official_doc_pdf: 공문서 생성 요청
- predict_fire_risk_map: 화재 위험 구간 지도 요청
- general_fire_chat: 그 외 일반 대화

규칙:
1) 반드시 도구(function) 호출을 사용해.
2) 4개 중 하나만 선택해 호출.
3) 인자로는 원문 query만 그대로 넣어.
"""