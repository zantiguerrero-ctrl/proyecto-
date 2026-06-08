# importar jsonify
from flask import jsonify, request


# obtener política
def get_politica():
    return jsonify({
        "politica": "Política de privacidad del sistema"
    })

# guardar consentimiento
def post_consentimiento():
    # obtener datos
    data = request.json

    return jsonify({
        "mensaje": "consentimiento guardado", "data": data
    })

# obtener consentimiento usuario
def get_consentimiento(idUsuario):
    return jsonify({
        "usuario": idUsuario,
        "consentimiento": True
    })

# eliminar usuario
def delete_usuario(idUsuario):
    return jsonify({
        "mensaje": f"usuario {idUsuario} eliminado"
    })
    
# anonimizar usuario
def anonimizar_usuario(idUsuario):
    return jsonify({
        "mensaje": f"usuario {idUsuario} anonimizado"
    })