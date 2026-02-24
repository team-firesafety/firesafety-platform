from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from ..config import settings
import logging

logger = logging.getLogger(__name__)

# SQLAlchemy 엔진 생성
visualization_engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=False  # SQL 쿼리 로깅
)

# 세션 팩토리 생성
VisualizationSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=visualization_engine)

# 베이스 클래스
VisualizationBase = declarative_base()

def get_visualization_db() -> Session:
    """데이터 시각화용 데이터베이스 세션 의존성"""
    db = VisualizationSessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Visualization database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def get_visualization_db_session() -> Session:
    """데이터 시각화용 데이터베이스 세션 (직접 반환)"""
    return VisualizationSessionLocal()

def create_visualization_tables():
    """데이터 시각화용 모든 테이블 생성"""
    try:
        VisualizationBase.metadata.create_all(bind=visualization_engine)
        logger.info("Visualization database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating visualization tables: {e}")
        raise

def check_visualization_connection():
    """데이터 시각화용 데이터베이스 연결 확인"""
    try:
        with visualization_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Visualization database connection successful")
        return True
    except Exception as e:
        logger.error(f"Visualization database connection failed: {e}")
        return False