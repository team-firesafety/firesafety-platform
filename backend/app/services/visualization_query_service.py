from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from ..models.visualization_models import FireSafetyData
from .visualization_ai_service import VisualizationAIQueryService
from .visualization_metadata_service import VisualizationMetadataService
from .column_mapping_service import ColumnMappingService
import time
import logging
import json
from decimal import Decimal
import datetime

logger = logging.getLogger(__name__)

class VisualizationQueryService:
    """쿼리 실행 및 데이터 처리 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = VisualizationAIQueryService(db)
        self.metadata_service = VisualizationMetadataService(db)
    
    def execute_natural_language_query(self, question: str, 
                                           dataset_type: Optional[str] = None,
                                           limit: int = 100) -> Dict[str, Any]:
        """자연어 질문을 처리하여 결과 반환"""
        start_time = time.time()
        
        try:
            # 1. AI를 통해 SQL 생성
            ai_result = self.ai_service.generate_sql_query(question, dataset_type)
            
            if not ai_result["success"]:
                return {
                    "success": False,
                    "error": ai_result["error"],
                    "generated_sql": None,
                    "data": [],
                    "total_count": 0,
                    "execution_time": time.time() - start_time
                }
            
            generated_sql = ai_result["sql"]
            
            # 2. LIMIT 추가 (이미 있는 경우 제외)
            if "LIMIT" not in generated_sql.upper():
                generated_sql += f" LIMIT {limit}"
            
            # 3. SQL 실행
            data, total_count = self._execute_sql_query(generated_sql)
            
            # 4. 쿼리 설명 생성 (선택적)
            explanation = self.ai_service.explain_query(generated_sql)
            
            execution_time = time.time() - start_time
            
            # 메타데이터 생성
            response_metadata = ColumnMappingService.build_response_metadata(data)
            
            return {
                "success": True,
                "generated_sql": generated_sql,
                "data": data,
                "total_count": total_count,
                "execution_time": execution_time,
                "metadata": {
                    "question": question,
                    "dataset_type": dataset_type,
                    "explanation": explanation,
                    "ai_context": ai_result.get("context_used", "")
                },
                # 차트 생성을 위한 메타데이터 추가
                "columns_metadata": response_metadata["columns_metadata"],
                "chart_recommendations": response_metadata["chart_recommendations"],
                "available_columns": response_metadata["available_columns"]
            }
            
        except Exception as e:
            logger.error(f"Natural language query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "generated_sql": None,
                "data": [],
                "total_count": 0,
                "execution_time": time.time() - start_time
            }
    
    def _execute_sql_query(self, sql: str) -> Tuple[List[Dict[str, Any]], int]:
        """SQL 쿼리 실행"""
        try:
            # 쿼리 실행
            result = self.db.execute(text(sql))
            rows = result.fetchall()
            
            # 결과를 딕셔너리 리스트로 변환
            data = []
            if rows:
                columns = result.keys()
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        # JSON 직렬화 가능한 형태로 변환
                        if isinstance(value, Decimal):
                            # Decimal을 float으로 변환
                            row_dict[col] = float(value)
                        elif isinstance(value, datetime.datetime):
                            # datetime을 ISO 문자열로 변환
                            row_dict[col] = value.isoformat()
                        elif isinstance(value, datetime.date):
                            # date를 ISO 문자열로 변환
                            row_dict[col] = value.isoformat()
                        elif isinstance(value, dict):
                            row_dict[col] = value
                        elif col == 'attributes' and isinstance(value, str):
                            try:
                                row_dict[col] = json.loads(value)
                            except:
                                row_dict[col] = value
                        else:
                            row_dict[col] = value
                    data.append(row_dict)
            
            # 총 개수 계산 (LIMIT 없는 버전으로)
            count_sql = self._generate_count_query(sql)
            count_result = self.db.execute(text(count_sql))
            total_count = count_result.scalar() or len(data)
            
            return data, total_count
            
        except Exception as e:
            logger.error(f"SQL execution failed: {e}")
            raise Exception(f"쿼리 실행 실패: {e}")
    
    def _generate_count_query(self, original_sql: str) -> str:
        """COUNT 쿼리 생성"""
        try:
            # LIMIT 제거
            sql_without_limit = original_sql
            if "LIMIT" in sql_without_limit.upper():
                limit_pos = sql_without_limit.upper().rfind("LIMIT")
                sql_without_limit = sql_without_limit[:limit_pos].strip()
            
            # ORDER BY 제거 (COUNT에는 불필요)
            if "ORDER BY" in sql_without_limit.upper():
                order_pos = sql_without_limit.upper().rfind("ORDER BY")
                sql_without_limit = sql_without_limit[:order_pos].strip()
            
            # SELECT 부분을 COUNT(*)로 변경
            count_sql = f"SELECT COUNT(*) FROM ({sql_without_limit}) as count_subquery"
            
            return count_sql
            
        except Exception as e:
            logger.error(f"Count query generation failed: {e}")
            # 실패시 원본 쿼리의 결과 개수를 사용
            return f"SELECT COUNT(*) FROM fire_safety_data"
    
    def insert_data(self, dataset_type: str, dataset_name: str, 
                         location: Optional[str], data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """데이터 삽입"""
        try:
            inserted_ids = []
            
            for data_item in data_list:
                new_record = FireSafetyData(
                    dataset_type=dataset_type,
                    dataset_name=dataset_name,
                    location=location,
                    attributes=data_item
                )
                
                self.db.add(new_record)
                self.db.flush()  # ID 생성을 위해 flush
                inserted_ids.append(new_record.id)
            
            self.db.commit()
            
            return {
                "success": True,
                "inserted_count": len(inserted_ids),
                "inserted_ids": inserted_ids,
                "message": f"{len(inserted_ids)}개의 레코드가 성공적으로 삽입되었습니다."
            }
            
        except Exception as e:
            logger.error(f"Data insertion failed: {e}")
            self.db.rollback()
            return {
                "success": False,
                "error": str(e),
                "inserted_count": 0,
                "inserted_ids": [],
                "message": "데이터 삽입에 실패했습니다."
            }
    
    def get_data_by_id(self, data_id: int) -> Optional[Dict[str, Any]]:
        """ID로 데이터 조회"""
        try:
            record = self.db.query(FireSafetyData).filter(
                FireSafetyData.id == data_id
            ).first()
            
            if record:
                return {
                    "id": record.id,
                    "dataset_type": record.dataset_type,
                    "dataset_name": record.dataset_name,
                    "location": record.location,
                    "created_at": record.created_at,
                    "updated_at": record.updated_at,
                    "attributes": record.attributes
                }
            return None
            
        except Exception as e:
            logger.error(f"Data retrieval by ID failed: {e}")
            return None
    
    def search_data(self, search_term: str, dataset_type: Optional[str] = None, 
                         limit: int = 100) -> List[Dict[str, Any]]:
        """텍스트 검색"""
        try:
            query = self.db.query(FireSafetyData)
            
            # 데이터셋 타입 필터
            if dataset_type:
                query = query.filter(FireSafetyData.dataset_type == dataset_type)
            
            # JSONB 속성에서 텍스트 검색
            search_filter = func.cast(FireSafetyData.attributes, text("text")).ilike(f"%{search_term}%")
            
            # 또는 dataset_name, location에서도 검색
            query = query.filter(
                search_filter |
                FireSafetyData.dataset_name.ilike(f"%{search_term}%") |
                FireSafetyData.location.ilike(f"%{search_term}%")
            )
            
            results = query.limit(limit).all()
            
            return [
                {
                    "id": record.id,
                    "dataset_type": record.dataset_type,
                    "dataset_name": record.dataset_name,
                    "location": record.location,
                    "created_at": record.created_at,
                    "attributes": record.attributes
                }
                for record in results
            ]
            
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return []
    
    def get_recent_data(self, dataset_type: Optional[str] = None, 
                             limit: int = 50) -> List[Dict[str, Any]]:
        """최근 데이터 조회"""
        try:
            query = self.db.query(FireSafetyData)
            
            if dataset_type:
                query = query.filter(FireSafetyData.dataset_type == dataset_type)
            
            results = query.order_by(FireSafetyData.created_at.desc()).limit(limit).all()
            
            return [
                {
                    "id": record.id,
                    "dataset_type": record.dataset_type,
                    "dataset_name": record.dataset_name,
                    "location": record.location,
                    "created_at": record.created_at,
                    "attributes": record.attributes
                }
                for record in results
            ]
            
        except Exception as e:
            logger.error(f"Recent data retrieval failed: {e}")
            return []