from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., description="사용자 입력 문장")