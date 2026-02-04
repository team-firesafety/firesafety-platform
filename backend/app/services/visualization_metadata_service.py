from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.visualization_models import DatasetSchema
import json
import logging

logger = logging.getLogger(__name__)

class VisualizationMetadataService:
    """데이터셋 메타데이터 관리 서비스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_schemas(self) -> Dict[str, Any]:
        """모든 데이터셋 스키마 정보 조회"""
        try:
            schemas = self.db.query(DatasetSchema).all()
            result = {}
            
            for schema in schemas:
                result[schema.dataset_type] = {
                    "description": schema.description,
                    "schema_definition": schema.schema_definition,
                    "query_examples": schema.query_examples or []
                }
            
            return result
        except Exception as e:
            logger.error(f"Error getting all schemas: {e}")
            return {}
    
    def get_schema_by_type(self, dataset_type: str) -> Optional[Dict[str, Any]]:
        """특정 데이터셋 타입의 스키마 정보 조회"""
        try:
            schema = self.db.query(DatasetSchema).filter(
                DatasetSchema.dataset_type == dataset_type
            ).first()
            
            if schema:
                return {
                    "dataset_type": schema.dataset_type,
                    "description": schema.description,
                    "schema_definition": schema.schema_definition,
                    "query_examples": schema.query_examples or []
                }
            return None
        except Exception as e:
            logger.error(f"Error getting schema for type {dataset_type}: {e}")
            return None
    
    def get_available_dataset_types(self) -> List[str]:
        """사용 가능한 데이터셋 타입 목록 조회"""
        try:
            result = self.db.query(DatasetSchema.dataset_type).all()
            return [row[0] for row in result]
        except Exception as e:
            logger.error(f"Error getting dataset types: {e}")
            return []
    
    def get_query_examples(self, dataset_type: Optional[str] = None) -> List[str]:
        """쿼리 예시 조회"""
        try:
            if dataset_type:
                schema = self.get_schema_by_type(dataset_type)
                return schema.get("query_examples", []) if schema else []
            else:
                schemas = self.get_all_schemas()
                examples = []
                for schema_info in schemas.values():
                    examples.extend(schema_info.get("query_examples", []))
                return examples
        except Exception as e:
            logger.error(f"Error getting query examples: {e}")
            return []
    
    def build_context_for_ai(self, dataset_type: Optional[str] = None) -> str:
        """AI를 위한 컨텍스트 문자열 생성"""
        try:
            if dataset_type:
                schema_info = self.db.query(DatasetSchema).filter(
                    DatasetSchema.dataset_type == dataset_type
                ).first()
                
                if not schema_info:
                    return f"데이터셋 타입 '{dataset_type}'을 찾을 수 없습니다."
                
                context = f"""
데이터셋 타입: {schema_info.dataset_type}
설명: {schema_info.description}

스키마 정의:
{json.dumps(schema_info.schema_definition, ensure_ascii=False, indent=2)}

쿼리 예시:
{chr(10).join(schema_info.query_examples or [])}
"""
            else:
                schemas = self.db.query(DatasetSchema).all()
                context_parts = []
                
                for schema in schemas:
                    context_parts.append(f"""
데이터셋 타입: {schema.dataset_type}
설명: {schema.description}
스키마: {json.dumps(schema.schema_definition, ensure_ascii=False)}
예시: {'; '.join(schema.query_examples or [])}
""")
                
                context = "\n".join(context_parts)
            
            return context.strip()
        
        except Exception as e:
            logger.error(f"Error building AI context: {e}")
            return "메타데이터를 불러오는데 실패했습니다."
    
    def update_schema(self, dataset_type: str, schema_definition: Dict[str, Any], 
                           query_examples: List[str], description: str) -> bool:
        """스키마 정보 업데이트"""
        try:
            schema = self.db.query(DatasetSchema).filter(
                DatasetSchema.dataset_type == dataset_type
            ).first()
            
            if schema:
                schema.schema_definition = schema_definition
                schema.query_examples = query_examples
                schema.description = description
            else:
                schema = DatasetSchema(
                    dataset_type=dataset_type,
                    schema_definition=schema_definition,
                    query_examples=query_examples,
                    description=description
                )
                self.db.add(schema)
            
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating schema: {e}")
            self.db.rollback()
            return False
    
    def get_data_statistics(self) -> Dict[str, Any]:
        """데이터 통계 조회"""
        try:
            query = text("""
                SELECT 
                    dataset_type,
                    COUNT(*) as count,
                    MIN(created_at) as first_created,
                    MAX(created_at) as last_created
                FROM fire_safety_data 
                GROUP BY dataset_type
                ORDER BY count DESC
            """)
            
            result = self.db.execute(query).fetchall()
            
            statistics = {
                "total_records": sum(row[1] for row in result),
                "dataset_types": {
                    row[0]: {
                        "count": row[1],
                        "first_created": row[2],
                        "last_created": row[3]
                    } for row in result
                }
            }
            
            return statistics
        except Exception as e:
            logger.error(f"Error getting data statistics: {e}")
            return {"total_records": 0, "dataset_types": {}}