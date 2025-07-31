from fastapi import APIRouter, Query
from ...schemas.building import Building
from ...services.building_service import get_buildings_by_station

router = APIRouter()

@router.get(
    "/buildings",
    response_model=list[Building],
    summary="소방서 관할 화재 취약 건물 조회",
)
async def list_buildings(
        station: str = Query("종로소방서", description="소방서 이름")
) -> list[Building]:
    return await get_buildings_by_station(station)
