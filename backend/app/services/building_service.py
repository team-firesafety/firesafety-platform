from __future__ import annotations
import asyncio, logging, httpx
from typing import List, Dict, Tuple, Optional
from shapely.geometry import shape, Point, box, Polygon, MultiPolygon

from ..schemas.building import Building
from .fire_risk import score
from .vworld import find_zone_by_center, bldginfo_url, split_bbox

logger = logging.getLogger("building_service")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(levelname).1s] %(asctime)s | %(message)s",
                                     datefmt="%H:%M:%S"))
    logger.addHandler(h)
logger.setLevel(logging.INFO)

# ---------- 내부 util ----------
async def _fetch(url: str, cli: httpx.AsyncClient):
    r = await cli.get(url, timeout=40)
    r.raise_for_status()
    return r.json()

def _lonlat(g: dict) -> Optional[Tuple[float, float]]:
    t, c = g["type"], g["coordinates"]
    if t == "Point":
        return c[:2]
    if t == "Polygon":
        return c[0][0][:2]
    if t == "MultiPolygon":
        return c[0][0][0][:2]

_s = lambda v, d="": str(v) if v not in (None, "") else d
_i = lambda v, d=0: int(v) if str(v).isdigit() else d
_f = lambda v, d=0.: float(v) if v not in (None, "") else d

# ---------- main ----------
async def get_buildings_by_center(center: str, top_n: int = 200) -> List[Building]:
    zone_dict = find_zone_by_center(center)
    if not zone_dict:
        logger.error("관할명 불일치: %s", center)
        return []

    poly = shape(zone_dict["geometry"])           # Polygon OR MultiPolygon

    # --- 타일링할 좌표 배열 생성 -------------------------------------------
    if isinstance(poly, Polygon):
        coord_src = list(poly.exterior.coords)
    elif isinstance(poly, MultiPolygon):
        # 모든 서브 폴리곤 외곽선 좌표를 합칩니다.
        coord_src = [pt
                     for geom in poly.geoms
                     for pt in geom.exterior.coords]
    else:                                         # 이론상 없지만 방어
        logger.error("지원하지 않는 geometry: %s", poly.geom_type)
        return []

    tiles = [t for t in split_bbox(coord_src, size=0.01)
             if box(*t).intersects(poly)]
    logger.info("DEBUG  tiles=%d  center=%s  polygon_type=%s",
                len(tiles), center, poly.geom_type)

    limit = httpx.Limits(max_connections=20, max_keepalive_connections=5)
    async with httpx.AsyncClient(limits=limit, timeout=30) as cli:
        pages = await asyncio.gather(*[
            _fetch(bldginfo_url(t), cli) for t in tiles
        ])

    # --- 건물 합치기 & 위험도 ----------------------------------------------
    uniq: Dict[str, Building] = {}
    for p in pages:
        for f in p["features"]:
            ll = _lonlat(f["geometry"])
            if not ll or not poly.contains(Point(ll)):
                continue
            prop = f["properties"]
            bid = _s(prop.get("buld_idntfc_no"))
            key = bid or f"{ll[0]:.7f}_{ll[1]:.7f}"
            risk = score(prop)
            if key in uniq and risk <= uniq[key].riskScore:
                continue
            uniq[key] = Building(
                name=_s(prop.get("buld_nm"), "건물"),
                lon=ll[0], lat=ll[1], buldId=bid,
                platPlc="-", newPlatPlc="-",
                buldKndCode=_s(prop.get("buld_knd_code")),
                mainPrposCode=_s(prop.get("main_prpos_code")),
                strctCdNm=_s(prop.get("strct_code")),
                useAprDay=_s(prop.get("prmisn_de") or
                             prop.get("use_confm_de"))[:8],
                totArea=_f(prop.get("buld_totar")),
                groundFloors=_i(prop.get("ground_floor_co")),
                bsmFloors=_i(prop.get("undgrnd_floor_co")),
                riskScore=risk,
            )

    top = sorted(uniq.values(),
                 key=lambda b: b.riskScore,
                 reverse=True)[:top_n]
    logger.info("건물 %d → top %d", len(uniq), len(top))
    return top
