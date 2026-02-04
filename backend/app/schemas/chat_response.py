from pydantic import BaseModel
from typing import Dict, Any

class ChatResponse(BaseModel):
    functionNo: int
    data: Dict[str, Any]