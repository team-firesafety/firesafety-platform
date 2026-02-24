# backend/app/services/hardcoded_data.py
from typing import List
from ..schemas.location import Location
from ..schemas.building import Building

FIRE_STATION = Location(
    name="종로소방서",
    lat=37.5725,
    lon=126.9789,
)

BUILDINGS: List[Building] = [
    Building(  # ① 낙원상가
        name="낙원상가",
        platPlc="낙원동 288",
        newPlatPlc="서울 종로구 삼일대로 428",
        lat=37.572774, lon=126.988043,
        strctCdNm="철근콘크리트구조",
        useAprDay="1968-09-15",
        totArea=43208,
        grndFloors=17, bsmFloors=1,
    ),
    Building(  # ② 세운전자상가
        name="세운전자상가",
        platPlc="장사동 116-4",
        newPlatPlc="서울 종로구 청계천로 159",
        lat=37.571121, lon=126.999118,
        strctCdNm="철근콘크리트구조",
        useAprDay="1968-10-01",
        totArea=47100,
        grndFloors=8, bsmFloors=1,
    ),
    Building(  # ③ 동대문종합시장 A동
        name="동대문종합시장 A동",
        platPlc="종로6가 262-1",
        newPlatPlc="서울 종로구 종로 272",
        lat=37.570480, lon=127.002100,
        strctCdNm="철근콘크리트구조",
        useAprDay="1970-12-23",
        totArea=23000,
        grndFloors=9, bsmFloors=1,
    ),
    Building(  # ④ 광장시장 본관
        name="광장시장 본관",
        platPlc="예지동 2-1",
        newPlatPlc="서울 종로구 창경궁로 88",
        lat=37.570115, lon=126.999706,
        strctCdNm="철근콘크리트+목재 혼합",
        useAprDay="1962-05-05",
        totArea=18975,
        grndFloors=3, bsmFloors=1,
    ),
    Building(  # ⑤ 국일고시원
        name="국일고시원 건물",
        platPlc="관수동 20-8",
        newPlatPlc="서울 종로구 돈화문로2길 53",
        lat=37.571990, lon=126.985630,
        strctCdNm="철근콘크리트구조",
        useAprDay="1983-08-11",
        totArea=614,
        grndFloors=3, bsmFloors=1,
    ),
    Building(  # ⑥ 현대 계동사옥
        name="현대 계동사옥",
        platPlc="계동 140-2",
        newPlatPlc="서울 종로구 율곡로 75",
        lat=37.577473, lon=126.987520,
        strctCdNm="철근콘크리트구조",
        useAprDay="1983-11-01",
        totArea=112000,
        grndFloors=14, bsmFloors=3,
    ),
    Building(  # ⑦ 한국불교역사문화기념관
        name="한국불교역사문화기념관",
        platPlc="견지동 45-1",
        newPlatPlc="서울 종로구 우정국로 55",
        lat=37.574170, lon=126.981940,
        strctCdNm="철근콘크리트구조",
        useAprDay="2004-02-17",
        totArea=16800,
        grndFloors=4, bsmFloors=4,
    ),
]
