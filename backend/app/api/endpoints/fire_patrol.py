"""
GET /patrol/buildings  화재 취약 건물 7곳의 메타데이터를 그대로 반환
"""

from fastapi import APIRouter

from ...schemas.building import Building
from ...services.patrol_service import get_all_buildings

# prefix="/patrol" 은 app/api/router.py 에서 부여됩니다.
router = APIRouter()

# -----------------------------------------------------------------
# 단일 엔드포인트:  GET /patrol/buildings
# -----------------------------------------------------------------
@router.get(
    "/buildings",
    summary="화재 위험 건물 메타데이터 7곳 조회",
    response_model=list[Building],   # Swagger에 배열 구조로 표시
)
def list_buildings() -> list[Building]:
    """
    ▶ 별다른 파라미터 없이 호출 가능한 **GET** 엔드포인트
    ▶ 서비스 계층에서 하드코딩 데이터를 읽어 그대로 반환합니다.
    """
    return get_all_buildings()
