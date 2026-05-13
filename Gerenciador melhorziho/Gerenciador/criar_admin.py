from projetosenac import app, database, bcrypt
from projetosenac.models import Usuario

with app.app_context():
    NOME     = "Marcy"
    EMAIL    = "marcy@admin.com"
    SENHA    = "polly461"

    if Usuario.query.filter_by(email=EMAIL).first():
        print(f"Já existe um usuário com o email '{EMAIL}'. Nada foi criado.")
    else:
        senha_criptografada = bcrypt.generate_password_hash(SENHA).decode('utf-8')
        admin = Usuario(
            username=NOME,
            email=EMAIL,
            senha=senha_criptografada,
            is_admin=True
        )
        database.session.add(admin)
        database.session.commit()
        print(f"Admin '{NOME}' criado com sucesso!")
        print(f"Email: {EMAIL}")
        print("Pode deletar este arquivo agora.")
