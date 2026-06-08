# Importando o módulo sys (usado para controlar a execução do programa)
import sys

# Biblioteca para trabalhar com banco SQLite
import sqlite3

# Importando apenas os componentes que estamos utilizando
from PySide6.QtWidgets import(
     QApplication,      # Controla toda a aplicação
     QWidget,           # Janela simples (base da interface)
     QPushButton,       # Botão Clicáveis
     QGridLayout,       # Layout em formado de grade (linhas e colunas)
     QVBoxLayout,       # Layout em pilhas verticais
     QLabel,            # Exibe textos na tela
     QLineEdit,         # Campo de entrada de texto
     QTableWidget,      # Tabela para exibir dados
     QTableWidgetItem   # Itens (valores) dentro da tabela
)

# ============================================
# CONEXÃO COM BANDO DE DADOS (SQLITE)
# ============================================

# cria ou abrir o BD
conexao = sqlite3.connect("cadastro.db")

cursor = conexao.cursor()

# ============================================
# CRIANDO A TABELA USUARIOS
# ============================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (   
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   nome TEXT NOT NULL,
   sobrenome TEXT NOT NULL,
   idade INTEGER NOT NULL,
   email TEXT UNIQUE NOT NULL,
   telefone TEXT NOT NULL  
   )
""")

# salva estrutura no banco
conexao.commit()

# Atualização da tabela com os dados do dicinário
def atualizar_tabela():
   
   # Remove todas as linhas existentes
   tabela.setRowCount(0)
   
   # ====================================
   # CONSULTA AO BANCO (SELECT)
   # ====================================

   cursor.execute ("""SELECT nome, sobrenome, idade, email, telefone FROM usuarios""")

   dados = cursor.fetchall()
  
   # Percorre o "Banco de Dados"
   for linha, usuario in enumerate(dados):
      
      # insere nova linha na tabela
      tabela.insertRow(linha)

      # preenche cada coluna da linha
      tabela.setItem(linha, 0, QTableWidgetItem(usuario[0]))
      tabela.setItem(linha, 1, QTableWidgetItem(usuario[1]))
      tabela.setItem(linha, 2, QTableWidgetItem(str(usuario[2])))
      tabela.setItem(linha, 3, QTableWidgetItem(usuario[3]))
      tabela.setItem(linha, 4, QTableWidgetItem(usuario[4]))

      # Avança para a próxima linha
      linha += 1

def editar_usuario():

   # usa o e-mail como chave
   email = input_email.text()

   if email == "":
      label_resultado.setText("O campo e-mail não pode ser nulo ou vazio!!!")
      return
   
   # Atualizar o BD
   cursor.execute("""
                  UPDATE usuarios 
                  SET nome = ?, sobrenome = ?, idade = ?, telefone = ? 
                  WHERE email = ?
                  """,(
                     input_nome.text(),
                     input_sobrenome.text(),
                     int(input_idade.text()),
                     input_telefone.text(),
                     email
                  ))
   conexao.commit()

   label_resultado.setText("Alteração realizada com sucesso!!!")

   atualizar_tabela()

def excluir_usuario():

   # usa o e-mail como chave
   email = input_email.text()

   if email == "":
      label_resultado.setText("O campo e-mail não pode ser nulo ou vazio!!!")
      return
   
   # remove registro do BD
   cursor.execute("DELETE FROM usuarios WHERE email = ?", [email])

   conexao.commit()

   label_resultado.setText("Usuário excluído com sucesso!!!")

   atualizar_tabela()

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
    
    # VERIFICA SE E-MAIL JÁ EXISTE NO BD

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,)) 
    
    usuario_existe = cursor.fetchone()

    # Verifica simples de email
    if usuario_existe:
       label_resultado.setText("E-mail já casdastrado!!!")
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
    # CRIA O REGISTRO DO USUÁRIO INSERT
    # ============================================
    
    cursor.execute("""
      INSERT INTO usuarios (nome, sobrenome, idade, email, telefone)
      values (?, ?, ?, ?, ?)""", (nome, sobrenome, int(idade), email, telefone))
    
    # confirma a operação
    conexao.commit()

    # Feedback para o cadastro na tela
    label_resultado.setText("Usuário Cadastrado com SUCESSO!!!")

    # ============================================
    # ATUALIZA A TABELA
    # ============================================

    atualizar_tabela()

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
janela.setWindowTitle('Cadastro de Usuarios')

# ============================================
# CRIA O LAYOUT
# ============================================
# QGridLayout organiza os elementos em linhas x colunas

layout_principal = QVBoxLayout()
layout_formulario = QGridLayout()
janela.setLayout(layout_principal)

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
botao_salvar = QPushButton("Salvar")      # CREATE
botao_editar = QPushButton("Editar")      # UPDATE
botao_excluir = QPushButton("Excluir")    # DELETE

# Label para mensagens ao usuário
label_resultado = QLabel("")

# ============================================
# TABELA DE DADOS
# ============================================

# Define a variável
tabela = QTableWidget()

# Define o número de colunas
tabela.setColumnCount(5)

# Define nomes das colunas
tabela.setHorizontalHeaderLabels(
   ["Nome", "Sobrenome", "Idade", "E-mail", "Telefone"]
)

# ============================================
# ADICIONAR OS COMPONTES AO LAYOUT
# ============================================

layout_formulario.addWidget(label_nome, 0, 0)
layout_formulario.addWidget(input_nome, 0, 1)

layout_formulario.addWidget(label_sobrenome, 1, 0)
layout_formulario.addWidget(input_sobrenome, 1, 1)

layout_formulario.addWidget(label_idade, 2, 0)
layout_formulario.addWidget(input_idade, 2, 1)

layout_formulario.addWidget(label_email, 3, 0)
layout_formulario.addWidget(input_email, 3, 1)

layout_formulario.addWidget(label_telefone, 4, 0)
layout_formulario.addWidget(input_telefone, 4, 1)


# ============================================
# ADICIONANDO COMPONENTES AO LAYOUT PRINCIPAL
# ============================================

layout_principal.addLayout(layout_formulario)
layout_principal.addWidget(botao_salvar)
layout_principal.addWidget(botao_editar)
layout_principal.addWidget(botao_excluir)
layout_principal.addWidget(label_resultado)
layout_principal.addWidget(tabela)

# ============================================
# EVENTO
# ============================================

# Quando o botão for clicadom a função salvar usuário
# dever ser executada
botao_salvar.clicked.connect(salvar_usuario)
botao_editar.clicked.connect(editar_usuario)
botao_excluir.clicked.connect(excluir_usuario)

# ============================================
# EXECUTA O PROGRAMA
# ============================================

# Carrega os dados os programa ao abrir
atualizar_tabela()

# Exibe a janela na tela
janela.show()

# Mantém o programa rodando até o usuário fechar
sys.exit(app.exec())