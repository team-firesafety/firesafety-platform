-- ================================
-- 🔥 Fire Safety Data Query API
-- 하이브리드 테이블 구조 마이그레이션
-- ================================

-- 기존 테이블 삭제 (필요시)
DROP TABLE IF EXISTS fire_safety_data CASCADE;
DROP TABLE IF EXISTS dataset_schemas CASCADE;

-- ================================
-- 1. 메타데이터 테이블 (개선된 버전)
-- ================================
CREATE TABLE dataset_schemas (
    id SERIAL PRIMARY KEY,
    dataset_type VARCHAR(100) UNIQUE NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    data_category VARCHAR(50) NOT NULL,
    keywords JSONB NOT NULL DEFAULT '[]',
    schema_definition JSONB NOT NULL,
    query_examples JSONB DEFAULT '[]',
    sample_queries JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 메타데이터 인덱스
CREATE INDEX idx_dataset_schemas_type ON dataset_schemas(dataset_type);
CREATE INDEX idx_dataset_schemas_category ON dataset_schemas(data_category);
CREATE INDEX idx_dataset_schemas_keywords ON dataset_schemas USING gin(keywords);

-- ================================
-- 2. 서울 화재출동 현황 (건축물)
-- ================================
CREATE TABLE seoul_fire_dispatch (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    wrinv_no VARCHAR(50) NOT NULL,
    fire_type_nm VARCHAR(100),
    bldg_srtfrm_nm VARCHAR(100),
    bldg_strctr_nm VARCHAR(100),
    bldg_srtrf_nm VARCHAR(100),
    bldg_rscu_dngct INTEGER,
    grnd_nofl INTEGER,
    udgd_nofl INTEGER,
    gfa NUMERIC,
    bttm_area NUMERIC,
    bldg_stts_nm VARCHAR(50),
    dth_cnt INTEGER DEFAULT 0,
    injpsn_cnt INTEGER DEFAULT 0,
    hnl_dam_cnt INTEGER DEFAULT 0,
    prpt_dam_amt BIGINT DEFAULT 0,
    ocrn_yr INTEGER,
    seasn_nm VARCHAR(20),
    qtr_no INTEGER,
    ocrn_ymd VARCHAR(20),
    ocrn_tm VARCHAR(20),
    ocrn_mm INTEGER,
    ocrn_day INTEGER,
    ocrn_hr INTEGER,
    ocrn_mn INTEGER,
    dclr_dow VARCHAR(20),
    frstn_nm VARCHAR(100),
    cntr_nm VARCHAR(100),
    lfdau_nm VARCHAR(100),
    dspt_req_tm VARCHAR(20),
    fire_supesn_req_tm VARCHAR(20),
    grnds_ctpv_nm VARCHAR(50),
    grnds_sgg_nm VARCHAR(50),
    cty_frmvl_se_nm VARCHAR(50),
    damg_rgn_lot NUMERIC,
    damg_rgn_lat NUMERIC,
    grnds_dstnc NUMERIC,
    cntr_grnds_dstnc NUMERIC,
    lfdau_grnds_dstnc NUMERIC,
    igtn_htsrc_lclsf_nm VARCHAR(100),
    igtn_htsrc_sclsf_nm VARCHAR(100),
    igtn_dmnt_lclsf_nm VARCHAR(100),
    igtn_dmnt_sclsf_nm VARCHAR(100),
    frst_igobj_lclsf_nm VARCHAR(100),
    frst_igobj_sclsf_nm VARCHAR(100),
    igtn_istr_lclsf_nm VARCHAR(100),
    igtn_istr_sclsf_nm VARCHAR(100),
    cmbs_expobj_lclsf_nm VARCHAR(100),
    cmbs_expobj_sclsf_nm VARCHAR(100),
    fclt_plc_lclsf_nm VARCHAR(100),
    fclt_plc_mclsf_nm VARCHAR(100),
    fclt_plc_sclsf_nm VARCHAR(100),
    igtn_flr_nm VARCHAR(50),
    so_area NUMERIC,
    fire_insrnc_oblg_join_trgt_yn CHAR(1),
    arson_mng_trgt_yn CHAR(1),
    mub_yn CHAR(1),
    emrg_cntrl_yn CHAR(1),
    igtn_plc_nm VARCHAR(100),
    vhcl_igtn_pstn_nm VARCHAR(100),
    fnd_fire_se_nm VARCHAR(100),
    fnd_fire_igtn_brnch_nm VARCHAR(100),
    hr_unit_artmp NUMERIC,
    hr_unit_rn NUMERIC,
    hr_unit_wspd NUMERIC,
    hr_unit_wndrct INTEGER,
    hr_unit_hum NUMERIC,
    hr_unit_snwfl NUMERIC,
    hr_unit_vsdst NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 서울 화재출동 인덱스
CREATE INDEX idx_seoul_fire_dispatch_year ON seoul_fire_dispatch(year);
CREATE INDEX idx_seoul_fire_dispatch_date ON seoul_fire_dispatch(ocrn_ymd);
CREATE INDEX idx_seoul_fire_dispatch_station ON seoul_fire_dispatch(frstn_nm);
CREATE INDEX idx_seoul_fire_dispatch_type ON seoul_fire_dispatch(fire_type_nm);
CREATE INDEX idx_seoul_fire_dispatch_casualties ON seoul_fire_dispatch(dth_cnt, injpsn_cnt);
CREATE INDEX idx_seoul_fire_dispatch_damage ON seoul_fire_dispatch(prpt_dam_amt);

-- ================================
-- 3. 서울 임야 화재출동 현황
-- ================================
CREATE TABLE seoul_forest_fire_dispatch (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    wrinv_no VARCHAR(50) NOT NULL,
    fire_type_nm VARCHAR(100),
    dth_cnt INTEGER DEFAULT 0,
    injpsn_cnt INTEGER DEFAULT 0,
    hnl_dam_cnt INTEGER DEFAULT 0,
    prpt_dam_amt BIGINT DEFAULT 0,
    ocrn_yr INTEGER,
    seasn_nm VARCHAR(20),
    qtr_no INTEGER,
    ocrn_ymd VARCHAR(20),
    ocrn_tm VARCHAR(20),
    ocrn_mm INTEGER,
    ocrn_day INTEGER,
    ocrn_hr INTEGER,
    ocrn_mn INTEGER,
    dclr_dow VARCHAR(20),
    frstn_nm VARCHAR(100),
    cntr_nm VARCHAR(100),
    lfdau_nm VARCHAR(100),
    dspt_req_tm VARCHAR(20),
    fire_supesn_req_tm VARCHAR(20),
    grnds_ctpv_nm VARCHAR(50),
    grnds_sgg_nm VARCHAR(50),
    cty_frmvl_se_nm VARCHAR(50),
    damg_rgn_lot NUMERIC,
    damg_rgn_lat NUMERIC,
    grnds_dstnc NUMERIC,
    cntr_grnds_dstnc NUMERIC,
    lfdau_grnds_dstnc NUMERIC,
    igtn_htsrc_lclsf_nm VARCHAR(100),
    igtn_htsrc_sclsf_nm VARCHAR(100),
    igtn_dmnt_lclsf_nm VARCHAR(100),
    igtn_dmnt_sclsf_nm VARCHAR(100),
    frst_igobj_lclsf_nm VARCHAR(100),
    frst_igobj_sclsf_nm VARCHAR(100),
    igtn_istr_lclsf_nm VARCHAR(100),
    igtn_istr_sclsf_nm VARCHAR(100),
    cmbs_expobj_lclsf_nm VARCHAR(100),
    cmbs_expobj_sclsf_nm VARCHAR(100),
    fclt_plc_lclsf_nm VARCHAR(100),
    fclt_plc_mclsf_nm VARCHAR(100),
    fclt_plc_sclsf_nm VARCHAR(100),
    fnd_fire_se_nm VARCHAR(100),
    fnd_fire_igtn_brnch_nm VARCHAR(100),
    -- 기상정보 (임야화재 특화)
    hr_unit_artmp NUMERIC,
    hr_unit_rn NUMERIC,
    hr_unit_wspd NUMERIC,
    hr_unit_wndrct INTEGER,
    hr_unit_hum NUMERIC,
    hr_unit_snwfl NUMERIC,
    hr_unit_vsdst NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 서울 임야화재 인덱스
CREATE INDEX idx_seoul_forest_fire_year ON seoul_forest_fire_dispatch(year);
CREATE INDEX idx_seoul_forest_fire_date ON seoul_forest_fire_dispatch(ocrn_ymd);
CREATE INDEX idx_seoul_forest_fire_station ON seoul_forest_fire_dispatch(frstn_nm);
CREATE INDEX idx_seoul_forest_fire_casualties ON seoul_forest_fire_dispatch(dth_cnt, injpsn_cnt);
CREATE INDEX idx_seoul_forest_fire_weather ON seoul_forest_fire_dispatch(hr_unit_artmp, hr_unit_wspd);

-- ================================
-- 4. 서울 차량 화재출동 현황
-- ================================
CREATE TABLE seoul_vehicle_fire_dispatch (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    wrinv_no VARCHAR(50) NOT NULL,
    fire_type_nm VARCHAR(100),
    dth_cnt INTEGER DEFAULT 0,
    injpsn_cnt INTEGER DEFAULT 0,
    hnl_dam_cnt INTEGER DEFAULT 0,
    prpt_dam_amt BIGINT DEFAULT 0,
    ocrn_yr INTEGER,
    seasn_nm VARCHAR(20),
    qtr_no INTEGER,
    ocrn_ymd VARCHAR(20),
    ocrn_tm VARCHAR(20),
    ocrn_mm INTEGER,
    ocrn_day INTEGER,
    ocrn_hr INTEGER,
    ocrn_mn INTEGER,
    dclr_dow VARCHAR(20),
    frstn_nm VARCHAR(100),
    cntr_nm VARCHAR(100),
    lfdau_nm VARCHAR(100),
    dspt_req_tm VARCHAR(20),
    fire_supesn_req_tm VARCHAR(20),
    grnds_ctpv_nm VARCHAR(50),
    grnds_sgg_nm VARCHAR(50),
    cty_frmvl_se_nm VARCHAR(50),
    damg_rgn_lot NUMERIC,
    damg_rgn_lat NUMERIC,
    grnds_dstnc NUMERIC,
    cntr_grnds_dstnc NUMERIC,
    lfdau_grnds_dstnc NUMERIC,
    igtn_htsrc_lclsf_nm VARCHAR(100),
    igtn_htsrc_sclsf_nm VARCHAR(100),
    igtn_dmnt_lclsf_nm VARCHAR(100),
    igtn_dmnt_sclsf_nm VARCHAR(100),
    frst_igobj_lclsf_nm VARCHAR(100),
    frst_igobj_sclsf_nm VARCHAR(100),
    igtn_istr_lclsf_nm VARCHAR(100),
    igtn_istr_sclsf_nm VARCHAR(100),
    cmbs_expobj_lclsf_nm VARCHAR(100),
    cmbs_expobj_sclsf_nm VARCHAR(100),
    fclt_plc_lclsf_nm VARCHAR(100),
    fclt_plc_mclsf_nm VARCHAR(100),
    fclt_plc_sclsf_nm VARCHAR(100),
    -- 차량 특화 필드
    igtn_plc_nm VARCHAR(100),
    vhcl_igtn_pstn_nm VARCHAR(100),
    emrg_cntrl_yn CHAR(1),
    -- 기상정보
    hr_unit_artmp NUMERIC,
    hr_unit_rn NUMERIC,
    hr_unit_wspd NUMERIC,
    hr_unit_wndrct INTEGER,
    hr_unit_hum NUMERIC,
    hr_unit_snwfl NUMERIC,
    hr_unit_vsdst NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 서울 차량화재 인덱스
CREATE INDEX idx_seoul_vehicle_fire_year ON seoul_vehicle_fire_dispatch(year);
CREATE INDEX idx_seoul_vehicle_fire_date ON seoul_vehicle_fire_dispatch(ocrn_ymd);
CREATE INDEX idx_seoul_vehicle_fire_station ON seoul_vehicle_fire_dispatch(frstn_nm);
CREATE INDEX idx_seoul_vehicle_fire_position ON seoul_vehicle_fire_dispatch(vhcl_igtn_pstn_nm);

-- ================================
-- 5. 서울 화재사고 구조출동 현황
-- ================================
CREATE TABLE seoul_rescue_dispatch (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    clmty_rscu_rptp_no VARCHAR(50) NOT NULL,
    acdnt_cs_nm VARCHAR(100),
    prcs_rslt_se_nm VARCHAR(100),
    dclr_ymd VARCHAR(20),
    dclr_tm VARCHAR(20),
    dclr_yr INTEGER,
    seasn_nm VARCHAR(20),
    qtr_no INTEGER,
    dclr_mm INTEGER,
    dclr_day INTEGER,
    dclr_hr INTEGER,
    dclr_mn INTEGER,
    dclr_dow VARCHAR(20),
    dspt_ymd VARCHAR(20),
    dspt_tm VARCHAR(20),
    dspt_yr INTEGER,
    dspt_mm INTEGER,
    dspt_day INTEGER,
    dspt_hr INTEGER,
    dspt_mn INTEGER,
    grnds_arvl_ymd VARCHAR(20),
    grnds_arvl_tm VARCHAR(20),
    grnds_arvl_yr INTEGER,
    grnds_arvl_mm INTEGER,
    grnds_arvl_day INTEGER,
    grnds_arvl_hr INTEGER,
    grnds_arvl_mn INTEGER,
    rscu_cmptn_ymd VARCHAR(20),
    rscu_cmptn_tm VARCHAR(20),
    rscu_cmptn_yr INTEGER,
    rscu_cmptn_mm INTEGER,
    rscu_cmptn_day INTEGER,
    rscu_cmptn_hr INTEGER,
    rscu_cmptn_mn INTEGER,
    cbk_ymd VARCHAR(20),
    cbk_tm VARCHAR(20),
    cbk_yr INTEGER,
    cbk_mm INTEGER,
    cbk_day INTEGER,
    cbk_hr INTEGER,
    cbk_mn INTEGER,
    grnds_ctpv_nm VARCHAR(50),
    grnds_sgg_nm VARCHAR(50),
    cty_frmvl_se_nm VARCHAR(50),
    damg_rgn_lot NUMERIC,
    damg_rgn_lat NUMERIC,
    grnds_dstnc NUMERIC,
    acdnt_ocrn_plc_nm VARCHAR(200),
    etc_ocrn_type_dtl_nm VARCHAR(200),
    acdnt_cs_assrt_nm VARCHAR(200),
    frstn_nm VARCHAR(100),
    cntr_nm VARCHAR(100),
    lfdau_nm VARCHAR(100),
    hr_unit_artmp NUMERIC,
    hr_unit_rn NUMERIC,
    hr_unit_wspd NUMERIC,
    hr_unit_wndrct INTEGER,
    hr_unit_hum NUMERIC,
    hr_unit_snwfl NUMERIC,
    hr_unit_vsdst NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 서울 구조출동 인덱스
CREATE INDEX idx_seoul_rescue_year ON seoul_rescue_dispatch(year);
CREATE INDEX idx_seoul_rescue_date ON seoul_rescue_dispatch(dclr_ymd);
CREATE INDEX idx_seoul_rescue_station ON seoul_rescue_dispatch(frstn_nm);
CREATE INDEX idx_seoul_rescue_result ON seoul_rescue_dispatch(prcs_rslt_se_nm);

-- ================================
-- 6. 전국 화재현황
-- ================================
CREATE TABLE national_fire_status (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    wrinv_no VARCHAR(50) NOT NULL,
    fire_type_nm VARCHAR(100),
    bldg_srtfrm_nm VARCHAR(100),
    bldg_strctr_nm VARCHAR(100),
    bldg_srtrf_nm VARCHAR(100),
    bldg_rscu_dngct NUMERIC,
    grnd_nofl INTEGER,
    udgd_nofl INTEGER,
    bldg_gfa NUMERIC,
    bttm_area NUMERIC,
    bldg_stts_nm VARCHAR(50),
    spfptg_nm VARCHAR(100),
    smtpr_lclsf_nm VARCHAR(100),
    smtpr_sclsf_nm VARCHAR(100),
    dth_cnt INTEGER DEFAULT 0,
    injpsn_cnt INTEGER DEFAULT 0,
    hnl_dam_cnt INTEGER DEFAULT 0,
    prpt_dam_amt BIGINT DEFAULT 0,
    dow_nm VARCHAR(20),
    frstn_nm VARCHAR(100),
    cntr_nm VARCHAR(100),
    rcpt_dt VARCHAR(14),
    dspt_dt VARCHAR(14),
    grnds_arvl_dt VARCHAR(14),
    bgnn_potfr_dt VARCHAR(14),
    prfect_potfr_dt VARCHAR(14),
    cbk_dt VARCHAR(14),
    dspt_req_hr VARCHAR(6),
    fire_supesn_hr VARCHAR(6),
    ctpv_nm VARCHAR(50),
    sgg_nm VARCHAR(50),
    frstn_grnds_dstnc NUMERIC,
    cntr_grnds_dstnc NUMERIC,
    lfdau_grnds_dstnc NUMERIC,
    igtn_htsrc_nm VARCHAR(100),
    igtn_htsrc_sclsf_nm VARCHAR(100),
    igtn_dmnt_lclsf_nm VARCHAR(100),
    igtn_dmnt_sclsf_nm VARCHAR(100),
    frst_igobj_lclsf_nm VARCHAR(100),
    frst_igobj_sclsf_nm VARCHAR(100),
    igtn_istr_lclsf_nm VARCHAR(100),
    igtn_istr_sclsf_nm VARCHAR(100),
    cmbs_expobj_lclsf_nm VARCHAR(100),
    cmbs_expobj_sclsf_nm VARCHAR(100),
    fclt_plc_lclsf_nm VARCHAR(100),
    fclt_plc_mclsf_nm VARCHAR(100),
    fclt_plc_sclsf_nm VARCHAR(100),
    igtn_flr_nm VARCHAR(50),
    so_area NUMERIC,
    fire_insrnc_oblg_trgt_yn CHAR(1),
    arson_mng_trgt_yn CHAR(1),
    mub_yn CHAR(1),
    vhcl_plc_nm VARCHAR(100),
    vhcl_igtn_pstn_nm VARCHAR(100),
    fnd_fire_se_nm VARCHAR(100),
    fnd_igtn_pstn_nm VARCHAR(100),
    hr_unit_artmp NUMERIC,
    hr_unit_wspd_info VARCHAR(50),
    wndrct_brng VARCHAR(50),
    hr_unit_hum NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 전국 화재현황 인덱스
CREATE INDEX idx_national_fire_year ON national_fire_status(year);
CREATE INDEX idx_national_fire_region ON national_fire_status(ctpv_nm, sgg_nm);
CREATE INDEX idx_national_fire_casualties ON national_fire_status(dth_cnt, injpsn_cnt);
CREATE INDEX idx_national_fire_damage ON national_fire_status(prpt_dam_amt);

-- ================================
-- 7. 메타데이터 초기 데이터 삽입
-- ================================
INSERT INTO dataset_schemas (dataset_type, table_name, description, data_category, keywords, schema_definition, query_examples, sample_queries) VALUES

-- 서울 화재출동 현황
('seoul_fire_dispatch', 'seoul_fire_dispatch', 
'서울특별시 건축물 화재출동 현황 - 아파트, 단독주택, 상가 등 건축물에서 발생한 화재사고 데이터', 
'fire_dispatch',
'["건축물화재", "건물화재", "아파트화재", "화재출동", "서울화재", "상가화재", "주택화재"]'::jsonb,
'{
  "fields": {
    "fire_type_nm": "화재유형 (건축/구조물, 기타 등)",
    "bldg_strctr_nm": "건물구조 (철근콘크리트조, 목조, 철골조 등)",
    "dth_cnt": "사망자수",
    "injpsn_cnt": "부상자수", 
    "prpt_dam_amt": "재산피해액 (천원 단위)",
    "ocrn_ymd": "발생일자 (YYYYMMDD)",
    "frstn_nm": "소방서명",
    "igtn_htsrc_lclsf_nm": "점화열원 대분류 (전기적요인, 담뱃불 등)",
    "fclt_plc_lclsf_nm": "시설장소 대분류 (주거, 상업, 산업시설 등)"
  },
  "common_patterns": ["WHERE year = 2024", "WHERE dth_cnt > 0", "WHERE prpt_dam_amt > 100000"]
}'::jsonb,
'["2024년 건축물 화재 중 사망자가 발생한 사건", "재산피해가 1억원 이상인 화재", "전기적 요인으로 발생한 화재"]'::jsonb,
'["SELECT fire_type_nm, dth_cnt, injpsn_cnt, prpt_dam_amt FROM seoul_fire_dispatch WHERE year = 2024 AND dth_cnt > 0", "SELECT frstn_nm, COUNT(*) FROM seoul_fire_dispatch WHERE year = 2024 GROUP BY frstn_nm ORDER BY COUNT(*) DESC"]'::jsonb),

-- 서울 임야 화재출동 현황  
('seoul_forest_fire_dispatch', 'seoul_forest_fire_dispatch',
'서울특별시 임야 화재출동 현황 - 산, 들판, 논밭에서 발생한 산불 및 들불 데이터, 기상정보 포함',
'fire_dispatch', 
'["임야화재", "산불", "들불", "산림화재", "들판화재", "기상정보"]'::jsonb,
'{
  "fields": {
    "fire_type_nm": "화재유형 (임야)",
    "dth_cnt": "사망자수",
    "injpsn_cnt": "부상자수",
    "prpt_dam_amt": "재산피해액 (천원 단위)", 
    "ocrn_ymd": "발생일자 (YYYYMMDD)",
    "frstn_nm": "소방서명",
    "hr_unit_artmp": "시간당 기온",
    "hr_unit_wspd": "시간당 풍속",
    "hr_unit_hum": "시간당 습도",
    "igtn_htsrc_lclsf_nm": "점화열원 (담뱃불, 라이터불 등)"
  },
  "weather_analysis": true
}'::jsonb,
'["봄철 임야화재 발생 현황", "강풍 시 발생한 산불", "담뱃불로 인한 들불"]'::jsonb,
'["SELECT * FROM seoul_forest_fire_dispatch WHERE ocrn_mm IN (3,4,5) AND year = 2024", "SELECT * FROM seoul_forest_fire_dispatch WHERE hr_unit_wspd > 5"]'::jsonb),

-- 서울 차량 화재출동 현황
('seoul_vehicle_fire_dispatch', 'seoul_vehicle_fire_dispatch',
'서울특별시 차량 화재출동 현황 - 자동차, 철도차량 등 차량에서 발생한 화재사고 데이터',
'fire_dispatch',
'["차량화재", "자동차화재", "차량출동", "차량점화위치"]'::jsonb,
'{
  "fields": {
    "fire_type_nm": "화재유형 (자동차/철도차량)",
    "dth_cnt": "사망자수",
    "injpsn_cnt": "부상자수",
    "prpt_dam_amt": "재산피해액 (천원 단위)",
    "ocrn_ymd": "발생일자 (YYYYMMDD)", 
    "frstn_nm": "소방서명",
    "vhcl_igtn_pstn_nm": "차량점화위치 (엔진룸, 차체 등)",
    "igtn_htsrc_lclsf_nm": "점화열원 (마찰/전도/복사, 작동기기 등)"
  }
}'::jsonb,
'["엔진룸에서 발생한 차량화재", "고속도로 차량화재", "전기적 요인 차량화재"]'::jsonb,
'["SELECT * FROM seoul_vehicle_fire_dispatch WHERE vhcl_igtn_pstn_nm LIKE \"%엔진%\"", "SELECT COUNT(*) FROM seoul_vehicle_fire_dispatch WHERE year = 2024 GROUP BY ocrn_mm"]'::jsonb),

-- 서울 화재사고 구조출동 현황
('seoul_rescue_dispatch', 'seoul_rescue_dispatch', 
'서울특별시 화재사고 구조출동 현황 - 화재 관련 인명구조 및 안전조치 활동 데이터',
'rescue_dispatch',
'["구조출동", "인명구조", "화재구조", "구조활동", "안전조치"]'::jsonb,
'{
  "fields": {
    "acdnt_cs_nm": "사고원인명 (화재)",
    "prcs_rslt_se_nm": "처리결과 구분 (인명구조, 안전조치, 오인신고 등)",
    "dclr_ymd": "신고일자 (YYYYMMDD)",
    "rscu_cmptn_ymd": "구조완료일자 (YYYYMMDD)",
    "frstn_nm": "소방서명",
    "acdnt_ocrn_plc_nm": "사고발생장소명",
    "dspt_tm": "출동시간",
    "grnds_arvl_tm": "현장도착시간"
  },
  "response_time_analysis": true
}'::jsonb,  
'["인명구조가 성공한 화재사고", "출동시간이 빠른 구조활동", "오인신고 현황"]'::jsonb,
'["SELECT * FROM seoul_rescue_dispatch WHERE prcs_rslt_se_nm = \"인명구조\"", "SELECT frstn_nm, AVG(grnds_dstnc) FROM seoul_rescue_dispatch GROUP BY frstn_nm"]'::jsonb),

-- 전국 화재현황
('national_fire_status', 'national_fire_status',
'전국 화재현황 통계 - 전국 시도별 화재발생 현황 및 피해 통계 데이터', 
'national_statistics',
'["전국화재", "시도별화재", "화재통계", "화재현황", "전국통계"]'::jsonb,
'{
  "fields": {
    "ctpv_nm": "시도명 (서울특별시, 부산광역시 등)",
    "sgg_nm": "시군구명", 
    "fire_type_nm": "화재유형",
    "dth_cnt": "사망자수",
    "injpsn_cnt": "부상자수",
    "prpt_dam_amt": "재산피해액 (천원 단위)",
    "rcpt_dt": "접수일시",
    "dspt_dt": "출동일시", 
    "grnds_arvl_dt": "현장도착일시",
    "frstn_nm": "소방서명"
  },
  "regional_analysis": true
}'::jsonb,
'["서울시 화재 현황", "경기도 화재 통계", "사망자 발생 화재 지역별 분석"]'::jsonb,
'["SELECT ctpv_nm, COUNT(*) FROM national_fire_status WHERE year = 2023 GROUP BY ctpv_nm", "SELECT * FROM national_fire_status WHERE dth_cnt > 0 AND ctpv_nm = \"서울특별시\""]'::jsonb);

-- ================================
-- 8. 업데이트 트리거 생성
-- ================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_dataset_schemas_updated_at 
    BEFORE UPDATE ON dataset_schemas 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ================================
-- 9. 뷰 생성 (종합 조회용)
-- ================================
CREATE VIEW v_all_fire_dispatch AS
SELECT 
    'building' as fire_category,
    year, 
    fire_type_nm,
    dth_cnt,
    injpsn_cnt, 
    prpt_dam_amt,
    ocrn_ymd,
    frstn_nm,
    grnds_sgg_nm as location,
    igtn_htsrc_lclsf_nm as ignition_source,
    NULL as vehicle_position,
    'seoul_fire_dispatch' as source_table
FROM seoul_fire_dispatch

UNION ALL

SELECT 
    'forest' as fire_category,
    year,
    fire_type_nm, 
    dth_cnt,
    injpsn_cnt,
    prpt_dam_amt,
    ocrn_ymd,
    frstn_nm,
    grnds_sgg_nm as location,
    igtn_htsrc_lclsf_nm as ignition_source, 
    NULL as vehicle_position,
    'seoul_forest_fire_dispatch' as source_table
FROM seoul_forest_fire_dispatch

UNION ALL

SELECT 
    'vehicle' as fire_category,
    year,
    fire_type_nm,
    dth_cnt, 
    injpsn_cnt,
    prpt_dam_amt,
    ocrn_ymd,
    frstn_nm,
    grnds_sgg_nm as location,
    igtn_htsrc_lclsf_nm as ignition_source,
    vhcl_igtn_pstn_nm as vehicle_position,
    'seoul_vehicle_fire_dispatch' as source_table  
FROM seoul_vehicle_fire_dispatch;

-- ================================
-- 10. 권한 설정 (필요시)
-- ================================
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO fire_safety_user;
-- GRANT INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO fire_safety_admin;

-- ================================
-- 마이그레이션 완료 확인
-- ================================
SELECT 
    'Migration completed successfully!' as status,
    COUNT(*) as total_schemas
FROM dataset_schemas;