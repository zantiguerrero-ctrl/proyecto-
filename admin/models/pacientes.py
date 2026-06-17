from main import db

class Paciente(db.Model):

    __tablename__ = "pacientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    estado = db.Column(db.String(50))