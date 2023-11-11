from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_BASE, DB_USER, DB_SERVER, DB_PASSWORD

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_BASE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/db/base_class.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
