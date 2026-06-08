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

def somar():
    try:
        # Pega o texto digitado e converte para o número
        n1 = float(num1.text())
        n2 = float(num2.text())

        # realiza a operacao
        calc = n1 + n2
        resultado.setText(f"Resultado: {calc}")
    except:
        resultado.setText("ERRO!!! Digite somente números.")

def subtrair():
    try:
        # Pega o texto digitado e converte para o número
        n1 = float(num1.text())
        n2 = float(num2.text())

        # realiza a operacao
        calc = n1 - n2
        resultado.setText(f"Resultado: {calc}")
    except:
        resultado.setText("ERRO!!! Digite somente números.")

def multiplicar():
    try:
        # Pega o texto digitado e converte para o número
        n1 = float(num1.text())
        n2 = float(num2.text())

        # realiza a operacao
        calc = n1 * n2
        resultado.setText(f"Resultado: {calc}")
    except:
        resultado.setText("ERRO!!! Digite somente números.")

def divisao():
    try:
        # Pega o texto digitado e converte para o número
        n1 = float(num1.text())
        n2 = float(num2.text())

        # realiza a operacao
        if n2 == 0:
            resultado.setText("Erro: divisão por zero não existe")
        else:
            calc = n1 / n2
            resultado.setText(f"Resultado: {calc}")
    except:
        resultado.setText("ERRO!!! Digite somente números.")

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

# Define o título da janela
janela.setWindowTitle('Calculadora Simples')

# ============================================
# CRIA LAYOUT
# ============================================

# QGridLayout organiza os elementos em linhas e colunas (tipo tabela)
layout = QGridLayout()

# ============================================
# CRIA CAMPOS DE ENTRADA
# ============================================

# QLineEdit para usar para o primeiro e segundo número
# Aqui vai ser lido ambos os números
num1 = QLineEdit()
num2 = QLineEdit()

num1.setPlaceholderText('Número 1')
num2.setPlaceholderText('Número 2')

# ============================================
# CRIA LABEL RESULTADO
# ============================================

# QLabel serve para mostrar informações na tela
# Aqui será usado para exibir o resultado
resultado = QLabel('Resultado: ')

# ============================================
# CRIA BOTÕES
# ============================================

# Cria um notão com o texto "CALCULE"
botao_somar = QPushButton('+')
botao_subtrair = QPushButton('-')
botao_multiplicar = QPushButton('*')
botao_dividir = QPushButton('/')

# Conectando os eventos
botao_somar.clicked.connect(somar)
botao_subtrair.clicked.connect(subtrair)
botao_multiplicar.clicked.connect(multiplicar)
botao_dividir.clicked.connect(divisao)

# ============================================
# ADICIONAR ELEMENTOS
# ============================================
# Adiciona os campos na linha 0
layout.addWidget(num1, 0, 0)
layout.addWidget(num2, 0, 1)

# Adiciona o botão na linha 1
layout.addWidget(botao_somar, 1, 0)
layout.addWidget(botao_subtrair, 1, 1)
layout.addWidget(botao_multiplicar, 2, 0)
layout.addWidget(botao_dividir, 2, 1)

# Adiciona o resultado na linha 2
layout.addWidget(resultado, 3, 0, 2, 2)

# ============================================
# APLICA O LAYOUT NA JANELA
# ============================================

# Defino que a janela vai usar o layout que criamos
janela.setLayout(layout)

# ============================================
# EXECUTA O PROGRAMA
# ============================================

# Exibe a janela na tela
janela.show()

# Mantém o programa rodando até o usuário fechar
sys.exit(app.exec())
 