from __future__ import annotations
import os, functools, httpx

VWORLD_KEY = os.getenv("VWORLD_KEY")
VWORLD_DOMAIN = os.getenv("VWORLD_DOMAIN", "localhost")
WFS_ENDPOINT = "https://api.vworld.kr/req/wfs"
SRID = "EPSG:4326"

def _wfs(p:dict)->str:
    p |= {"KEY":VWORLD_KEY,"DOMAIN":VWORLD_DOMAIN}
    return WFS_ENDPOINT+"?"+"&".join(f"{k}={v}" for k,v in p.items())

def _dl(start:int):
    return httpx.get(_wfs({
        "SERVICE":"WFS","REQUEST":"GetFeature","VERSION":"1.1.0",
        "TYPENAME":"lt_c_usfsffb","outputFormat":"application/json",
        "MAXFEATURES":1000,"STARTINDEX":start}),timeout=60).json()["features"]

@functools.lru_cache(maxsize=1)
def load_zones():            # 1 053 feature 캐시
    return _dl(0)+_dl(1000)

def find_zone_by_center(center:str):
    key=center.lower().replace(" ","")
    for f in load_zones():
        n=f["properties"]["ward_nm"].lower().replace(" ","")
        if n==key: return f
    return None

def bldginfo_url(bbox):
    minx, miny, maxx, maxy = bbox          # X=경도, Y=위도
    # ✘ 기존 : lat,lon,lat,lon                 (반대로 넣음)
    # ✔ 수정 : lon,lat,lon,lat
    bbox = f"{minx:.7f},{miny:.7f},{maxx:.7f},{maxy:.7f}"
    return _wfs({
        "SERVICE":"WFS", "REQUEST":"GetFeature", "VERSION":"1.1.0",
        "TYPENAME":"dt_d162", "outputFormat":"application/json",
        "MAXFEATURES":1000, "BBOX":bbox, "SRSNAME":"EPSG:4326"
    })


def split_bbox(coords,size=0.005):
    xs,ys=zip(*coords);minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
    x=minx
    while x<maxx:
        y=miny
        while y<maxy:
            yield (x,y,min(x+size,maxx),min(y+size,maxy))
            y+=size
        x+=size
