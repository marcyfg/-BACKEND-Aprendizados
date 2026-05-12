import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Gerenciador.db'
app.config["SECRET_KEY"] = "144b35e7d055a510ab3890fb5be86294"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'fotos_posts')

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from projetosenac import routes
from projetosenac.models import Usuario, Foto