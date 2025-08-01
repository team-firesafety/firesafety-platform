from typing import Dict, Any
import time
from .building_service import get_buildings_by_station

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
    예) '종로 소방서 화재 예측 지도 그려줘' → station='종로소방서'
    간단 문자열 파싱만(공백 제거) 적용
    """
    station = query.split(" ")[0].replace(" ", "")
    data = await get_buildings_by_station(station)
    # pydantic 모델 → dict 로 시리얼라이즈
    return {"station": station, "buildings": [b.dict(by_alias=True) for b in data]}


def feature_4_general_chat(query: str) -> Dict[str, Any]:
    return {"message": f"4번 기능 호출, 입력 쿼리: {query}"}