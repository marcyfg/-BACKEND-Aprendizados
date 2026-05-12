from flask_login import login_required
from projetosenac import app
from flask import render_template, url_for
from projetosenac.forms import FormLogin, FormCriarConta

@app.route('/criar-conta')
def criarconta():
    formcriarconta = FormCriarConta()
    return render_template('criarconta.html', form=formcriarconta)

@app.route('/')
def homepage():
    formlogin = FormLogin()
    return render_template('homepage.html')

@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)



