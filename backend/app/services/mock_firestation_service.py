"""
mock_firestation_service.py
───────────────────────────
• 종로소방서 위치 + 반경 1 km 건물 ≈ 500 건 반환
• 거리순  →  riskScore 균등 샘플링  →  최종 리스트
"""

from __future__ import annotations
import json, pathlib, logging, math, random
from typing import List, Tuple
from ..schemas.building import Building

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname).1s] %(asctime)s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("mock_firestation_service")

# ─── 종로소방서 좌표 ───────────────────────────────────────────────────────
_STATION = {"name": "종로소방서", "lon": 126.987649258831, "lat": 37.5768173425423}

# ─── 데이터 로드 (기존 2 000 + 건) ─────────────────────────────────────────
PROJ_ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA_FILE = PROJ_ROOT / "backend" / "data" / "real_buildings_jongno.json"
with DATA_FILE.open("r", encoding="utf-8") as f:
    _RAW: List[Building] = [Building(**b) for b in json.load(f)]
log.info("📖 로드된 원본 건물 = %d 건", len(_RAW))

# ─── Haversine(근사) 거리 계산 ─────────────────────────────────────────────
def _dist_km(lat1, lon1, lat2, lon2) -> float:
    dx = (lon2 - lon1) * 88.74 * math.cos(math.radians((lat1 + lat2) / 2))
    dy = (lat2 - lat1) * 111.2
    return math.hypot(dx, dy)           # km

# ─── 반경 1 km 필터 + 거리순 정렬 ─────────────────────────────────────────
_NEAR: List[Building] = []
for b in _RAW:
    if _dist_km(_STATION["lat"], _STATION["lon"], b.lat, b.lon) <= 1.2:
        _NEAR.append(b)

_NEAR.sort(key=lambda b: _dist_km(_STATION["lat"], _STATION["lon"], b.lat, b.lon))
log.info("📍 1 km내 건물 = %d 건", len(_NEAR))     # 500 ± 예상

# ─── riskScore 균등 샘플링 (시각적 색상 다양화) ────────────────────────────
_BUCKETS: dict[int, list[Building]] = {}
for b in _NEAR:
    bucket = b.riskScore // 10         # 0‑9, 10‑19, …, 90‑99
    _BUCKETS.setdefault(bucket, []).append(b)

def _balanced_sample(n: int = 2000) -> List[Building]:
    """
    버킷별 동일 비율로 뽑아 색상 분포 고르게
    """
    sample: List[Building] = []
    quota = max(1, n // len(_BUCKETS))
    for lst in _BUCKETS.values():
        random.shuffle(lst)
        sample += lst[:quota]
    # 부족하면 남은 것에서 추가
    if len(sample) < n:
        remainder = [b for lst in _BUCKETS.values() for b in lst[quota:]]
        random.shuffle(remainder)
        sample += remainder[: n - len(sample)]
    return sample[:n]

_SAMPLE_CACHE = _balanced_sample()      # 서버 기동 시 1회 생성

# ─── public 함수 ──────────────────────────────────────────────────────────
async def get_buildings_by_station(_: str, top_n: int | None = None) -> Tuple[dict, List[Building]]:
    """
    ‘station’ 파라미터는 무시하고 종로소방서 기준 데이터 반환
    • 기본 : 버퍼샘플 500 건
    • top_n 가 주어지면 그 갯수로 잘라 보냄 (최대 500)
    """
    if top_n and 0 < top_n < len(_SAMPLE_CACHE):
        return _STATION, _SAMPLE_CACHE[:top_n]
    return _STATION, _SAMPLE_CACHE
