"""
▶ Building = Location + 건축물대장 주요 필드를 확장한 모델
"""

from typing import Optional
from pydantic import Field

from .location import Location

class Building(Location):
    # ------------------------------
    # 순찰 경로용 메타데이터
    # ------------------------------
    seq: Optional[int] = Field(
        None,
        description="경로 상 방문 순서 (1부터). 서비스 계산 뒤 세팅."
    )

    # ------------------------------
    # 건축물대장(getBrRecapTitleInfo) 주요 필드
    # ------------------------------
    platPlc: str      = Field(..., description="지번 주소")
    newPlatPlc: str   = Field(..., description="도로명 주소")
    strctCdNm: str    = Field(..., description="주 구조(예: 목조)")
    useAprDay: str    = Field(..., description="사용 승인일 (YYYY-MM-DD)")
    totArea: float    = Field(..., description="연면적(㎡)")
