from typing import Dict, Any
from .building_service import get_buildings_by_station

def feature_1_visualization(query: str) -> Dict[str, Any]:
    return {"message": f"1번 기능 호출, 입력 쿼리: {query}"}


def feature_2_doc_pdf(query: str) -> Dict[str, Any]:
    return {"message": f"2번 기능 호출, 입력 쿼리: {query}"}


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