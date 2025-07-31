"""
V‑World WFS 헬퍼 모듈
────────────────────────────
* 소방서 관할 폴리곤(lt_c_usfsffb) → 건물 레이어(dt_d162) 교차 조회
* dt_d162 는 WFS 2.0.0 에서 PK(정렬) 문제가 있으므로
  ⇒ WFS 1.1.0 + CQL_INTERSECTS + JSON 출력 방식 사용
* Polygon → 0.005°(≈550 m) BBOX 타일 분할도 지원
"""

from __future__ import annotations
from urllib.parse import urlencode
from typing import Iterator, List, Tuple

import httpx
from ..config import settings

# ───────────────────────────────────────────────
# 공통 상수
# ───────────────────────────────────────────────
VWORLD_DOM   = "localhost"
BASE_WFS     = "https://api.vworld.kr/req/wfs"

# ───────────────────────────────────────────────
# 1) 소방서 관할 폴리곤 WFS URL
# ───────────────────────────────────────────────
def fire_zone_url(ward_name: str) -> str:
    """lt_c_usfsffb 레이어에서 ward_nm='종로소방서' 형태로 검색"""
    q = {
        "service"   : "WFS",
        "version"   : "2.0.0",
        "request"   : "GetFeature",
        "typeName"  : "lt_c_usfsffb",
        "CQL_FILTER": f"ward_nm='{ward_name}'",
        "output"    : "json",
        "srsName"   : "EPSG:4326",
        "key"       : settings.VWORLD_KEY,
        "domain"    : VWORLD_DOM,
    }
    return f"{BASE_WFS}?{urlencode(q, safe=':,()')}"  # :,() 는 CQL 안에서 필요

# ───────────────────────────────────────────────
# 2) 건물(dt_d162) WFS URL (※ 1.1.0 + CQL_INTERSECTS)
# ───────────────────────────────────────────────
def bldginfo_url(poly_wkt: str) -> str:
    """
    dt_d162(건축물대장 요약) 레이어를
    ① WFS 1.1.0   ② JSON 출력  ③ CQL_INTERSECTS 로 호출
    => PK 없어서 생기는 2.0.0 오류, 축 혼동 모두 회피
    """
    q = {
        "service"      : "WFS",
        "version"      : "1.1.0",
        "request"      : "GetFeature",
        "typeName"     : "dt_d162",
        "CQL_FILTER"   : f"INTERSECTS(geom, POLYGON(({poly_wkt})))",
        "outputFormat" : "application/json",
        "srsName"      : "EPSG:4326",
        "maxFeatures"  : 1000,          # 타일 1장당 최대 1000건
        "key"          : settings.VWORLD_KEY,
        "domain"       : VWORLD_DOM,
    }
    return f"{BASE_WFS}?{urlencode(q, safe=':,() ')}"  # 공백도 허용

# ───────────────────────────────────────────────
# 3) 폴리곤 외접 BBOX(≈550 m) 타일 제너레이터
# ───────────────────────────────────────────────
def split_bbox(poly_coords: List[Tuple[float, float]],
               step: float = 0.005) -> Iterator[str]:
    """
    Parameters
    ----------
    poly_coords : [(lon, lat), ...]  # EPSG:4326
    step        : 0.005° ≈ 550 m (경위도 기준)

    Yields
    ------
    str : "lon lat,lon lat,lon lat,lon lat,lon lat"  (닫힌 WKT 링)
    """
    lons, lats = zip(*poly_coords)
    minx, maxx = min(lons), max(lons)
    miny, maxy = min(lats), max(lats)

    xs = [round(minx + i * step, 6) for i in range(int((maxx - minx) / step) + 1)]
    ys = [round(miny + i * step, 6) for i in range(int((maxy - miny) / step) + 1)]

    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            yield (
                f"{xs[i]} {ys[j]},{xs[i+1]} {ys[j]},"
                f"{xs[i+1]} {ys[j+1]},{xs[i]} {ys[j+1]},"
                f"{xs[i]} {ys[j]}"
            )

# ───────────────────────────────────────────────
# 4) HTTP‑GET → JSON 헬퍼
# ───────────────────────────────────────────────
async def fetch_json(url: str, client: httpx.AsyncClient):
    r = await client.get(url, timeout=10.0)
    r.raise_for_status()
    return r.json()
