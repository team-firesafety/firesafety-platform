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
    DB_URL: str | None = os.getenv("DB_URL")          # 예) mysql+asyncmy://user:pass@host/db


settings = Settings()

__all__ = ["settings"]
