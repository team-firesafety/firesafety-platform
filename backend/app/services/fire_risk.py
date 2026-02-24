"""
위험도 산정 v3 – 시그모이드 기반
────────────────────────────────
0~99 분포를 확보하면서도 화재학적으로 논리적 근거를 유지
"""

from math import log, exp
from datetime import datetime

THIS_YEAR = datetime.now().year


# ──────────────────────────────────
# 안전 변환 헬퍼
# ──────────────────────────────────
def _safe_int(v, d=0):
    try: return int(v)
    except (TypeError, ValueError): return d

def _safe_float(v, d=0.0):
    try: return float(v)
    except (TypeError, ValueError): return d


# ──────────────────────────────────
# S‑커브 변환 함수
# ──────────────────────────────────
def _sigmoid(x: float, mid: float, scale: float) -> float:
    """
    값이 mid 에서 0.5, scale 은 기울기(작을수록 급격)
    반환 범위 0.0 ~ 1.0
    """
    return 1.0 / (1.0 + exp(-(x - mid) / scale))


# ──────────────────────────────────
# 위험도 계산
# ──────────────────────────────────
def score(prop: dict) -> int:
    # ---------- 1) 발생 가능성 P ----------
    # (a) 노후도
    year = _safe_int((prop.get("prmisn_de") or "")[:4], 1970)
    age  = max(0, THIS_YEAR - year)
    age_norm = _sigmoid(age, mid=35, scale=7)   # 35년 = 0.5

    # (b) 가연성 구조
    combust_map = {"10": 1.0, "20": 0.95, "21": 0.9, "30": 0.7,
                   "40": 0.4, "42": 0.3}          # 42=철근콘크리트
    strct = str(prop.get("strct_code") or "")[:2]
    combust_norm = combust_map.get(strct, 0.25)  # 기본 0.25

    P = 0.6 * age_norm + 0.4 * combust_norm      # 0 ~ 1

    # ---------- 2) 피해 규모 C ----------
    # (a) 층수
    floors = _safe_int(prop.get("ground_floor_co"))
    floors_norm = _sigmoid(floors, mid=6, scale=1.8)  # 6층=0.5

    # (b) 연면적(로그)
    area = max(1.0, _safe_float(prop.get("buld_totar")))
    area_norm = _sigmoid(log(area), mid=log(3000), scale=0.6)

    # (c) 다중이용
    multi_use = str(prop.get("main_prpos_code") or "")
    if multi_use in {"04000","15000","17000","21000","22000","23000"}:
        usage_norm = 1.0
    elif multi_use in {"03000","09000","18000","20000"}:  # 업무·공장 등
        usage_norm = 0.4
    else:
        usage_norm = 0.1

    C = 0.45 * floors_norm + 0.35 * area_norm + 0.20 * usage_norm

    # ---------- 3) 최종 위험도 ----------
    risk = int(round(100 * P * C))          # 0 ~ 100
    return min(max(risk, 0), 99)
