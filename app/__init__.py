
from flask import Flask
from .models import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do aplicativo
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234....Rr@localhost/mydb_covidLonga'

# Outras configurações do aplicativo


# Defina outros objetos, como o banco de dados (db), aqui

def create_app():
    # Coloque qualquer inicialização adicional aqui, se necessário
    return app
