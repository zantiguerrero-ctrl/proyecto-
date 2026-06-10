import pymysql

def get_connection():
    print(">>> Intentando conectar a MySQL...")
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="123456789",
            database="diagnohealth",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        print(">>> Conexión exitosa")
        return connection
    except Exception as e:
        print(f">>> ERROR DE CONEXIÓN: {e}")
        raise