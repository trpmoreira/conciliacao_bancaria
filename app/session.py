from sqlalchemy.orm import sessionmaker
from app.db_info import engine_sqlite

SessionLocal = sessionmaker(bind=engine_sqlite)

def get_session():
    return SessionLocal()
