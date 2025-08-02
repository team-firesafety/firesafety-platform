#!/usr/bin/env python3
"""
🔥 Fire Safety Data Loader
하이브리드 테이블 구조용 데이터 로더
"""

import pandas as pd
import psycopg
from psycopg.rows import dict_row
from pathlib import Path
import os
import logging
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FireSafetyDataLoader:
    """소방 안전 데이터 로더"""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Args:
            db_config: 데이터베이스 연결 설정
        """
        self.db_config = db_config
        self.conn = None
        
        # 데이터셋 매핑 (영어 폴더명)
        self.dataset_mapping = {
            "seoul_fire_dispatch": {
                "table": "seoul_fire_dispatch",
                "dataset_type": "seoul_fire_dispatch",
                "file_pattern": r"fire_dispatch_(\d{4})\.csv"
            },
            "seoul_forest_fire_dispatch": {
                "table": "seoul_forest_fire_dispatch", 
                "dataset_type": "seoul_forest_fire_dispatch",
                "file_pattern": r"forest_fire_dispatch_(\d{4})\.csv"
            },
            "seoul_vehicle_fire_dispatch": {
                "table": "seoul_vehicle_fire_dispatch",
                "dataset_type": "seoul_vehicle_fire_dispatch", 
                "file_pattern": r"vehicle_fire_dispatch_(\d{4})\.csv"
            },
            "seoul_rescue_dispatch": {
                "table": "seoul_rescue_dispatch",
                "dataset_type": "seoul_rescue_dispatch",
                "file_pattern": r"rescue_dispatch_(\d{4})\.csv"
            },
            "national_fire_status": {
                "table": "national_fire_status",
                "dataset_type": "national_fire_status",
                "file_pattern": r"national_fire_status_(\d{4})\.csv"
            }
        }
    
    def connect_db(self):
        """데이터베이스 연결"""
        try:
            # psycopg3는 connection string을 사용
            conninfo = f"host={self.db_config['host']} dbname={self.db_config['database']} user={self.db_config['user']} port={self.db_config['port']}"
            self.conn = psycopg.connect(conninfo)
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def disconnect_db(self):
        """데이터베이스 연결 해제"""
        if self.conn:
            self.conn.close()
            logger.info("Database disconnected")
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """컬럼명 정리 (BOM 문자 제거, 소문자 변환)"""
        # BOM 문자 제거
        df.columns = df.columns.str.replace('\ufeff', '')
        # 소문자 변환
        df.columns = df.columns.str.lower()
        return df
    
    def extract_year_from_filename(self, filename: str, pattern: str) -> Optional[int]:
        """파일명에서 연도 추출"""
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
        return None
    
    def prepare_data_for_table(self, df: pd.DataFrame, table: str, year: int) -> List[Dict[str, Any]]:
        """테이블별 데이터 전처리"""
        records = []
        
        for _, row in df.iterrows():
            record = {"year": year}
            
            # 각 컬럼을 테이블 스키마에 맞게 매핑
            for col in df.columns:
                value = row[col]
                
                # NULL/NaN 처리
                if pd.isna(value) or value == '' or str(value).strip() == '':
                    value = None
                # Integer 타입 처리 (모든 정수 컬럼)
                elif col in ['dth_cnt', 'injpsn_cnt', 'hnl_dam_cnt', 'ocrn_yr', 'qtr_no', 'ocrn_mm', 'ocrn_day', 'ocrn_hr', 'ocrn_mn',
                           'bldg_rscu_dngct', 'grnd_nofl', 'udgd_nofl', 'hr_unit_wndrct', 'dclr_yr', 'dclr_mm', 'dclr_day', 'dclr_hr', 'dclr_mn',
                           'dspt_yr', 'dspt_mm', 'dspt_day', 'dspt_hr', 'dspt_mn', 'grnds_arvl_yr', 'grnds_arvl_mm', 'grnds_arvl_day', 
                           'grnds_arvl_hr', 'grnds_arvl_mn', 'rscu_cmptn_yr', 'rscu_cmptn_mm', 'rscu_cmptn_day', 'rscu_cmptn_hr', 'rscu_cmptn_mn',
                           'cbk_yr', 'cbk_mm', 'cbk_day', 'cbk_hr', 'cbk_mn']:
                    try:
                        if value is not None and str(value).strip() != '':
                            # 소수점이 있는 경우 정수로 변환
                            if '.' in str(value):
                                value = int(float(str(value)))
                            else:
                                value = int(str(value))
                        else:
                            value = None
                    except (ValueError, TypeError):
                        value = None
                # BIGINT 타입 처리 (큰 숫자)        
                elif col in ['prpt_dam_amt']:
                    try:
                        if value is not None and str(value).strip() != '':
                            if '.' in str(value):
                                value = int(float(str(value)))
                            else:
                                value = int(str(value))
                        else:
                            value = 0
                    except (ValueError, TypeError):
                        value = 0
                # NUMERIC/FLOAT 타입 처리
                elif col in ['hr_unit_artmp', 'hr_unit_rn', 'hr_unit_wspd', 'hr_unit_hum', 'hr_unit_snwfl', 'hr_unit_vsdst', 
                            'gfa', 'bttm_area', 'damg_rgn_lot', 'damg_rgn_lat', 'grnds_dstnc', 'cntr_grnds_dstnc', 'lfdau_grnds_dstnc',
                            'bldg_rscu_dngct', 'bldg_gfa', 'so_area', 'frstn_grnds_dstnc', 'cntr_grnds_dstnc', 'lfdau_grnds_dstnc']:
                    try:
                        if value is not None and str(value).strip() != '':
                            value = float(str(value))
                        else:
                            value = None
                    except (ValueError, TypeError):
                        value = None
                else:
                    # 문자열 처리
                    value = str(value).strip() if value is not None else None
                    if value == 'nan' or value == '':
                        value = None
                
                record[col] = value
            
            records.append(record)
        
        return records
    
    def insert_data_batch(self, table: str, records: List[Dict[str, Any]], batch_size: int = 100):
        """배치 단위로 데이터 삽입"""
        if not records:
            logger.warning(f"No records to insert for table {table}")
            return 0
        
        # 컬럼명 정리
        columns = list(records[0].keys())
        
        # INSERT SQL 생성
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
        """
        
        total_inserted = 0
        cursor = self.conn.cursor()
        
        try:
            # 배치 단위로 처리
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                values = [tuple(record.get(col) for col in columns) for record in batch]
                
                # psycopg3에서는 executemany 사용
                cursor.executemany(sql, values)
                
                inserted_count = cursor.rowcount
                total_inserted += inserted_count
                
                logger.info(f"Inserted {inserted_count} records to {table} (batch {i//batch_size + 1})")
            
            self.conn.commit()
            logger.info(f"Total {total_inserted} records inserted to {table}")
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting data to {table}: {e}")
            raise
        finally:
            cursor.close()
        
        return total_inserted
    
    def load_csv_file(self, file_path: Path, table_info: Dict[str, str]) -> int:
        """CSV 파일 로드 및 삽입"""
        logger.info(f"Loading file: {file_path}")
        
        # 연도 추출
        year = self.extract_year_from_filename(file_path.name, table_info["file_pattern"])
        if year is None:
            logger.warning(f"Could not extract year from filename: {file_path.name}")
            return 0
        
        # CSV 읽기 (인코딩 자동 감지)
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding='cp949')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='euc-kr')
        
        logger.info(f"Loaded {len(df)} rows from {file_path.name} for year {year}")
        
        # 컬럼명 정리
        df = self.clean_column_names(df)
        
        # 데이터 전처리
        records = self.prepare_data_for_table(df, table_info["table"], year)
        
        # 데이터베이스 삽입
        return self.insert_data_batch(table_info["table"], records)
    
    def load_dataset_folder(self, folder_path: Path, table_info: Dict[str, str] = None) -> Dict[str, int]:
        """데이터셋 폴더 로드"""
        folder_name = folder_path.name
        
        if not table_info:
            if folder_name not in self.dataset_mapping:
                logger.warning(f"Unknown dataset folder: {folder_name}")
                return {}
            table_info = self.dataset_mapping[folder_name]
        
        logger.info(f"Processing dataset: {folder_name} -> {table_info['table']}")
        
        results = {}
        csv_files = list(folder_path.glob("*.csv"))
        
        if not csv_files:
            logger.warning(f"No CSV files found in {folder_path}")
            return results
        
        logger.info(f"Found {len(csv_files)} CSV files: {[f.name for f in csv_files]}")
        
        # 파일별 처리
        for csv_file in sorted(csv_files):
            try:
                inserted_count = self.load_csv_file(csv_file, table_info)
                results[csv_file.name] = inserted_count
            except Exception as e:
                logger.error(f"Failed to load {csv_file}: {e}")
                results[csv_file.name] = 0
        
        return results
    
    def load_all_data(self, data_root_path: str) -> Dict[str, Dict[str, int]]:
        """모든 데이터 로드"""
        data_path = Path(data_root_path)
        
        if not data_path.exists():
            raise FileNotFoundError(f"Data path does not exist: {data_root_path}")
        
        logger.info(f"Scanning data path: {data_path}")
        
        # 폴더 목록 확인
        all_folders = [f.name for f in data_path.iterdir() if f.is_dir()]
        logger.info(f"Found folders: {all_folders}")
        logger.info(f"Expected folders: {list(self.dataset_mapping.keys())}")
        
        self.connect_db()
        
        total_results = {}
        
        try:
            # 각 데이터셋 폴더 처리
            for folder in data_path.iterdir():
                if folder.is_dir() and folder.name in self.dataset_mapping:
                    folder_name = folder.name
                    table_info = self.dataset_mapping[folder_name]
                    
                    logger.info(f"\n{'='*50}")
                    logger.info(f"Processing folder: {folder_name}")
                    logger.info(f"Target table: {table_info['table']}")
                    logger.info(f"{'='*50}")
                    
                    folder_results = self.load_dataset_folder(folder, table_info)
                    total_results[folder_name] = folder_results
                    
                    # 폴더별 요약
                    total_records = sum(folder_results.values())
                    logger.info(f"Folder '{folder_name}' completed: {total_records} total records")
                elif folder.is_dir():
                    logger.warning(f"❌ Folder '{folder.name}' not in dataset mapping - skipping")
            
            # 전체 요약
            logger.info(f"\n{'='*50}")
            logger.info("LOADING SUMMARY")
            logger.info(f"{'='*50}")
            
            grand_total = 0
            for folder_name, folder_results in total_results.items():
                folder_total = sum(folder_results.values()) 
                grand_total += folder_total
                logger.info(f"{folder_name}: {folder_total} records")
                
                for file_name, count in folder_results.items():
                    logger.info(f"  - {file_name}: {count} records")
            
            logger.info(f"\nGRAND TOTAL: {grand_total} records loaded")
            
        finally:
            self.disconnect_db()
        
        return total_results

def main():
    """메인 함수"""
    # 데이터베이스 설정
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'fire_safety_db',
        'user': 'suhong', 
        'port': '5432'
    }
    
    # 데이터 경로 (프로젝트 내부 경로)
    DATA_PATH = str(Path(__file__).parent / "data" / "fire_safety_data")
    
    # 데이터 로더 초기화
    loader = FireSafetyDataLoader(DB_CONFIG)
    
    try:
        # 모든 데이터 로드
        results = loader.load_all_data(DATA_PATH)
        
        print("\n🎉 Data loading completed successfully!")
        print(f"Total datasets processed: {len(results)}")
        
    except Exception as e:
        logger.error(f"Data loading failed: {e}")
        print(f"\n❌ Data loading failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())