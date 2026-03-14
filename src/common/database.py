from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.common.config import settings

class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or settings.DATABASE_URL
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
    def create_tables(self):
        self.Base.metadata.create_all(bind=self.engine)
    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
