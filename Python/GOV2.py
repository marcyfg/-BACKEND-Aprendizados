import sys

from PySide6.QtWidgets import(
     QApplication,
     QWidget,
     QPushButton,
     QGridLayout,
     QLabel,
     QLineEdit,
)

gov2 = QApplication(sys.argv)

window = QWidget()
window.resize(500, 500)
window.setWindowTitle('Tela de GOV2!!!')

desing = QGridLayout()
window.setLayout(desing)

# ============================================
# BANCO DE DADOS SIMULADO
# ============================================

usuarios = {
    "12345678901": "senha123",
    "98765432100": "abc456",
}

# ============================================
# COMPONENTES
# ============================================

label_user = QLabel("CPF:")
input_user = QLineEdit()
input_user.setPlaceholderText("Somente números sem pontos!!!")

label_password = QLabel("Password:")
input_password = QLineEdit()
input_password.setPlaceholderText("Defina sua senha!!!")

button_registry = QPushButton("Cadastrar")
button_login = QPushButton("Login")

label_result = QLabel("")

# ============================================
# FUNÇÕES DOS BOTÕES
# ============================================

def fazer_login():
    cpf = input_user.text().strip()
    senha = input_password.text().strip()

    # Valida se os campos estão preenchidos
    if not cpf or not senha:
        label_result.setText("⚠️ Linha em branco — preencha todos os campos!")
        return

    # Verifica se o usuário existe
    if cpf not in usuarios:
        label_result.setText("❌ Usuário não encontrado!")
        return

    # Verifica a senha
    if usuarios[cpf] == senha:
        label_result.setText(f"✅ Login realizado com sucesso! Bem-vindo.")
    else:
        label_result.setText("❌ Senha incorreta!")

def cadastrar():
    cpf = input_user.text().strip()
    senha = input_password.text().strip()

    # Valida se os campos estão preenchidos
    if not cpf or not senha:
        label_result.setText("⚠️ Linha em branco — preencha todos os campos!")
        return

    # Verifica se o usuário já existe
    if cpf in usuarios:
        label_result.setText("⚠️ CPF já cadastrado!")
        return

    # Cadastra o novo usuário
    usuarios[cpf] = senha
    label_result.setText(f"✅ Usuário {cpf} cadastrado com sucesso!")

button_login.clicked.connect(fazer_login)
button_registry.clicked.connect(cadastrar)

# ============================================
# LAYOUT
# ============================================

desing.addWidget(label_user, 0, 0)
desing.addWidget(input_user, 1, 0)

desing.addWidget(label_password, 2, 0)
desing.addWidget(input_password, 3, 0)

desing.addWidget(button_login, 4, 0)
desing.addWidget(button_registry, 5, 0)

desing.addWidget(label_result, 6, 0, 1, 1)

window.show()
sys.exit(gov2.exec())