from flask_login import login_required, login_user, logout_user, current_user
from projetosenac import app, database, bcrypt
from flask import render_template, redirect, url_for, flash, request
from projetosenac.forms import FormLogin, FormCriarConta, FormFoto, FormTarefa
from projetosenac.models import Usuario, Foto, Tarefa
import os
from werkzeug.utils import secure_filename


@app.route('/criar-conta', methods=['GET', 'POST'])
@login_required
def criarconta():

    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for('perfil', id_usuario=current_user.id))

    form = FormCriarConta()
    if form.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            senha=senha_cript
        )
        database.session.add(usuario)
        database.session.commit()
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for('feed'))  # admin volta ao feed

    return render_template('criarconta.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
        else:
            flash("Email ou senha inválidos", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/perfil/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):

    if id_usuario != current_user.id:
        flash("Você não tem permissão para acessar esse perfil.", "danger")
        return redirect(url_for('perfil', id_usuario=current_user.id))

    form_foto = FormFoto()
    form_tarefa = FormTarefa() if current_user.is_admin else None

    if request.form.get('form_type') == 'foto' and form_foto.validate_on_submit():
        arquivo = form_foto.foto.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho_projeto = os.path.abspath(os.path.dirname(__file__))
        caminho = os.path.join(caminho_projeto, app.config['UPLOAD_FOLDER'], nome_seguro)
        arquivo.save(caminho)
        foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
        database.session.add(foto)
        database.session.commit()
        flash("Foto enviada com sucesso!", "success")
        return redirect(url_for('perfil', id_usuario=id_usuario))

    if current_user.is_admin and request.form.get('form_type') == 'tarefa' and form_tarefa.validate_on_submit():
        anexo_nome = None
        if form_tarefa.anexo.data:
            arquivo = form_tarefa.anexo.data
            anexo_nome = secure_filename(arquivo.filename)
            caminho_projeto = os.path.abspath(os.path.dirname(__file__))
            caminho = os.path.join(caminho_projeto, app.config['UPLOAD_FOLDER'], anexo_nome)
            arquivo.save(caminho)
        tarefa = Tarefa(
            titulo=form_tarefa.titulo.data,
            descricao=form_tarefa.descricao.data,
            anexo=anexo_nome,
            id_usuario=None  # começa sem atribuição
        )
        database.session.add(tarefa)
        database.session.commit()
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for('perfil', id_usuario=id_usuario))

    # Tarefas atribuídas ao usuário logado
    minhas_tarefas = Tarefa.query.filter_by(id_usuario=current_user.id).all()

    return render_template('perfil.html', usuario=current_user,
                           form=form_foto, form_tarefa=form_tarefa,
                           tarefas=minhas_tarefas)


@app.route('/concluir-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def concluir_tarefa(id_tarefa):
    tarefa = Tarefa.query.get_or_404(id_tarefa)

    # Só o dono da tarefa pode concluir
    if tarefa.id_usuario != current_user.id:
        flash("Ação não permitida.", "danger")
        return redirect(url_for('perfil', id_usuario=current_user.id))

    ids = tarefa.concluida_por.split(',') if tarefa.concluida_por else []
    if str(current_user.id) in ids:
        ids.remove(str(current_user.id))
    else:
        ids.append(str(current_user.id))

    tarefa.concluida_por = ','.join(ids)
    database.session.commit()
    return redirect(url_for('perfil', id_usuario=current_user.id))


@app.route('/atribuir-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def atribuir_tarefa(id_tarefa):
    tarefa = Tarefa.query.get_or_404(id_tarefa)


    tarefa.id_usuario = current_user.id
    database.session.commit()

    flash(f'Tarefa "{tarefa.titulo}" atribuída a você!', "success")
    return redirect(url_for('feed'))


@app.route('/feed')
@login_required
def feed():

    usuarios = Usuario.query.all()
    lista_fotos = []
    for usuario in usuarios:
        if usuario.fotos:
            foto = usuario.fotos[-1]
            imagem = str(foto.imagem)
        else:
            imagem = 'default.png'
        lista_fotos.append({'usuario': usuario, 'imagem': imagem})


    tarefas_disponiveis = Tarefa.query.filter_by(id_usuario=None).all()

    return render_template('feed.html', lista_fotos=lista_fotos,
                           tarefas_disponiveis=tarefas_disponiveis)