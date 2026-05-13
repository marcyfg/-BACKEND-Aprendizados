import secrets
from projetosenac import app, database
from projetosenac.models import Usuario
from sqlalchemy import text

with app.app_context():
    with database.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE usuario ADD COLUMN token VARCHAR(64)"))
            conn.commit()
            print("Coluna 'token' adicionada.")
        except Exception:
            print("Coluna 'token' já existe, pulando ALTER TABLE.")

    usuarios_sem_token = Usuario.query.filter(
        (Usuario.token == None) | (Usuario.token == '')
    ).all()

    for u in usuarios_sem_token:
        u.token = secrets.token_urlsafe(32)

    database.session.commit()
    print(f"{len(usuarios_sem_token)} usuário(s) receberam tokens.")
    print("Migração concluída!")
