import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_SERVER = os.getenv("POSTGRES_SERVER", "db")
DB_BASE = os.getenv("POSTGRES_DB", "app")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'secret_KEY1234')