import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_SERVER = os.getenv("POSTGRES_SERVER", "db")
DB_BASE = os.getenv("POSTGRES_DB", "app")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'secret_KEY1234')

print(DB_USER, DB_PASSWORD, DB_SERVER, DB_BASE)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = 'ru-central1'

UNIPAY_SECRET = os.getenv("UNIPAY_SECRET", None)
UNIPAY_MERCH_ID = os.getenv("UNIPAY_MERCH_ID", None)
