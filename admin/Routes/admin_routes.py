# importar Blueprint
from flask import Blueprint

# importar todas las funciones del controlador
from Controllers.admin_controllers import *

# crear blueprint
admin_routes = Blueprint("admin_routes", __name__)

# ============================
# ESTADÍSTICAS
# ============================

# obtener estadísticas generales
@admin_routes.route("/admin/estadisticas", methods=["GET"])
def estadisticas():
    return get_estadisticas()

# obtener uso del chatbot
@admin_routes.route("/admin/uso-chatbot", methods=["GET"])
def uso_chatbot():
    return get_uso_chatbot()

# ============================
# FUENTE DE CONOCIMIENTO
# ============================

# crear nueva fuente
@admin_routes.route("/admin/fuente-conocimiento", methods=["POST"])
def crear_fuente():
    return post_fuente()

# eliminar fuente
@admin_routes.route("/admin/fuente-conocimiento/<id>", methods=["DELETE"])
def eliminar_fuente(id):
    return delete_fuente(id)

# ============================
# ANALÍTICAS
# ============================

# obtener analíticas generales
@admin_routes.route("/admin/analiticas", methods=["GET"])
def analiticas():
    return get_analiticas()

# obtener segmentación
@admin_routes.route("/admin/analiticas/segmentacion", methods=["GET"])
def segmentacion():
    return get_segmentacion()

# obtener retención
@admin_routes.route("/admin/analiticas/retencion", methods=["GET"])
def retencion():
    return get_retencion()

# obtener abandono chatbot
@admin_routes.route("/admin/analiticas/abandono-chatbot", methods=["GET"])
def abandono():
    return get_abandono()
# ============================
# PACIENTES
# ============================

# obtener pacientes
@admin_routes.route("/admin/pacientes", methods=["GET"])
def pacientes():
    return get_pacientes()

# ============================
# RECURSOS
# ============================

# obtener recursos
@admin_routes.route("/admin/recursos", methods=["GET"])
def recursos():
    return get_recursos()

# crear recurso
@admin_routes.route("/admin/recursos", methods=["POST"])
def crear_recurso():
    return post_recurso()

# eliminar recurso
@admin_routes.route("/admin/recursos/<id>", methods=["DELETE"])
def eliminar_recurso(id):
    return delete_recurso(id)