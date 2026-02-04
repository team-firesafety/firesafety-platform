from typing import Optional

from pydantic import Field

from .location import Location


class Building(Location):
    """
    Location( name · lat · lon ) + 건축물대장 주요 필드 + 위험도
    """

    # --- 주소 ---
    platPlc: str = Field(..., description="지번 주소")
    newPlatPlc: str = Field(..., description="도로명 주소")

    # --- 건물 식별·용도·구조 ---
    buldId: Optional[str] = Field(
        None, description="건물 식별번호(건축물대장 buld_idntfc_no)"
    )
    buldKndCode: Optional[str] = Field(
        None, description="건물 종류 코드(단독·공장·교육 등)"
    )
    mainPrposCode: Optional[str] = Field(
        None, description="주용도 코드"
    )
    strctCdNm: str = Field(..., description="주 구조(예: 철근콘크리트구조)")

    # --- 연식·규모 ---
    useAprDay: str = Field(..., description="준공/사용승인일(YYYY-MM-DD)")
    totArea: float = Field(..., description="연면적(㎡)")
    groundFloors: int = Field(..., alias="grndFloors", description="지상 층수")
    bsmFloors: int = Field(..., alias="bsmFloors", description="지하 층수")

    # --- 위험도 ---
    riskScore: int = Field(
        ..., ge=0, le=99, description="화재 취약도(0~99)"
    )
