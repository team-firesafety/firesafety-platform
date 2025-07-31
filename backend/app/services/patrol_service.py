# backend/app/services/building_service.py
"""
▶ 하드코딩해 둔 BUILDINGS 리스트를 그대로 돌려주는
  아주 단순한 서비스 모듈입니다.
▶ 추후 DB나 API로 바뀌면 여기만 수정하면 됩니다.
"""

from copy import deepcopy
from typing import List

from .patrol_data import BUILDINGS
from ..schemas.building import Building


def get_all_buildings() -> List[Building]:
    """
    하드코딩된 BUILDINGS 원본을 손대지 않기 위해 deepcopy 후 반환.
    """
    return deepcopy(BUILDINGS)
