-- ================================
-- 🔥 Korean-Only Fire Safety Schema
-- 한글 컬럼명 전용 소방 안전 데이터 스키마
-- ================================

-- 기존 모든 테이블 삭제
DROP TABLE IF EXISTS fire_safety_data CASCADE;
DROP TABLE IF EXISTS dataset_schemas CASCADE;
DROP TABLE IF EXISTS seoul_fire_dispatch CASCADE;
DROP TABLE IF EXISTS seoul_forest_fire_dispatch CASCADE;  
DROP TABLE IF EXISTS seoul_vehicle_fire_dispatch CASCADE;
DROP TABLE IF EXISTS seoul_rescue_dispatch CASCADE;
DROP TABLE IF EXISTS national_fire_status CASCADE;

-- 한글 테이블들도 삭제 (새로 생성)
DROP TABLE IF EXISTS seoul_fire_dispatch_kr CASCADE;
DROP TABLE IF EXISTS seoul_forest_fire_dispatch_kr CASCADE;
DROP TABLE IF EXISTS seoul_vehicle_fire_dispatch_kr CASCADE;  
DROP TABLE IF EXISTS seoul_rescue_dispatch_kr CASCADE;
DROP TABLE IF EXISTS national_fire_status_kr CASCADE;

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
-- 2. 서울 화재출동 현황 (한글 컬럼명)
-- ================================
CREATE TABLE seoul_fire_dispatch (
    ID SERIAL PRIMARY KEY,
    연도 INTEGER NOT NULL,
    화재조사번호 VARCHAR(50) NOT NULL,
    화재유형명 VARCHAR(100),
    건물주구조형태명 VARCHAR(100),
    건물구조명 VARCHAR(100),
    건물지붕구조명 VARCHAR(100),
    건물위험등급 INTEGER,
    지상층수 INTEGER,
    지하층수 INTEGER,
    연면적 NUMERIC,
    바닥면적 NUMERIC,
    건물상태명 VARCHAR(50),
    사망자수 INTEGER DEFAULT 0,
    부상자수 INTEGER DEFAULT 0,
    인명피해수 INTEGER DEFAULT 0,
    재산피해액 BIGINT DEFAULT 0,
    발생연도 INTEGER,
    계절명 VARCHAR(20),
    분기 INTEGER,
    발생일자 VARCHAR(20),
    발생시각 VARCHAR(20),
    발생월 INTEGER,
    발생일 INTEGER,
    발생시 INTEGER,
    발생분 INTEGER,
    신고요일 VARCHAR(20),
    소방서명 VARCHAR(100),
    센터명 VARCHAR(100),
    ladder차량명 VARCHAR(100),
    출동요청시각 VARCHAR(20),
    화재진압요청시각 VARCHAR(20),
    현장시도명 VARCHAR(50),
    현장시군구명 VARCHAR(50),
    도시농촌구분명 VARCHAR(50),
    피해지역경도 NUMERIC,
    피해지역위도 NUMERIC,
    현장거리 NUMERIC,
    센터현장거리 NUMERIC,
    ladder차량현장거리 NUMERIC,
    점화열원대분류명 VARCHAR(100),
    점화열원소분류명 VARCHAR(100),
    점화물대분류명 VARCHAR(100),
    점화물소분류명 VARCHAR(100),
    최초점화물대분류명 VARCHAR(100),
    최초점화물소분류명 VARCHAR(100),
    점화인자대분류명 VARCHAR(100),
    점화인자소분류명 VARCHAR(100),
    연소확대물대분류명 VARCHAR(100),
    연소확대물소분류명 VARCHAR(100),
    시설장소대분류명 VARCHAR(100),
    시설장소중분류명 VARCHAR(100),
    시설장소소분류명 VARCHAR(100),
    점화층명 VARCHAR(50),
    소실면적 NUMERIC,
    화재보험의무가입대상여부 CHAR(1),
    방화관리대상여부 CHAR(1),
    다중이용업소여부 CHAR(1),
    응급제어여부 CHAR(1),
    점화장소명 VARCHAR(100),
    차량점화위치명 VARCHAR(100),
    화재발견구분명 VARCHAR(100),
    화재발견점화부위명 VARCHAR(100),
    시간당기온 NUMERIC,
    시간당강수량 NUMERIC,
    시간당풍속 NUMERIC,
    시간당풍향 INTEGER,
    시간당습도 NUMERIC,
    시간당강설량 NUMERIC,
    시간당가시거리 NUMERIC,
    생성일시 TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_seoul_fire_dispatch_연도 ON seoul_fire_dispatch(연도);
CREATE INDEX idx_seoul_fire_dispatch_발생일자 ON seoul_fire_dispatch(발생일자);
CREATE INDEX idx_seoul_fire_dispatch_소방서명 ON seoul_fire_dispatch(소방서명);
CREATE INDEX idx_seoul_fire_dispatch_화재유형명 ON seoul_fire_dispatch(화재유형명);
CREATE INDEX idx_seoul_fire_dispatch_피해 ON seoul_fire_dispatch(사망자수, 부상자수);
CREATE INDEX idx_seoul_fire_dispatch_재산피해액 ON seoul_fire_dispatch(재산피해액);

-- ================================
-- 3. 서울 임야 화재출동 현황
-- ================================
CREATE TABLE seoul_forest_fire_dispatch (
    ID SERIAL PRIMARY KEY,
    연도 INTEGER NOT NULL,
    화재조사번호 VARCHAR(50) NOT NULL,
    화재유형명 VARCHAR(100),
    사망자수 INTEGER DEFAULT 0,
    부상자수 INTEGER DEFAULT 0,
    인명피해수 INTEGER DEFAULT 0,
    재산피해액 BIGINT DEFAULT 0,
    발생연도 INTEGER,
    계절명 VARCHAR(20),
    분기 INTEGER,
    발생일자 VARCHAR(20),
    발생시각 VARCHAR(20),
    발생월 INTEGER,
    발생일 INTEGER,
    발생시 INTEGER,
    발생분 INTEGER,
    신고요일 VARCHAR(20),
    소방서명 VARCHAR(100),
    센터명 VARCHAR(100),
    ladder차량명 VARCHAR(100),
    출동요청시각 VARCHAR(20),
    화재진압요청시각 VARCHAR(20),
    현장시도명 VARCHAR(50),
    현장시군구명 VARCHAR(50),
    도시농촌구분명 VARCHAR(50),
    피해지역경도 NUMERIC,
    피해지역위도 NUMERIC,
    현장거리 NUMERIC,
    센터현장거리 NUMERIC,
    ladder차량현장거리 NUMERIC,
    점화열원대분류명 VARCHAR(100),
    점화열원소분류명 VARCHAR(100),
    점화물대분류명 VARCHAR(100),
    점화물소분류명 VARCHAR(100),
    최초점화물대분류명 VARCHAR(100),
    최초점화물소분류명 VARCHAR(100),
    점화인자대분류명 VARCHAR(100),
    점화인자소분류명 VARCHAR(100),
    연소확대물대분류명 VARCHAR(100),
    연소확대물소분류명 VARCHAR(100),
    시설장소대분류명 VARCHAR(100),
    시설장소중분류명 VARCHAR(100),
    시설장소소분류명 VARCHAR(100),
    화재발견구분명 VARCHAR(100),
    화재발견점화부위명 VARCHAR(100),
    -- 기상정보 (임야화재 특화)
    시간당기온 NUMERIC,
    시간당강수량 NUMERIC,
    시간당풍속 NUMERIC,
    시간당풍향 INTEGER,
    시간당습도 NUMERIC,
    시간당강설량 NUMERIC,
    시간당가시거리 NUMERIC,
    생성일시 TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_seoul_forest_fire_연도 ON seoul_forest_fire_dispatch(연도);
CREATE INDEX idx_seoul_forest_fire_발생일자 ON seoul_forest_fire_dispatch(발생일자);
CREATE INDEX idx_seoul_forest_fire_소방서명 ON seoul_forest_fire_dispatch(소방서명);
CREATE INDEX idx_seoul_forest_fire_피해 ON seoul_forest_fire_dispatch(사망자수, 부상자수);
CREATE INDEX idx_seoul_forest_fire_기상 ON seoul_forest_fire_dispatch(시간당기온, 시간당풍속);

-- ================================
-- 4. 서울 차량 화재출동 현황
-- ================================
CREATE TABLE seoul_vehicle_fire_dispatch (
    ID SERIAL PRIMARY KEY,
    연도 INTEGER NOT NULL,
    화재조사번호 VARCHAR(50) NOT NULL,
    화재유형명 VARCHAR(100),
    사망자수 INTEGER DEFAULT 0,
    부상자수 INTEGER DEFAULT 0,
    인명피해수 INTEGER DEFAULT 0,
    재산피해액 BIGINT DEFAULT 0,
    발생연도 INTEGER,
    계절명 VARCHAR(20),
    분기 INTEGER,
    발생일자 VARCHAR(20),
    발생시각 VARCHAR(20),
    발생월 INTEGER,
    발생일 INTEGER,
    발생시 INTEGER,
    발생분 INTEGER,
    신고요일 VARCHAR(20),
    소방서명 VARCHAR(100),
    센터명 VARCHAR(100),
    ladder차량명 VARCHAR(100),
    출동요청시각 VARCHAR(20),
    화재진압요청시각 VARCHAR(20),
    현장시도명 VARCHAR(50),
    현장시군구명 VARCHAR(50),
    도시농촌구분명 VARCHAR(50),
    피해지역경도 NUMERIC,
    피해지역위도 NUMERIC,
    현장거리 NUMERIC,
    센터현장거리 NUMERIC,
    ladder차량현장거리 NUMERIC,
    점화열원대분류명 VARCHAR(100),
    점화열원소분류명 VARCHAR(100),
    점화물대분류명 VARCHAR(100),
    점화물소분류명 VARCHAR(100),
    최초점화물대분류명 VARCHAR(100),
    최초점화물소분류명 VARCHAR(100),
    점화인자대분류명 VARCHAR(100),
    점화인자소분류명 VARCHAR(100),
    연소확대물대분류명 VARCHAR(100),
    연소확대물소분류명 VARCHAR(100),
    시설장소대분류명 VARCHAR(100),
    시설장소중분류명 VARCHAR(100),
    시설장소소분류명 VARCHAR(100),
    -- 차량 특화 필드
    점화장소명 VARCHAR(100),
    차량점화위치명 VARCHAR(100),
    응급제어여부 CHAR(1),
    -- 기상정보
    시간당기온 NUMERIC,
    시간당강수량 NUMERIC,
    시간당풍속 NUMERIC,
    시간당풍향 INTEGER,
    시간당습도 NUMERIC,
    시간당강설량 NUMERIC,
    시간당가시거리 NUMERIC,
    생성일시 TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_seoul_vehicle_fire_연도 ON seoul_vehicle_fire_dispatch(연도);
CREATE INDEX idx_seoul_vehicle_fire_발생일자 ON seoul_vehicle_fire_dispatch(발생일자);
CREATE INDEX idx_seoul_vehicle_fire_소방서명 ON seoul_vehicle_fire_dispatch(소방서명);
CREATE INDEX idx_seoul_vehicle_fire_차량위치 ON seoul_vehicle_fire_dispatch(차량점화위치명);

-- ================================
-- 5. 서울 화재사고 구조출동 현황
-- ================================
CREATE TABLE seoul_rescue_dispatch (
    ID SERIAL PRIMARY KEY,
    연도 INTEGER NOT NULL,
    재난구조신고번호 VARCHAR(50) NOT NULL,
    사고원인명 VARCHAR(100),
    처리결과구분명 VARCHAR(100),
    신고일자 VARCHAR(20),
    신고시각 VARCHAR(20),
    신고연도 INTEGER,
    계절명 VARCHAR(20),
    분기 INTEGER,
    신고월 INTEGER,
    신고일 INTEGER,
    신고시 INTEGER,
    신고분 INTEGER,
    신고요일 VARCHAR(20),
    출동일자 VARCHAR(20),
    출동시각 VARCHAR(20),
    출동연도 INTEGER,
    출동월 INTEGER,
    출동일 INTEGER,
    출동시 INTEGER,
    출동분 INTEGER,
    현장도착일자 VARCHAR(20),
    현장도착시각 VARCHAR(20),
    현장도착연도 INTEGER,
    현장도착월 INTEGER,
    현장도착일 INTEGER,
    현장도착시 INTEGER,
    현장도착분 INTEGER,
    구조완료일자 VARCHAR(20),
    구조완료시각 VARCHAR(20),
    구조완료연도 INTEGER,
    구조완료월 INTEGER,
    구조완료일 INTEGER,
    구조완료시 INTEGER,
    구조완료분 INTEGER,
    철수일자 VARCHAR(20),
    철수시각 VARCHAR(20),
    철수연도 INTEGER,
    철수월 INTEGER,
    철수일 INTEGER,
    철수시 INTEGER,
    철수분 INTEGER,
    현장시도명 VARCHAR(50),
    현장시군구명 VARCHAR(50),
    도시농촌구분명 VARCHAR(50),
    피해지역경도 NUMERIC,
    피해지역위도 NUMERIC,
    현장거리 NUMERIC,
    사고발생장소명 VARCHAR(200),
    기타발생유형상세명 VARCHAR(200),
    사고원인주장명 VARCHAR(200),
    소방서명 VARCHAR(100),
    센터명 VARCHAR(100),
    ladder차량명 VARCHAR(100),
    시간당기온 NUMERIC,
    시간당강수량 NUMERIC,
    시간당풍속 NUMERIC,
    시간당풍향 INTEGER,
    시간당습도 NUMERIC,
    시간당강설량 NUMERIC,
    시간당가시거리 NUMERIC,
    생성일시 TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_seoul_rescue_연도 ON seoul_rescue_dispatch(연도);
CREATE INDEX idx_seoul_rescue_신고일자 ON seoul_rescue_dispatch(신고일자);
CREATE INDEX idx_seoul_rescue_소방서명 ON seoul_rescue_dispatch(소방서명);
CREATE INDEX idx_seoul_rescue_처리결과 ON seoul_rescue_dispatch(처리결과구분명);

-- ================================
-- 6. 전국 화재현황
-- ================================
CREATE TABLE national_fire_status (
    ID SERIAL PRIMARY KEY,
    연도 INTEGER NOT NULL,
    화재조사번호 VARCHAR(50) NOT NULL,
    화재유형명 VARCHAR(100),
    건물주구조형태명 VARCHAR(100),
    건물구조명 VARCHAR(100),
    건물지붕구조명 VARCHAR(100),
    건물위험등급 NUMERIC,
    지상층수 INTEGER,
    지하층수 INTEGER,
    건물연면적 NUMERIC,
    바닥면적 NUMERIC,
    건물상태명 VARCHAR(50),
    소방시설명 VARCHAR(100),
    연기감지기대분류명 VARCHAR(100),
    연기감지기소분류명 VARCHAR(100),
    사망자수 INTEGER DEFAULT 0,
    부상자수 INTEGER DEFAULT 0,
    인명피해수 INTEGER DEFAULT 0,
    재산피해액 BIGINT DEFAULT 0,
    요일명 VARCHAR(20),
    소방서명 VARCHAR(100),
    센터명 VARCHAR(100),
    접수일시 VARCHAR(14),
    출동일시 VARCHAR(14),
    현장도착일시 VARCHAR(14),
    진화개시일시 VARCHAR(14),
    완전진화일시 VARCHAR(14),
    철수일시 VARCHAR(14),
    출동요청시각 VARCHAR(6),
    화재진압시각 VARCHAR(6),
    시도명 VARCHAR(50),
    시군구명 VARCHAR(50),
    소방서현장거리 NUMERIC,
    센터현장거리 NUMERIC,
    ladder차량현장거리 NUMERIC,
    점화열원명 VARCHAR(100),
    점화열원소분류명 VARCHAR(100),
    점화물대분류명 VARCHAR(100),
    점화물소분류명 VARCHAR(100),
    최초점화물대분류명 VARCHAR(100),
    최초점화물소분류명 VARCHAR(100),
    점화인자대분류명 VARCHAR(100),
    점화인자소분류명 VARCHAR(100),
    연소확대물대분류명 VARCHAR(100),
    연소확대물소분류명 VARCHAR(100),
    시설장소대분류명 VARCHAR(100),
    시설장소중분류명 VARCHAR(100),
    시설장소소분류명 VARCHAR(100),
    점화층명 VARCHAR(50),
    소실면적 NUMERIC,
    화재보험의무가입대상여부 CHAR(1),
    방화관리대상여부 CHAR(1),
    다중이용업소여부 CHAR(1),
    차량장소명 VARCHAR(100),
    차량점화위치명 VARCHAR(100),
    화재발견구분명 VARCHAR(100),
    화재발견점화위치명 VARCHAR(100),
    시간당기온 NUMERIC,
    시간당풍속정보 VARCHAR(50),
    풍향방위 VARCHAR(50),
    시간당습도 NUMERIC,
    생성일시 TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_national_fire_연도 ON national_fire_status(연도);
CREATE INDEX idx_national_fire_지역 ON national_fire_status(시도명, 시군구명);
CREATE INDEX idx_national_fire_피해 ON national_fire_status(사망자수, 부상자수);
CREATE INDEX idx_national_fire_재산피해액 ON national_fire_status(재산피해액);

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
    "화재유형명": "화재유형 (건축/구조물, 기타 등)",
    "건물구조명": "건물구조 (철근콘크리트조, 목조, 철골조 등)",
    "사망자수": "사망자수",
    "부상자수": "부상자수", 
    "재산피해액": "재산피해액 (천원 단위)",
    "발생일자": "발생일자 (YYYYMMDD)",
    "소방서명": "소방서명",
    "점화열원대분류명": "점화열원 대분류 (전기적요인, 담뱃불 등)",
    "시설장소대분류명": "시설장소 대분류 (주거, 상업, 산업시설 등)"
  },
  "common_patterns": ["WHERE 연도 = 2024", "WHERE 사망자수 > 0", "WHERE 재산피해액 > 100000"]
}'::jsonb,
'["2024년 건축물 화재 중 사망자가 발생한 사건", "재산피해가 1억원 이상인 화재", "전기적 요인으로 발생한 화재"]'::jsonb,
'["SELECT 화재유형명, 사망자수, 부상자수, 재산피해액 FROM seoul_fire_dispatch WHERE 연도 = 2024 AND 사망자수 > 0", "SELECT 소방서명, COUNT(*) FROM seoul_fire_dispatch WHERE 연도 = 2024 GROUP BY 소방서명 ORDER BY COUNT(*) DESC"]'::jsonb),

-- 서울 임야 화재출동 현황
('seoul_forest_fire_dispatch', 'seoul_forest_fire_dispatch',
'서울특별시 임야 화재출동 현황 - 산, 들판, 논밭에서 발생한 산불 및 들불 데이터, 기상정보 포함',
'fire_dispatch', 
'["임야화재", "산불", "들불", "산림화재", "들판화재", "기상정보"]'::jsonb,
'{
  "fields": {
    "화재유형명": "화재유형 (임야)",
    "사망자수": "사망자수",
    "부상자수": "부상자수",
    "재산피해액": "재산피해액 (천원 단위)", 
    "발생일자": "발생일자 (YYYYMMDD)",
    "소방서명": "소방서명",
    "시간당기온": "시간당 기온",
    "시간당풍속": "시간당 풍속",
    "시간당습도": "시간당 습도",
    "점화열원대분류명": "점화열원 (담뱃불, 라이터불 등)"
  },
  "weather_analysis": true
}'::jsonb,
'["봄철 임야화재 발생 현황", "강풍 시 발생한 산불", "담뱃불로 인한 들불"]'::jsonb,
'["SELECT * FROM seoul_forest_fire_dispatch WHERE 발생월 IN (3,4,5) AND 연도 = 2024", "SELECT * FROM seoul_forest_fire_dispatch WHERE 시간당풍속 > 5"]'::jsonb),

-- 서울 차량 화재출동 현황
('seoul_vehicle_fire_dispatch', 'seoul_vehicle_fire_dispatch',
'서울특별시 차량 화재출동 현황 - 자동차, 철도차량 등 차량에서 발생한 화재사고 데이터',
'fire_dispatch',
'["차량화재", "자동차화재", "차량출동", "차량점화위치"]'::jsonb,
'{
  "fields": {
    "화재유형명": "화재유형 (자동차/철도차량)",
    "사망자수": "사망자수",
    "부상자수": "부상자수",
    "재산피해액": "재산피해액 (천원 단위)",
    "발생일자": "발생일자 (YYYYMMDD)", 
    "소방서명": "소방서명",
    "차량점화위치명": "차량점화위치 (엔진룸, 차체 등)",
    "점화열원대분류명": "점화열원 (마찰/전도/복사, 작동기기 등)"
  }
}'::jsonb,
'["엔진룸에서 발생한 차량화재", "고속도로 차량화재", "전기적 요인 차량화재"]'::jsonb,
'["SELECT * FROM seoul_vehicle_fire_dispatch WHERE 차량점화위치명 LIKE \"%엔진%\"", "SELECT COUNT(*) FROM seoul_vehicle_fire_dispatch WHERE 연도 = 2024 GROUP BY 발생월"]'::jsonb),

-- 서울 화재사고 구조출동 현황
('seoul_rescue_dispatch', 'seoul_rescue_dispatch', 
'서울특별시 화재사고 구조출동 현황 - 화재 관련 인명구조 및 안전조치 활동 데이터',
'rescue_dispatch',
'["구조출동", "인명구조", "화재구조", "구조활동", "안전조치"]'::jsonb,
'{
  "fields": {
    "사고원인명": "사고원인명 (화재)",
    "처리결과구분명": "처리결과 구분 (인명구조, 안전조치, 오인신고 등)",
    "신고일자": "신고일자 (YYYYMMDD)",
    "구조완료일자": "구조완료일자 (YYYYMMDD)",
    "소방서명": "소방서명",
    "사고발생장소명": "사고발생장소명",
    "출동시각": "출동시간",
    "현장도착시각": "현장도착시간"
  },
  "response_time_analysis": true
}'::jsonb,  
'["인명구조가 성공한 화재사고", "출동시간이 빠른 구조활동", "오인신고 현황"]'::jsonb,
'["SELECT * FROM seoul_rescue_dispatch WHERE 처리결과구분명 = \"인명구조\"", "SELECT 소방서명, AVG(현장거리) FROM seoul_rescue_dispatch GROUP BY 소방서명"]'::jsonb),

-- 전국 화재현황
('national_fire_status', 'national_fire_status',
'전국 화재현황 통계 - 전국 시도별 화재발생 현황 및 피해 통계 데이터', 
'national_statistics',
'["전국화재", "시도별화재", "화재통계", "화재현황", "전국통계"]'::jsonb,
'{
  "fields": {
    "시도명": "시도명 (서울특별시, 부산광역시 등)",
    "시군구명": "시군구명", 
    "화재유형명": "화재유형",
    "사망자수": "사망자수",
    "부상자수": "부상자수",
    "재산피해액": "재산피해액 (천원 단위)",
    "접수일시": "접수일시",
    "출동일시": "출동일시", 
    "현장도착일시": "현장도착일시",
    "소방서명": "소방서명"
  },
  "regional_analysis": true
}'::jsonb,
'["서울시 화재 현황", "경기도 화재 통계", "사망자 발생 화재 지역별 분석"]'::jsonb,
'["SELECT 시도명, COUNT(*) FROM national_fire_status WHERE 연도 = 2023 GROUP BY 시도명", "SELECT * FROM national_fire_status WHERE 사망자수 > 0 AND 시도명 = \"서울특별시\""]'::jsonb);

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
-- 9. 종합 뷰 생성
-- ================================
DROP VIEW IF EXISTS v_all_fire_dispatch CASCADE;
CREATE VIEW v_all_fire_dispatch AS
SELECT 
    'building' as 화재분류,
    연도, 
    화재유형명,
    사망자수,
    부상자수, 
    재산피해액,
    발생일자,
    소방서명,
    현장시군구명 as 위치,
    점화열원대분류명 as 점화원인,
    NULL as 차량위치,
    'seoul_fire_dispatch' as 원본테이블
FROM seoul_fire_dispatch

UNION ALL

SELECT 
    'forest' as 화재분류,
    연도,
    화재유형명, 
    사망자수,
    부상자수,
    재산피해액,
    발생일자,
    소방서명,
    현장시군구명 as 위치,
    점화열원대분류명 as 점화원인, 
    NULL as 차량위치,
    'seoul_forest_fire_dispatch' as 원본테이블
FROM seoul_forest_fire_dispatch

UNION ALL

SELECT 
    'vehicle' as 화재분류,
    연도,
    화재유형명,
    사망자수, 
    부상자수,
    재산피해액,
    발생일자,
    소방서명,
    현장시군구명 as 위치,
    점화열원대분류명 as 점화원인,
    차량점화위치명 as 차량위치,
    'seoul_vehicle_fire_dispatch' as 원본테이블  
FROM seoul_vehicle_fire_dispatch;

-- ================================
-- 마이그레이션 완료 확인
-- ================================
SELECT 
    '한글 전용 테이블 생성 완료!' as 상태,
    COUNT(*) as 총_스키마수
FROM dataset_schemas;