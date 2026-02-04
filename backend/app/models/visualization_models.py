from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.sql import func
from ..core.visualization_database import VisualizationBase

class FireSafetyData(VisualizationBase):
    """소방 안전 데이터 메인 테이블"""
    __tablename__ = "fire_safety_data"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_type = Column(String(100), nullable=False, index=True, 
                         comment="데이터 타입 (fire_equipment, fire_incident 등)")
    dataset_name = Column(String(255), nullable=False,
                         comment="데이터셋 이름")
    location = Column(String(255), nullable=True,
                     comment="위치 정보")
    created_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), onupdate=func.now())
    attributes = Column(JSONB, nullable=False,
                       comment="실제 데이터 저장용 JSON 컬럼")
    search_vector = Column(TSVECTOR, nullable=True,
                          comment="전문 검색용 벡터")
    
    def __repr__(self):
        return f"<FireSafetyData(id={self.id}, type={self.dataset_type}, name={self.dataset_name})>"

class DatasetSchema(VisualizationBase):
    """데이터셋 스키마 메타데이터 테이블"""
    __tablename__ = "dataset_schemas"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_type = Column(String(100), unique=True, nullable=False, index=True,
                         comment="데이터 타입 식별자")
    table_name = Column(String(100), nullable=False,
                       comment="실제 테이블명")
    description = Column(Text, nullable=True,
                        comment="데이터셋 설명")
    data_category = Column(String(50), nullable=True,
                          comment="데이터 카테고리")
    keywords = Column(JSONB, nullable=True,
                     comment="검색 키워드 배열")
    schema_definition = Column(JSONB, nullable=False,
                              comment="필드 정의, 타입, 설명 등")
    query_examples = Column(JSONB, nullable=True,
                           comment="AI를 위한 쿼리 예시")
    sample_queries = Column(JSONB, nullable=True,
                           comment="샘플 SQL 쿼리")
    created_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), 
                       server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<DatasetSchema(id={self.id}, type={self.dataset_type})>"