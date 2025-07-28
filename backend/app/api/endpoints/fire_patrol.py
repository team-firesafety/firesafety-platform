#   HTTPException → 오류 응답(상태코드·메시지) 쉽게 반환
#   status → HTTP 상태코드 값(400, 404…)을 상수로 제공
from fastapi import APIRouter, HTTPException, status

from ...schemas.location import Location
from ...services.patrol_service import patrol_service

# 라우터 인스턴스 생성
# prefix는 api/router.py 에서 붙일 예정
router = APIRouter()


# 1) 소방서 위치 설정 엔드포인트
@router.post("/firestation")          # POST /patrol/firestation (prefix 포함 시)
def set_firestation(loc: Location):   # loc 매개변수 = 요청 JSON을 Location 스키마로 파싱
    patrol_service.set_fire_station(loc)  # 비즈니스 로직 호출
    return {"msg": "fire station set", "fire_station": loc}


# 2) 건물 한 곳 추가
@router.post("/buildings")            # POST /patrol/buildings
def add_building(loc: Location):
    try:
        patrol_service.add_building(loc)
    except ValueError as e:           # 서비스 계층이 에러를 던지면
        raise HTTPException(          # → 400 Bad Request 로 변환
            status.HTTP_400_BAD_REQUEST,
            str(e)
        )
    return {"count": len(patrol_service.list_buildings())}


# 3) 등록된 건물 목록 조회
@router.get("/buildings")             # GET /patrol/buildings
def list_buildings():
    return patrol_service.list_buildings()


# 4) 순찰 경로 계산 (소방서 + 가까운 순 건물)
@router.get("/route")                 # GET /patrol/route
def get_route():
    try:
        return {"route": patrol_service.patrol_route()}
    except ValueError as e:           # 소방서/건물이 아직 없을 때
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            str(e)
        )
