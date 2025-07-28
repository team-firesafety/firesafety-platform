# 1) typing 모듈 : 파이썬에 ‘타입 힌트’(List, Optional 등)를 제공
# 2) geopy.distance.geodesic : 두 위·경도 간 실제 거리(m) 계산
# ------------------------------------------------------------
from typing import List, Optional
from geopy.distance import geodesic
from ..schemas.location import Location   # .. = 상위 폴더 한 칸 up

# 건물은 5곳까지만 허용 — 하드코딩(상수)으로 규칙을 정해 둠
MAX_BUILDINGS = 5


class PatrolService:
    """
    ▶ 목적 : ‘소방서 + 건물 목록’을 메모리에 보관하고,
             가장 가까운 순으로 ‘순찰 경로’를 계산해 주는 클래스
    ▶ 실제 서비스에서는 DB·복잡한 알고리즘으로 바뀔 수 있지만,
      구조(메서드 시그니처)는 유지하면 외부 코드를 고칠 필요가 없음.
    """

    def __init__(self):
        """
        인스턴스가 만들어질 때(empty) 기본값을 준비.
        - fire_station : 아직 정해지지 않았으므로 None
        - buildings    : 빈 리스트
        """
        self.fire_station: Optional[Location] = None
        self.buildings: List[Location] = []

    # -----------------------------------------------------------------
    # 1) 소방서 위치 등록
    # -----------------------------------------------------------------
    def set_fire_station(self, loc: Location):
        """
        ─ loc : Location 타입(이름 + lat + lon)
        기능 : ① 소방서 좌표 저장
              ② 기존 건물 목록 초기화
        """
        self.fire_station = loc
        self.buildings.clear()  # 소방서가 바뀌면 건물도 리셋!

    # -----------------------------------------------------------------
    # 2) 건물 한 곳 추가
    # -----------------------------------------------------------------
    def add_building(self, loc: Location):
        """
        예외 처리(ValueError) 두 가지:
          A. 소방서가 먼저 설정돼 있지 않으면 안 된다
          B. 이미 5곳이 등록돼 있으면 더 못 넣는다
        """
        if not self.fire_station:                 # A
            raise ValueError("Fire station first")
        if len(self.buildings) >= MAX_BUILDINGS:  # B
            raise ValueError("Too many buildings")

        self.buildings.append(loc)                # 정상 케이스 → 목록에 추가

    # -----------------------------------------------------------------
    # 3) 건물 목록 조회
    # -----------------------------------------------------------------
    def list_buildings(self) -> List[Location]:
        """그냥 리스트 그대로 리턴 (GET /buildings 용)"""
        return self.buildings

    # -----------------------------------------------------------------
    # 4) 순찰 경로 계산
    # -----------------------------------------------------------------
    def patrol_route(self) -> List[Location]:
        """
        반환값 : [소방서, 건물1, 건물2, ...]  ➡️ Vue / 지도 API가 선을 그릴 수 있음
        알고리즘 흐름
        ① 소방서·건물이 모두 있어야 함 (없으면 에러)
        ② 각 건물까지의 거리를 geodesic()으로 구함
        ③ 거리 짧은 순으로 sorted() 정렬 → ordered
        ④ [소방서] + ordered 리스트를 만들어 리턴
        """
        if not self.fire_station or not self.buildings:
            raise ValueError("Need station & buildings")

        # key= 매개변수 : ‘정렬 기준’을 지정하는 람다(lambda) 함수
        ordered = sorted(
            self.buildings,
            key=lambda b: geodesic(
                (self.fire_station.lat, self.fire_station.lon),  # 소방서 좌표
                (b.lat, b.lon),                                  # 건물 좌표
            ).meters,  # geodesic() 결과 객체 → .meters 로 숫자거리 추출
        )
        return [self.fire_station, *ordered]  # * = 리스트 풀기(splat)


# ------------------------------------------------------------
# 파일 맨 아래에서 ‘싱글턴’ 인스턴스 한 개를 만들어 둔다.
# 다른 모듈(api)에서 import 해 쓰면 어디서든 ‘같은 메모리’ 공유!
# ------------------------------------------------------------
patrol_service = PatrolService()
