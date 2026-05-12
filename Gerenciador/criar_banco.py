from projetosenac import database, app
from projetosenac.models import Usuario, Foto, Tarefa

with app.app_context():
    database.create_all()