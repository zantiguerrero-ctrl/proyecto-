# importar Flask
from flask import Flask

# importar CORS para permitir conexión con React
from flask_cors import CORS

# importar rutas administrativas
from Routes.admin_routes import admin_routes

# importar rutas privacidad
from Routes.privacy_routes import privacy_routes

# crear aplicación Flask
app = Flask(__name__)
CORS(app)

# registrar blueprint admin
app.register_blueprint(admin_routes)

# registrar blueprint privacidad
app.register_blueprint(privacy_routes)



# ejecutar servidor
if __name__ == "__main__":
    app.run(debug=True)