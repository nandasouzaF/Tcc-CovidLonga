from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import UserMixin, LoginManager
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

db = SQLAlchemy()

bcrypt = Bcrypt(app)
# banco de dado

app.config['SECRET_KEY'] = 'your_secret_key'
#toolbar = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234....Rr@localhost/mydb_covidLonga'
db = SQLAlchemy(app)
# Configuração do Flask Debug Toolbar
app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


#Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Configurar a rota de login. Esta será a rota para onde o usuário é redirecionado ao fazer logout.
login_manager.login_view = "login"  # Substitua "login" pela rota de login do seu aplicativo.
login_manager = LoginManager(app)


# TESTANDO O BANCO DE DADO
try:
    with app.app_context():
        result = db.session.execute(text('SELECT 1')).fetchone()
        if result[0] == 1:
            print("Conexão com o banco de dados bem-sucedida.")
        else:
            print("Falha na conexão com o banco de dados.")
except Exception as e:
    print("Erro durante a conexão com o banco de dados:", str(e))

