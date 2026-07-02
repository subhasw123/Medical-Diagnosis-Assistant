import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)
class Config:
    MYSQL_HOST = os.getenv("DB_HOST", "localhost")
    MYSQL_PORT = os.getenv("DB_PORT", 3306)
    MYSQL_USER = os.getenv("DB_USER", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "Subha@123")
    MYSQL_DATABASE = os.getenv("DB_NAME", "medical_assistant")