# importar Blueprint
from flask import Blueprint

# importar controlador
from Controllers.privacy_controllers import *

# crear blueprint
privacy_routes = Blueprint("privacy_routes", __name__)

# obtener política privacidad
@privacy_routes.route("/privacidad/politica", methods=["GET"])
def politica():
    return get_politica()

# guardar consentimiento
@privacy_routes.route("/privacidad/consentimiento", methods=["POST"])
def consentimiento_post():
    return post_consentimiento()

# obtener consentimiento usuario
@privacy_routes.route("/privacidad/consentimiento/<idUsuario>", methods=["GET"])
def consentimiento_get(idUsuario):
    return get_consentimiento(idUsuario)

# eliminar cuenta
@privacy_routes.route("/privacidad/eliminar-cuenta/<idUsuario>", methods=["DELETE"])
def eliminar_usuario(idUsuario):
    return delete_usuario(idUsuario)

# anonimizar usuario
@privacy_routes.route("/privacidad/anonimizar/<idUsuario>", methods=["POST"])
def anonimizar(idUsuario):
    return anonimizar_usuario(idUsuario)