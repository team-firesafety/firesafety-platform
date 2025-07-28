from pydantic import BaseModel, Field

class Location(BaseModel):
    # 건물 공통 좌표 스키마
    name: str = Field(..., example="Gangnam Fire Station")
    lat: float = Field(..., ge=-90, le=90, example=37.4993)
    lon: float = Field(..., ge=-180, le=180, example=127.0364)
