import mysql.connector
from app.core.config import settings

def get_connection():

    connection = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )

    return connection