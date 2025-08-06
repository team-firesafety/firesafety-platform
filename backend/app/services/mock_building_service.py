"""
mock_building_service.py
────────────────────────
• 런타임 네트워크 호출 없이, data/real_buildings_jongno.json 을 읽어
  Building 스키마 리스트를 반환한다.
• JSON 은 prepare_buildings_real.py 를 한번 실행해 생성한다.
"""

from __future__ import annotations
import json, pathlib, logging
from typing import List, Dict
from ..schemas.building import Building   # 프로젝트 스키마 그대로

logger = logging.getLogger("mock_building_service")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("[%(levelname).1s] %(asctime)s | %(message)s",
                                      datefmt="%H:%M:%S"))
    logger.addHandler(_h)
logger.setLevel(logging.INFO)

# ▒▒ JSON 로드 ▒▒
DATA_FILE = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "real_buildings_jongno.json"

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"{DATA_FILE} 가 없습니다.\n"
        "➜  먼저 `python -m backend.app.services.prepare_buildings_real` 명령으로 "
        "데이터 파일을 생성해 주세요."
    )

with DATA_FILE.open("r", encoding="utf-8") as f:
    _RAW: List[dict] = json.load(f)

_BUILDINGS: Dict[str, Building] = {
    b["buldId"]: Building(**b) for b in _RAW
}

logger.info("📖 로드된 건물 개수 = %d 건", len(_BUILDINGS))

# ▒▒ public 함수 ▒▒
async def get_buildings_by_center(_: str, top_n: int = 200) -> List[Building]:
    """
    · center 인자(‘○○119안전센터’ 등)는 무시하고
    · 하드코딩 JSON 의 riskScore 내림차순 Top‑N 반환
    """
    sorted_b = sorted(_BUILDINGS.values(),
                      key=lambda b: b.riskScore,
                      reverse=True)
    return sorted_b[:top_n]
