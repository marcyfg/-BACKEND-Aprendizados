from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from projetosenac.models import Usuario


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer Login')


class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=30)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 32)])
    confirmacao_senha = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Confirmar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado. Faça Login para continuar")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'])])
    botao_confirmacao = SubmitField("Enviar foto")


class FormTarefa(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(min=3, max=100)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    anexo = FileField("Anexo (opcional)", validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'pdf', 'webp'])])
    botao_confirmacao = SubmitField("Criar Tarefa")


class FormAtribuirTarefa(FlaskForm):
    """Usado pelo admin para atribuir uma tarefa a um usuário específico."""
    id_usuario = SelectField("Atribuir a", coerce=int, validators=[DataRequired()])
    botao_confirmacao = SubmitField("Atribuir")