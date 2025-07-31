"""
소방서 → 관할 건물 목록 + 위험도 계산 서비스
──────────────────────────────────────────
1) 관할 폴리곤(lt_c_usfsffb) → 타일링
2) 각 타일과 dt_d162 레이어 INTERSECTS 조회(WFS 1.1.0 JSON)
3) 위험도(score) 계산 → riskScore 내림차순 상위 200건 반환
※ 모든 필드 변환·파싱을 안전 함수로 감싸 None/빈값 오류 방지
"""

from __future__ import annotations

import asyncio
from typing import List, Tuple, Optional

import httpx

from ..schemas.building import Building
from .fire_risk import score
from .vworld import fire_zone_url, bldginfo_url, split_bbox, fetch_json


# ───────────────────────────────────────────────
# 안전 변환 헬퍼
# ───────────────────────────────────────────────
def _safe_str(v: object | None, default: str = "") -> str:
    return str(v) if v not in (None, "") else default


def _safe_int(v: object | None, default: int = 0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _safe_float(v: object | None, default: float = 0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


# ───────────────────────────────────────────────
# geometry → 대표 lon/lat 추출
# ───────────────────────────────────────────────
def _lonlat(geom: dict) -> Optional[Tuple[float, float]]:
    gtype = geom.get("type")
    coords = geom.get("coordinates")

    if not coords:
        return None

    try:
        if gtype == "Point":
            lon, lat = coords[:2]
        elif gtype == "Polygon":
            lon, lat = coords[0][0][:2]
        elif gtype == "MultiPolygon":
            lon, lat = coords[0][0][0][:2]
        else:
            return None
        return lon, lat
    except (IndexError, TypeError):
        return None


# ───────────────────────────────────────────────
# public 함수 : 엔드포인트에서 호출
# ───────────────────────────────────────────────
async def get_buildings_by_station(station: str) -> List[Building]:
    """
    Parameters
    ----------
    station : '종로소방서', '구로소방서' …  (소방서명 전체)

    Returns
    -------
    List[Building]  (riskScore desc, max 200)
    """
    async with httpx.AsyncClient() as client:
        # ① 관할 폴리곤 GeoJSON
        zone_geo = await fetch_json(fire_zone_url(station), client)
        geom = zone_geo["features"][0]["geometry"]

        ring = (
            geom["coordinates"][0] if geom["type"] == "Polygon"
            else geom["coordinates"][0][0]
        )
        poly_coords = [(pt[0], pt[1]) for pt in ring]   # (lon,lat)

        # ② 타일링 후 병렬로 dt_d162 조회
        tasks = [fetch_json(bldginfo_url(tile), client)
                 for tile in split_bbox(poly_coords)]
        pages = await asyncio.gather(*tasks)

    # ③ 병합 + 위험도
    buildings: list[Building] = []
    for page in pages:
        for feat in page.get("features", []):
            ll = _lonlat(feat["geometry"])
            if ll is None:        # 좌표 추출 실패 → skip
                continue

            prop = feat["properties"]

            buildings.append(
                Building(
                    # 기본 위치·이름
                    name      = _safe_str(prop.get("buld_nm"), "건물"),
                    lon       = ll[0],
                    lat       = ll[1],

                    # 주소 (dt_d162 에는 상세 주소 없음)
                    platPlc   = "-",
                    newPlatPlc= "-",

                    # 구조·규모·연식
                    strctCdNm   = _safe_str(prop.get("strct_code")),
                    useAprDay   = _safe_str(prop.get("prmisn_de") or
                                            prop.get("use_confm_de"))[:8],
                    totArea     = _safe_float(prop.get("buld_totar")),
                    grndFloors  = _safe_int(prop.get("ground_floor_co")),
                    bsmFloors   = _safe_int(prop.get("undgrnd_floor_co")),

                    # 식별 코드
                    buldId        = _safe_str(prop.get("buld_idntfc_no")),
                    buldKndCode   = _safe_str(prop.get("buld_knd_code")),
                    mainPrposCode = _safe_str(prop.get("main_prpos_code")),

                    # 위험도
                    riskScore = score(prop),
                )
            )

    # ④ 위험도 높은 순 정렬 → 상위 200건만
    buildings.sort(key=lambda b: b.riskScore, reverse=True)
    return buildings[:200]
