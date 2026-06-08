import mysql.connector

# conexión MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="diagnohealth"
)

# cursor para consultas
cursor = db.cursor(dictionary=True)

print("Base de datos conectada")