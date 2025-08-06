"""
한글 컬럼명 매핑 및 메타데이터 관리 서비스
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ColumnMappingService:
    """컬럼 메타데이터 관리 서비스 (한글 컬럼명 전용)"""
    
    # 영어→한글 매핑 (데이터 로더에서만 사용)
    COLUMN_MAPPING: Dict[str, str] = {
        # 공통 필드
        "id": "ID",
        "year": "연도",
        "created_at": "생성일시",
        "updated_at": "수정일시",
        
        # 화재 기본 정보
        "wrinv_no": "화재조사번호",
        "fire_type_nm": "화재유형명",
        "bldg_srtfrm_nm": "건물주구조형태명",
        "bldg_strctr_nm": "건물구조명",
        "bldg_srtrf_nm": "건물지붕구조명", 
        "bldg_rscu_dngct": "건물위험등급",
        "grnd_nofl": "지상층수",
        "udgd_nofl": "지하층수",
        "gfa": "연면적",
        "bttm_area": "바닥면적",
        "bldg_stts_nm": "건물상태명",
        "spfptg_nm": "소방시설명",
        "smtpr_lclsf_nm": "연기감지기대분류명",
        "smtpr_sclsf_nm": "연기감지기소분류명",
        
        # 피해 현황
        "dth_cnt": "사망자수",
        "injpsn_cnt": "부상자수",
        "hnl_dam_cnt": "인명피해수",
        "prpt_dam_amt": "재산피해액",
        
        # 발생 일시 정보
        "ocrn_yr": "발생연도",
        "ocrn_ymd": "발생일자",
        "ocrn_tm": "발생시각",
        "ocrn_mm": "발생월",
        "ocrn_day": "발생일",
        "ocrn_hr": "발생시",
        "ocrn_mn": "발생분",
        "seasn_nm": "계절명",
        "qtr_no": "분기",
        "dow_nm": "요일명",
        "dclr_dow": "신고요일",
        
        # 출동 및 처리 정보
        "frstn_nm": "소방서명",
        "cntr_nm": "센터명",
        "lfdau_nm": "ladder차량명",
        "dspt_req_tm": "출동요청시각",
        "dspt_dt": "출동일시",
        "fire_supesn_req_tm": "화재진압요청시각",
        "rcpt_dt": "접수일시",
        "grnds_arvl_dt": "현장도착일시",
        "bgnn_potfr_dt": "진화개시일시",
        "prfect_potfr_dt": "완전진화일시",
        "cbk_dt": "철수일시",
        "dspt_req_hr": "출동요청시각",
        "fire_supesn_hr": "화재진압시각",
        
        # 위치 정보
        "grnds_ctpv_nm": "현장시도명",
        "grnds_sgg_nm": "현장시군구명", 
        "ctpv_nm": "시도명",
        "sgg_nm": "시군구명",
        "cty_frmvl_se_nm": "도시농촌구분명",
        "damg_rgn_lot": "피해지역경도",
        "damg_rgn_lat": "피해지역위도",
        "grnds_dstnc": "현장거리",
        "cntr_grnds_dstnc": "센터현장거리",
        "lfdau_grnds_dstnc": "ladder차량현장거리",
        "frstn_grnds_dstnc": "소방서현장거리",
        
        # 화재 원인 및 특성
        "igtn_htsrc_lclsf_nm": "점화열원대분류명",
        "igtn_htsrc_sclsf_nm": "점화열원소분류명",
        "igtn_htsrc_nm": "점화열원명",
        "igtn_dmnt_lclsf_nm": "점화물대분류명", 
        "igtn_dmnt_sclsf_nm": "점화물소분류명",
        "frst_igobj_lclsf_nm": "최초점화물대분류명",
        "frst_igobj_sclsf_nm": "최초점화물소분류명",
        "igtn_istr_lclsf_nm": "점화인자대분류명",
        "igtn_istr_sclsf_nm": "점화인자소분류명",
        "cmbs_expobj_lclsf_nm": "연소확대물대분류명",
        "cmbs_expobj_sclsf_nm": "연소확대물소분류명",
        
        # 발생 장소
        "fclt_plc_lclsf_nm": "시설장소대분류명",
        "fclt_plc_mclsf_nm": "시설장소중분류명", 
        "fclt_plc_sclsf_nm": "시설장소소분류명",
        "igtn_flr_nm": "점화층명",
        "igtn_plc_nm": "점화장소명",
        "so_area": "소실면적",
        "acdnt_ocrn_plc_nm": "사고발생장소명",
        
        # 차량 화재 관련
        "vhcl_igtn_pstn_nm": "차량점화위치명",
        "vhcl_plc_nm": "차량장소명",
        
        # 기타 특성
        "fire_insrnc_oblg_trgt_yn": "화재보험의무가입대상여부",
        "fire_insrnc_oblg_join_trgt_yn": "화재보험의무가입대상여부",
        "arson_mng_trgt_yn": "방화관리대상여부",
        "mub_yn": "다중이용업소여부",
        "emrg_cntrl_yn": "응급제어여부",
        "fnd_fire_se_nm": "화재발견구분명",
        "fnd_fire_igtn_brnch_nm": "화재발견점화부위명",
        "fnd_igtn_pstn_nm": "화재발견점화위치명",
        
        # 기상 정보
        "hr_unit_artmp": "시간당기온",
        "hr_unit_rn": "시간당강수량",
        "hr_unit_wspd": "시간당풍속",
        "hr_unit_wspd_info": "시간당풍속정보",
        "hr_unit_wndrct": "시간당풍향",
        "wndrct_brng": "풍향방위",
        "hr_unit_hum": "시간당습도",
        "hr_unit_snwfl": "시간당강설량",
        "hr_unit_vsdst": "시간당가시거리",
        
        # 구조 출동 관련
        "clmty_rscu_rptp_no": "재난구조신고번호",
        "acdnt_cs_nm": "사고원인명",
        "prcs_rslt_se_nm": "처리결과구분명",
        "dclr_ymd": "신고일자",
        "dclr_tm": "신고시각",
        "dclr_yr": "신고연도",
        "dclr_mm": "신고월",
        "dclr_day": "신고일",
        "dclr_hr": "신고시",
        "dclr_mn": "신고분",
        "dspt_ymd": "출동일자",
        "dspt_tm": "출동시각",
        "dspt_yr": "출동연도",
        "dspt_mm": "출동월",
        "dspt_day": "출동일",
        "dspt_hr": "출동시",
        "dspt_mn": "출동분",
        "grnds_arvl_ymd": "현장도착일자",
        "grnds_arvl_tm": "현장도착시각",
        "grnds_arvl_yr": "현장도착연도",
        "grnds_arvl_mm": "현장도착월",
        "grnds_arvl_day": "현장도착일",
        "grnds_arvl_hr": "현장도착시",
        "grnds_arvl_mn": "현장도착분",
        "rscu_cmptn_ymd": "구조완료일자",
        "rscu_cmptn_tm": "구조완료시각",
        "rscu_cmptn_yr": "구조완료연도",
        "rscu_cmptn_mm": "구조완료월",
        "rscu_cmptn_day": "구조완료일",
        "rscu_cmptn_hr": "구조완료시",
        "rscu_cmptn_mn": "구조완료분",
        "cbk_ymd": "철수일자",
        "cbk_tm": "철수시각",
        "cbk_yr": "철수연도",
        "cbk_mm": "철수월",
        "cbk_day": "철수일",
        "cbk_hr": "철수시",
        "cbk_mn": "철수분",
        "etc_ocrn_type_dtl_nm": "기타발생유형상세명",
        "acdnt_cs_assrt_nm": "사고원인주장명",
        
        # 전국 화재 관련 추가
        "bldg_gfa": "건물연면적"
    }
    
    # 컬럼 타입 및 차트 사용 메타데이터
    COLUMN_METADATA: Dict[str, Dict[str, Any]] = {
        # 수치형 (Y축에 적합)
        "사망자수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "명"},
        "부상자수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "명"},
        "인명피해수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "명"},
        "재산피해액": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "천원"},
        "연면적": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "㎡"},
        "바닥면적": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "㎡"},
        "소실면적": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "㎡"},
        "지상층수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "층"},
        "지하층수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "층"},
        "현장거리": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "km"},
        "시간당기온": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "℃"},
        "시간당풍속": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "m/s"},
        "시간당습도": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "%"},
        "시간당강수량": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "mm"},
        
        # 범주형 (그룹화에 적합)
        "화재유형명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "소방서명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "건물구조명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "시도명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "시군구명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "계절명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "요일명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "신고요일": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "점화열원대분류명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "시설장소대분류명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "사고원인명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        "처리결과구분명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
        
        # 날짜형 (X축 시계열에 적합)
        "발생일자": {"type": "date", "chart_usage": ["x_axis"], "format": "YYYYMMDD"},
        "발생연도": {"type": "date", "chart_usage": ["x_axis"], "format": "YYYY"},
        "발생월": {"type": "date", "chart_usage": ["x_axis"], "format": "MM"},
        "발생일": {"type": "date", "chart_usage": ["x_axis"], "format": "DD"},
        "발생시": {"type": "date", "chart_usage": ["x_axis"], "format": "HH"},
        "분기": {"type": "date", "chart_usage": ["x_axis"], "format": "Q"},
        "신고일자": {"type": "date", "chart_usage": ["x_axis"], "format": "YYYYMMDD"},
        "출동일자": {"type": "date", "chart_usage": ["x_axis"], "format": "YYYYMMDD"},
        
        # 좌표형 (지도에 적합)
        "피해지역위도": {"type": "coordinate", "chart_usage": ["map"], "coord_type": "latitude"},
        "피해지역경도": {"type": "coordinate", "chart_usage": ["map"], "coord_type": "longitude"},
        
        # 기타
        "ID": {"type": "identifier", "chart_usage": []},
        "화재조사번호": {"type": "identifier", "chart_usage": []},
        "생성일시": {"type": "timestamp", "chart_usage": []},
        "수정일시": {"type": "timestamp", "chart_usage": []}
    }
    
    # 차트 추천 조합
    CHART_RECOMMENDATIONS: List[Dict[str, Any]] = [
        {
            "type": "line_chart",
            "name": "시계열 트렌드 분석",
            "x_axis": ["발생일자", "발생연도", "발생월"],
            "y_axis": ["사망자수", "부상자수", "재산피해액"],
            "description": "시간에 따른 화재 발생 트렌드 분석"
        },
        {
            "type": "bar_chart", 
            "name": "지역별/원인별 분석",
            "x_axis": ["소방서명", "시군구명", "화재유형명", "점화열원대분류명"],
            "y_axis": ["사망자수", "부상자수", "재산피해액"],
            "description": "카테고리별 화재 발생 현황 비교"
        },
        {
            "type": "pie_chart",
            "name": "비율 분석",
            "category": ["화재유형명", "점화열원대분류명", "시설장소대분류명"],
            "value": ["사망자수", "부상자수", "재산피해액"],
            "description": "전체 대비 각 카테고리의 비율 분석"
        },
        {
            "type": "scatter_plot",
            "name": "상관관계 분석", 
            "x_axis": ["연면적", "지상층수", "시간당기온", "시간당풍속"],
            "y_axis": ["재산피해액", "사망자수", "부상자수"],
            "description": "수치형 변수 간 상관관계 분석"
        },
        {
            "type": "map_chart",
            "name": "지리적 분포 분석",
            "latitude": ["피해지역위도"],
            "longitude": ["피해지역경도"],
            "value": ["재산피해액", "사망자수"],
            "description": "화재 발생 지역별 분포 및 피해 규모"
        }
    ]
    
    @classmethod
    def get_korean_column_name(cls, english_name: str) -> str:
        """영어 컬럼명을 한글로 변환 (데이터 로더에서만 사용)"""
        return cls.COLUMN_MAPPING.get(english_name, english_name)
    
    @classmethod
    def get_column_metadata(cls, column_name: str) -> Dict[str, Any]:
        """컬럼의 메타데이터 반환"""
        return cls.COLUMN_METADATA.get(column_name, {
            "type": "unknown",
            "chart_usage": [],
            "unit": None
        })
    
    @classmethod
    def get_columns_by_type(cls, column_type: str) -> List[str]:
        """특정 타입의 컬럼들 반환"""
        return [
            col_name for col_name, metadata in cls.COLUMN_METADATA.items()
            if metadata.get("type") == column_type
        ]
    
    @classmethod
    def get_chart_suitable_columns(cls, chart_usage: str) -> List[str]:
        """특정 차트 용도에 적합한 컬럼들 반환"""
        return [
            col_name for col_name, metadata in cls.COLUMN_METADATA.items()
            if chart_usage in metadata.get("chart_usage", [])
        ]
    
    @classmethod
    def get_chart_recommendations_for_data(cls, available_columns: List[str]) -> List[Dict[str, Any]]:
        """사용 가능한 컬럼을 기반으로 차트 추천"""
        recommendations = []
        
        for chart_config in cls.CHART_RECOMMENDATIONS:
            # 해당 차트에 필요한 컬럼들이 있는지 확인
            chart_copy = chart_config.copy()
            
            if chart_config["type"] in ["line_chart", "bar_chart"]:
                suitable_x = [col for col in chart_config["x_axis"] if col in available_columns]
                suitable_y = [col for col in chart_config["y_axis"] if col in available_columns]
                
                if suitable_x and suitable_y:
                    chart_copy["available_x_axis"] = suitable_x
                    chart_copy["available_y_axis"] = suitable_y
                    recommendations.append(chart_copy)
                    
            elif chart_config["type"] == "pie_chart":
                suitable_cat = [col for col in chart_config["category"] if col in available_columns]
                suitable_val = [col for col in chart_config["value"] if col in available_columns]
                
                if suitable_cat and suitable_val:
                    chart_copy["available_category"] = suitable_cat
                    chart_copy["available_value"] = suitable_val
                    recommendations.append(chart_copy)
                    
            elif chart_config["type"] == "scatter_plot":
                suitable_x = [col for col in chart_config["x_axis"] if col in available_columns]
                suitable_y = [col for col in chart_config["y_axis"] if col in available_columns]
                
                if suitable_x and suitable_y:
                    chart_copy["available_x_axis"] = suitable_x
                    chart_copy["available_y_axis"] = suitable_y
                    recommendations.append(chart_copy)
                    
            elif chart_config["type"] == "map_chart":
                has_lat = any(col in available_columns for col in chart_config["latitude"])
                has_lon = any(col in available_columns for col in chart_config["longitude"])
                suitable_val = [col for col in chart_config["value"] if col in available_columns]
                
                if has_lat and has_lon and suitable_val:
                    chart_copy["available_latitude"] = [col for col in chart_config["latitude"] if col in available_columns]
                    chart_copy["available_longitude"] = [col for col in chart_config["longitude"] if col in available_columns]
                    chart_copy["available_value"] = suitable_val
                    recommendations.append(chart_copy)
        
        return recommendations
    
    @classmethod
    def build_response_metadata(cls, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """응답에 포함할 메타데이터 구성"""
        if not data:
            return {
                "columns_metadata": {},
                "chart_recommendations": []
            }
        
        # 실제 데이터에 있는 컬럼들
        available_columns = list(data[0].keys())
        
        # 컬럼별 메타데이터
        columns_metadata = {}
        for col in available_columns:
            columns_metadata[col] = cls.get_column_metadata(col)
        
        # 차트 추천
        chart_recommendations = cls.get_chart_recommendations_for_data(available_columns)
        
        return {
            "columns_metadata": columns_metadata,
            "chart_recommendations": chart_recommendations,
            "available_columns": {
                "numeric": cls.get_columns_by_type("numeric"),
                "categorical": cls.get_columns_by_type("categorical"), 
                "date": cls.get_columns_by_type("date"),
                "coordinate": cls.get_columns_by_type("coordinate")
            }
        }