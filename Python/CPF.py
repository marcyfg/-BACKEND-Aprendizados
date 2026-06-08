# Importando o módulo sys (usado para controlar a execução do programa)
import sys

# Importando apenas os componentes que estamos utilizando
from PySide6.QtWidgets import(
     QApplication,   # Controla toda a aplicação
     QWidget,        # Janela simples (base da interface)
     QPushButton,    # Botão Clicáveis
     QGridLayout,    # Layout em formado de grade (linhas e colunas)
     QLabel,         # Exibe textos na tela
     QLineEdit,      # Campo de entrada de texto
)

# ============================================
# "BANCO DE DADOS" (DICIONÁRIO)
# ============================================

# Um dicionário que simula um banco de dados
# Estrutura
# e-mail --> {nome, sobrenome, idade, e-mail, telefone}
usuario = {}

def salvar_usuario():
    # Lê os dados digitados
    nome = input_nome.text()
    sobrenome = input_sobrenome.text()
    idade = input_idade.text()
    email = input_email.text()
    telefone = input_telefone.text()

    # ============================================
    # VALIDAÇÃO DOS DADOS
    # ============================================

    # Verifica se algum campo está vazio
    if nome == "" or sobrenome == "" or idade == "" or email == "" or telefone == "":
      label_resultado.setText("Preencha todos os campos!!!")
      return

    # Verifica se a idade contém apenas números
    if not idade.isdigit():
       label_resultado.setText("Idade deve ser numérica!!!")
       return
    
    # Verifica simples de email
    if "@" not in email:
       label_resultado.setText("E-mail Inválido!!!")
       return
    
    # Verifica se o telefone contém apenas números
    if not telefone.isdigit():
       label_resultado.setText("Telefone deve ser numérico!!!")
       return

    # Verifica o tamanho do telefone
    if len(telefone) != 10 and len(telefone) != 11:
       label_resultado.setText("Telefone inválido,  use ddd + número!!!")
       return
    
    # ============================================
    # CRIA O REGISTRO DO USUÁRIO
    # ============================================
    usuario = {
       "nome": nome,
       "sobrenome": sobrenome,
       "idade": int(idade),
       "email": email,
       "telefone": telefone
    }

    # Feedback para o cadastro na tela
    label_resultado.setText("Usuário Cadastrado com SUCESSO!!!")

    # Apresenta o conteúdo no terminal
    print(usuario)

    # ============================================
    # LIMPA OS CAMPOS DA TELA
    # ============================================
    input_nome.clear()
    input_sobrenome.clear()
    input_idade.clear()
    input_email.clear()
    input_telefone.clear()

# ============================================
# CRIA A APLICAÇÃO
# ============================================

# QApplication é responsável por iniciar a gerenciar o programa
app = QApplication(sys.argv)

# ============================================
# CRIA A JANELA PRINCIPAL
# ============================================

# QWidget será nossa janela (forma mais simples de interface)
janela = QWidget()

# Define o tamanho da janela
janela.resize(600, 300)

# Define o título da janela
janela.setWindowTitle('Casdastro de usuarios')

# ============================================
# CRIA O LAYOUT
# ============================================
# QGridLayout organiza os elementos em linhas x colunas

layout = QGridLayout()
janela.setLayout(layout)

# ============================================
# COMPONENTES DA INTERFACE
# ============================================

# Campo nome
label_nome = QLabel("Nome:")
input_nome = QLineEdit()
input_nome.setPlaceholderText("Ex: Paulo, Henrique, Maria")

# Campo sobrenome
label_sobrenome = QLabel("Sobrenome:")
input_sobrenome = QLineEdit()
input_sobrenome.setPlaceholderText("Ex: Silva, Pereira, Gomes Oliveira")

# Campo idade
label_idade = QLabel("Idade:")
input_idade = QLineEdit()
input_idade.setPlaceholderText("Ex: 40, 50, 18")

# Campo e-mail
label_email = QLabel("E-mail:")
input_email = QLineEdit()
input_email.setPlaceholderText("Ex: neunome@suaempresa.com")

# Campo Telefone
label_telefone = QLabel("Telefone:")
input_telefone = QLineEdit()
input_telefone.setPlaceholderText("Ex: 11972951008")

# botão de salvar o cadastro
botao_salvar = QPushButton("Salvar")

# Label para mensagens ao usuário
label_resultado = QLabel("")

# ============================================
# ADICIONAR OS COMPONTES AO LAYOUT
# ============================================

layout.addWidget(label_nome, 0, 0)
layout.addWidget(input_nome, 0, 1)

layout.addWidget(label_sobrenome, 1, 0)
layout.addWidget(input_sobrenome, 1, 1)

layout.addWidget(label_idade, 2, 0)
layout.addWidget(input_idade, 2, 1)

layout.addWidget(label_email, 3, 0)
layout.addWidget(input_email, 3, 1)

layout.addWidget(label_telefone, 4, 0)
layout.addWidget(input_telefone, 4, 1)

layout.addWidget(botao_salvar, 5, 0, 1, 2)
layout.addWidget(label_resultado, 6, 0, 1, 2)

# ============================================
# EVENTO
# ============================================

# Quando o botão for clicadom a função salvar usuário
# dever ser executada
botao_salvar.clicked.connect(salvar_usuario)

# ============================================
# EXECUTA O PROGRAMA
# ============================================

# Exibe a janela na tela
janela.show()

# Mantém o programa rodando até o usuário fechar
sys.exit(app.exec())