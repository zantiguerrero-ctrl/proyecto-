import os

class Settings:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "123456789")
    DB_NAME = os.getenv("DB_NAME", "diagnohealth")

    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

settings = Settings()
