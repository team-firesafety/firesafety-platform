from typing import Dict, Any
import time
import re, asyncio
CENTER_RE = re.compile(r"([\w가-힣]+)\s*119\s*안전센터")
from .rag_chat import get_full_answer
import re
from .mock_firestation_service import get_buildings_by_station   # ← 변경

ST_RE = re.compile(r"([\w가-힣]+)\s*소방서")   # “종로소방서” 등

def feature_1_visualization(query: str) -> Dict[str, Any]:
    """데이터 시각화 기능 - 자연어로 소방 안전 데이터 조회"""
    try:
        from .visualization_query_service import VisualizationQueryService
        from ..core.visualization_database import get_visualization_db_session
        
        # 데이터베이스 세션 생성
        db = get_visualization_db_session()
        
        try:
            # 쿼리 서비스 초기화
            query_service = VisualizationQueryService(db)
            
            # 자연어 쿼리 실행
            result = query_service.execute_natural_language_query(
                question=query,
                dataset_type=None,  # 자동 추론
                limit=100
            )
            
            return result
            
        finally:
            db.close()
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"데이터 시각화 기능 실행 중 오류: {str(e)}"
        }


def feature_2_doc_pdf(query: str) -> Dict[str, Any]:
    time.sleep(3)
    # PDF 생성
    filename = "document.pdf"
    # 다운로드 엔드포인트를 가리키는 URL 반환
    return {
        "pdf_filename": filename,
        "download_url": f"/pdf/download/{filename}",
    }


async def feature_3_map_predict(query: str) -> Dict[str, Any]:
    """
    화재 예측 지도 → 소방서 위치 + 건물 리스트 반환 (MOCK)
    """
    m = ST_RE.search(query)
    # 소방서 언급이 없으면 그래도 종로소방서 데이터 반환
    station = (m.group(1) + "소방서") if m else "종로소방서"

    station_info, buildings = await get_buildings_by_station(station)

    return {
        "station": station_info,                                # {name, lon, lat}
        "buildings": [b.model_dump(by_alias=True) for b in buildings],
    }


def feature_4_general_chat(query: str) -> Dict[str, Any]:
    """
    Function‑Calling 라우팅(`/chat`)을 통해 호출될 때 사용됩니다.
    - 요구 사항: **JSON 한 덩어리**로 응답
    - 그래서 stream 대신 get_full_answer()로 ‘완결형 텍스트’를 생성합니다.
    """
    answer = get_full_answer(query)
    return {"message": answer}