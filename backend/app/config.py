"""
.env 로드 → 환경 변수를 Settings 클래스로 래핑
전역 인스턴스 `settings` 한 개만 생성
사용법:
    from app.config import settings
    db_url = settings.DB_URL
"""

import os
from dotenv import load_dotenv

# .env 파일 읽기 ------------------------------------------------------
load_dotenv()


class Settings:

    # 필수 값 ----------------------------------------------------------
    # PostgreSQL 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost/fire_safety_db")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    VWORLD_KEY = os.getenv("VWORLD_KEY")
    
    # AI 모델 설정(데이터 시각화)
    MAX_QUERY_RESULTS: int = 100

settings = Settings()

__all__ = ["settings"]
