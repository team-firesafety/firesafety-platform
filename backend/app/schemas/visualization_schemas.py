from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

class VisualizationQueryRequest(BaseModel):
    """데이터 시각화 자연어 쿼리 요청 모델"""
    question: str = Field(..., description="사용자의 자연어 질문", min_length=1)
    dataset_type: Optional[str] = Field(None, description="특정 데이터셋 타입 지정 (자동 추론 가능)")
    limit: Optional[int] = Field(100, description="결과 개수 제한", ge=1, le=1000)
    
    @validator('question')
    def question_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('질문은 비어있을 수 없습니다')
        return v.strip()

class VisualizationDataRecord(BaseModel):
    """데이터 시각화 데이터 레코드 모델"""
    id: int
    dataset_type: str
    dataset_name: str
    location: Optional[str]
    created_at: datetime
    attributes: Dict[str, Any]
    
    class Config:
        from_attributes = True

class VisualizationQueryResponse(BaseModel):
    """데이터 시각화 쿼리 응답 모델"""
    success: bool = True
    generated_sql: str = Field(..., description="생성된 SQL 쿼리")
    data: List[Dict[str, Any]] = Field(..., description="쿼리 실행 결과")
    total_count: int = Field(..., description="총 결과 개수")
    execution_time: float = Field(..., description="쿼리 실행 시간 (초)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="추가 메타데이터")

class VisualizationErrorResponse(BaseModel):
    """데이터 시각화 에러 응답 모델"""
    success: bool = False
    error_code: str = Field(..., description="에러 코드")
    message: str = Field(..., description="에러 메시지")
    details: Optional[Dict[str, Any]] = Field(None, description="에러 상세 정보")

class VisualizationSchemaInfo(BaseModel):
    """데이터 시각화 스키마 정보 모델"""
    dataset_type: str
    description: str
    fields: Dict[str, Any]
    query_examples: List[str]

class VisualizationHealthResponse(BaseModel):
    """데이터 시각화 헬스체크 응답 모델"""
    status: str
    timestamp: datetime
    database_connected: bool
    openai_configured: bool

class VisualizationDataUploadRequest(BaseModel):
    """데이터 시각화 데이터 업로드 요청 모델"""
    dataset_type: str = Field(..., description="데이터셋 타입")
    dataset_name: str = Field(..., description="데이터셋 이름")
    location: Optional[str] = Field(None, description="위치 정보")
    data: List[Dict[str, Any]] = Field(..., description="업로드할 데이터 목록")

class VisualizationDataUploadResponse(BaseModel):
    """데이터 시각화 데이터 업로드 응답 모델"""
    success: bool
    inserted_count: int
    inserted_ids: List[int]
    message: str