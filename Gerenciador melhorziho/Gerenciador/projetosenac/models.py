from projetosenac import app, database, login_manager
from datetime import datetime
from flask_login import UserMixin
import secrets

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    is_admin = database.Column(database.Boolean, default=False)
    token = database.Column(database.String(64), unique=True, nullable=False,
                            default=lambda: secrets.token_urlsafe(32))
    fotos = database.relationship("Foto", backref="usuario", lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)

class Tarefa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=True)
    anexo = database.Column(database.String, nullable=True)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    concluida_por = database.Column(database.String, default="")
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=True)
    usuario = database.relationship("Usuario", backref="tarefas")