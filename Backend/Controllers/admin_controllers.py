# importar jsonify para responder JSON
from flask import jsonify, request

# importar conexión MySQL
from Config.db import cursor, db

# ============================
# ESTADÍSTICAS
# ============================

# obtener estadísticas
# GET /admin/estadisticas
def get_estadisticas():

    # contar usuarios
    cursor.execute("SELECT COUNT(*) AS total FROM user")
    total_pacientes = cursor.fetchone()

    # contar tests
    cursor.execute("SELECT COUNT(*) AS total FROM test")
    total_tests = cursor.fetchone()

    # retornar respuesta JSON
    return jsonify({
        "pacientes": total_pacientes["total"],
        "tests": total_tests["total"]
    })

# obtener uso chatbot
# GET /admin/uso-chatbot
def get_uso_chatbot():

    cursor.execute("SELECT COUNT(*) AS total FROM chat_history")
    mensajes = cursor.fetchone()

    return jsonify({
        "mensajes": mensajes["total"],
        "usuarios_activos": 120
    })

# ============================
# FUENTE CONOCIMIENTO
# ============================

# crear fuente
# POST /admin/fuente-conocimiento
def post_fuente():

    data = request.json

    return jsonify({
        "mensaje": "fuente creada",
        "data": data
    })

# eliminar fuente
# DELETE /admin/fuente-conocimiento/:id
def delete_fuente(id):

    return jsonify({
        "mensaje": f"fuente {id} eliminada"
    })

# ============================
# ANALÍTICAS
# ============================

# obtener analíticas
def get_analiticas():

    return jsonify({
        "estado": "analíticas funcionando"
    })

# segmentación
def get_segmentacion():

    return jsonify({
        "segmentos": ["jóvenes", "adultos", "mayores"]
    })

# retención
def get_retencion():

    return jsonify({
        "retencion": "82%"
    })

# abandono
def get_abandono():

    return jsonify({
        "abandono": "18%"
    })

# ============================
# PACIENTES
# ============================

# obtener pacientes
# GET /admin/pacientes
def get_pacientes():

    cursor.execute("""
        SELECT
            id_user,
            name,
            email,
            phone,
            gender
        FROM user
    """)

    patients = cursor.fetchall()

    return jsonify(patients)

# ============================
# RECURSOS
# ============================

# obtener recursos
# GET /admin/recursos
def get_recursos():

    return jsonify({
        "mensaje": "tabla recursos aún no creada"
    })

# crear recurso
# POST /admin/recursos
def post_recurso():

    data = request.json

    return jsonify({
        "mensaje": "recurso creado",
        "data": data
    })

# eliminar recurso
# DELETE /admin/recursos/:id
def delete_recurso(id):

    return jsonify({
        "mensaje": f"recurso {id} eliminado"
    })