from fastapi import APIRouter, Query
from ...schemas.building import Building
from ...services.mock_firestation_service import get_buildings_by_station   # ← 변경

router = APIRouter()

@router.get(
    "/buildings",
    summary="소방서 관할 화재 취약 건물 (MOCK 실제 좌표)",
)
async def list_buildings(
        station: str = Query("종로소방서", description="어떤 값을 넣어도 종로 데이터 반환"),
        top_n: int = Query(200, ge=1, le=500)
):
    station_info, buildings = await get_buildings_by_station(station, top_n)
    return {
        "station": station_info,           # {name, lon, lat}
        "buildings": [b.model_dump(by_alias=True) for b in buildings],
    }
