import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_SERVER = os.getenv("POSTGRES_SERVER", "db")
DB_BASE = os.getenv("POSTGRES_DB", "app")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'secret_KEY1234')


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = 'ru-central1'

SMTP_SERVER=os.getenv("SMTP_SERVER", None)
SMTP_USER=os.getenv("SMTP_USER", None)
SMTP_FROM=os.getenv("SMTP_FROM", None)
SMTP_PASSWORD=os.getenv("SMTP_PASSWORD", None)

SMSTO_TOKEN = os.getenv('SMSTOTOKEN', None)

