from flask_login import login_required, login_user, logout_user, current_user
from projetosenac import app, database, bcrypt
from flask import render_template, redirect, url_for, flash, request
from projetosenac.forms import FormLogin, FormCriarConta, FormFoto, FormTarefa, FormAtribuirTarefa
from projetosenac.models import Usuario, Foto, Tarefa
import os
from werkzeug.utils import secure_filename


# ── helpers ──────────────────────────────────────────────────────────────────

def _salvar_arquivo(arquivo):
    """Salva um arquivo no UPLOAD_FOLDER e retorna o nome seguro."""
    nome_seguro = secure_filename(arquivo.filename)
    caminho_projeto = os.path.abspath(os.path.dirname(__file__))
    caminho = os.path.join(caminho_projeto, app.config['UPLOAD_FOLDER'], nome_seguro)
    arquivo.save(caminho)
    return nome_seguro


# ── autenticação ──────────────────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            # Redireciona usando o token seguro, não o ID numérico
            return redirect(url_for('perfil', token=usuario.token))
        else:
            flash("Email ou senha inválidos", "danger")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


# ── criar conta (somente admin) ───────────────────────────────────────────────

@app.route('/criar-conta', methods=['GET', 'POST'])
@login_required
def criarconta():
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for('perfil', token=current_user.token))

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
        flash(f'Conta de "{usuario.username}" criada com sucesso!', "success")
        return redirect(url_for('feed'))

    return render_template('criarconta.html', form=form)


# ── perfil ────────────────────────────────────────────────────────────────────

@app.route('/perfil/<string:token>', methods=['GET', 'POST'])
@login_required
def perfil(token):
    # Busca o dono do perfil pelo token — 404 se não existir
    dono = Usuario.query.filter_by(token=token).first_or_404()

    # Apenas o próprio usuário ou um admin pode ver o perfil
    if dono.id != current_user.id and not current_user.is_admin:
        flash("Você não tem permissão para acessar esse perfil.", "danger")
        return redirect(url_for('perfil', token=current_user.token))

    form_foto = FormFoto()
    form_tarefa = FormTarefa() if current_user.is_admin else None

    # ── upload de foto ────────────────────────────────────────────────────────
    if request.form.get('form_type') == 'foto' and form_foto.validate_on_submit():
        if not form_foto.foto.data or not form_foto.foto.data.filename:
            flash("Selecione uma foto antes de enviar.", "warning")
            return redirect(url_for('perfil', token=token))
        nome_seguro = _salvar_arquivo(form_foto.foto.data)
        foto = Foto(imagem=nome_seguro, id_usuario=dono.id)
        database.session.add(foto)
        database.session.commit()
        flash("Foto enviada com sucesso!", "success")
        return redirect(url_for('perfil', token=token))

    # ── criar tarefa (admin) ──────────────────────────────────────────────────
    if current_user.is_admin and request.form.get('form_type') == 'tarefa' and form_tarefa.validate_on_submit():
        anexo_nome = None
        if form_tarefa.anexo.data and form_tarefa.anexo.data.filename:
            anexo_nome = _salvar_arquivo(form_tarefa.anexo.data)

        tarefa = Tarefa(
            titulo=form_tarefa.titulo.data,
            descricao=form_tarefa.descricao.data,
            anexo=anexo_nome,
            id_usuario=None  # começa sem atribuição
        )
        database.session.add(tarefa)
        database.session.commit()
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for('perfil', token=token))

    # Tarefas do dono do perfil
    tarefas = Tarefa.query.filter_by(id_usuario=dono.id).all()
    usuarios_todos = Usuario.query.all() if current_user.is_admin else []

    return render_template(
        'perfil.html',
        usuario=dono,
        form=form_foto,
        form_tarefa=form_tarefa,
        tarefas=tarefas,
        usuarios_todos=usuarios_todos,
        eh_admin_vendo=current_user.is_admin and dono.id != current_user.id
    )


# ── concluir tarefa ───────────────────────────────────────────────────────────

@app.route('/concluir-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def concluir_tarefa(id_tarefa):
    tarefa = Tarefa.query.get_or_404(id_tarefa)

    # Só o dono da tarefa (ou admin) pode marcá-la como concluída
    if tarefa.id_usuario != current_user.id and not current_user.is_admin:
        flash("Ação não permitida.", "danger")
        return redirect(url_for('perfil', token=current_user.token))

    ids = tarefa.concluida_por.split(',') if tarefa.concluida_por else []
    alvo_id = str(tarefa.id_usuario)
    if alvo_id in ids:
        ids.remove(alvo_id)
    else:
        ids.append(alvo_id)

    tarefa.concluida_por = ','.join(ids)
    database.session.commit()
    return redirect(request.referrer or url_for('perfil', token=current_user.token))


# ── atribuir tarefa (feed — usuário pega pra si) ──────────────────────────────

@app.route('/atribuir-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def atribuir_tarefa(id_tarefa):
    tarefa = Tarefa.query.get_or_404(id_tarefa)

    if tarefa.id_usuario is not None:
        flash("Essa tarefa já está atribuída.", "warning")
        return redirect(url_for('feed'))

    tarefa.id_usuario = current_user.id
    database.session.commit()
    flash(f'Tarefa "{tarefa.titulo}" atribuída a você!', "success")
    return redirect(url_for('feed'))


# ── admin: atribuir tarefa a qualquer usuário ─────────────────────────────────

@app.route('/admin/atribuir-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def admin_atribuir_tarefa(id_tarefa):
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for('perfil', token=current_user.token))

    tarefa = Tarefa.query.get_or_404(id_tarefa)
    id_destino = request.form.get('id_usuario', type=int)

    if id_destino:
        usuario_destino = Usuario.query.get_or_404(id_destino)
        tarefa.id_usuario = usuario_destino.id
        tarefa.concluida_por = ""  # reseta conclusão ao reatribuir
        database.session.commit()
        flash(f'Tarefa "{tarefa.titulo}" atribuída a {usuario_destino.username}.', "success")
    else:
        flash("Usuário inválido.", "danger")

    return redirect(request.referrer or url_for('feed'))


# ── admin: desatribuir tarefa (volta a ficar disponível no feed) ──────────────

@app.route('/admin/desatribuir-tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def admin_desatribuir_tarefa(id_tarefa):
    if not current_user.is_admin:
        flash("Acesso negado.", "danger")
        return redirect(url_for('perfil', token=current_user.token))

    tarefa = Tarefa.query.get_or_404(id_tarefa)
    tarefa.id_usuario = None
    tarefa.concluida_por = ""
    database.session.commit()
    flash(f'Tarefa "{tarefa.titulo}" desatribuída e disponível no feed.', "success")
    return redirect(request.referrer or url_for('feed'))


# ── feed ──────────────────────────────────────────────────────────────────────

@app.route('/feed')
@login_required
def feed():
    usuarios = Usuario.query.all()
    lista_fotos = []
    for usuario in usuarios:
        imagem = usuario.fotos[-1].imagem if usuario.fotos else 'default.png'
        lista_fotos.append({'usuario': usuario, 'imagem': imagem})

    tarefas_disponiveis = Tarefa.query.filter_by(id_usuario=None).all()

    # Admin vê todas as tarefas atribuídas para poder reatribuir/desatribuir
    todas_tarefas = Tarefa.query.filter(Tarefa.id_usuario.isnot(None)).all() if current_user.is_admin else []

    return render_template(
        'feed.html',
        lista_fotos=lista_fotos,
        tarefas_disponiveis=tarefas_disponiveis,
        todas_tarefas=todas_tarefas,
        usuarios=usuarios  # necessário para o select de atribuição no template
    )