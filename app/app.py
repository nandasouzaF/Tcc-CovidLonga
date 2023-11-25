
from flask import Flask, session, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from email.mime.text import MIMEText
import logging
import secrets



app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234....Rr@localhost/mydb_covid'
app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensões
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"



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







#Definição do modelo User
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    confirm_password = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    state = db.Column(db.String(60), nullable=False)
    race = db.Column(db.String(60), nullable=False)

    #pacientes = db.relationship('Paciente', backref='user_pacientes', lazy=True)
    # Relacionamento com Paciente
    #paciente_user = db.relationship('Paciente', backref='user', overlaps="pacientes,user_pacientes")
    #paciente_user = db.relationship('Paciente', backref='related_user', overlaps="pacientes,user_pacientes")
    related_pacientes = db.relationship('Paciente', backref='related_user', overlaps="paciente_user,related_user")

    
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, new_password):
        self.password =  bcrypt.generate_password_hash(new_password)

    def is_active(self):
        return True
    

    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
            db.session.add(self)
            db.session.commit()



#TABELA NO BANCO PACIENTE-------------------------------------------
class Paciente(db.Model):
    __tablename__ = 'paciente'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(10))
    raca = db.Column(db.String(10))
    escolaridade = db.Column(db.String(20))
    estado = db.Column(db.String(2))
    cidade = db.Column(db.String(255))
    zona = db.Column(db.String(10))
    nosocomial = db.Column(db.Integer)  # Em vez de db.Boolean
    dispneia = db.Column(db.Integer)  # Em vez de db.Boolean
    cardiopati = db.Column(db.Integer)  # Em vez de db.Boolean
    asma = db.Column(db.Boolean)
    diabetes =  db.Column(db.Integer)
    neurologic = db.Column(db.Boolean)
    sintoma_nevoa_mental = db.Column(db.Integer, default=0)
    sintoma_perda_olfato = db.Column(db.Integer, default=0)
    sintoma_perda_paladar = db.Column(db.Integer, default=0)
    sintoma_fadiga =db.Column(db.Integer, default=0)
    sintoma_dores_cabeca = db.Column(db.Integer, default=0)
    sintoma_problemas_sono = db.Column(db.Integer, default=0)
    sintomas_neuromusculares = db.Column(db.Integer, default=0)
    sintoma_disturbios_emocionais_psicologicos = db.Column(db.Integer, default=0)
    dose_1 = db.Column(db.Boolean)
    dose_2 = db.Column(db.Boolean)
    hospitalization = db.Column(db.Integer, default=0)
    internacao_hospitalar = db.Column(db.Boolean)
    internacao_uti = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref='paciente_user')
    # Relacionamento com User
    #user = db.relationship('User', backref='related_pacientes', overlaps="pacientes,user_pacientes")
    user = db.relationship('User', backref='paciente_user', overlaps="paciente_user,related_user")
    
# Consulta à tabela Paciente após a criação
with app.app_context():
    paciente = Paciente.query.first()
    
    
    
    

class Teste(db.Model):
    __tablename__ = 'teste'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    nome = db.Column(db.String(255))
    probabilidade = db.Column(db.Float)
    data_do_teste = db.Column(db.DateTime, default=datetime.utcnow)  # Adicione o campo data_do_teste com o valor padrão de data e hora atuais

    # Defina o relacionamento com a classe Paciente
    paciente = db.relationship('Paciente', backref='testes')

    def __init__(self, user_id, paciente_id, nome, probabilidade, data_do_teste):  # Adicione o argumento data_do_teste
        self.user_id = user_id
        self.paciente_id = paciente_id
        self.nome = nome
        self.probabilidade = probabilidade
        self.data_do_teste = data_do_teste  # Inclua o atributo data_do_teste





# Defina um modelo para a tabela de resultados
class ResultadoTeste(db.Model):
    __tablename__ = 'ResultadoTeste'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    probabilidade = db.Column(db.Float)
    mensagem = db.Column(db.String(255))
    data_teste = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Chave estrangeira

    # Adicione um relacionamento para associar ResultadoTeste a User
    user = db.relationship('User', backref=db.backref('resultados_teste', lazy=True))
# PERFIL:Banco de dados
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(100))
    age = db.Column(db.Integer)
    # Adicione outros campos do formulário e resultados aqui
    

    def __init__(self, user_id, username, age,):
        self.user_id = user_id
        self.username = username
        self.age = age


@app.route('/get_user_info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            # Você encontrou um usuário com o ID especificado
            user_info = {
                'ID': user.id,
                'Nome de Usuário': user.username,
                'E-mail': user.email
                # Adicione outros atributos do usuário que você deseja incluir
            }
            return render_template('user_info.html', user_info=user_info)
        else:
            return "Usuário não encontrado."


#TESTE CONECÇÃO
@app.route('/test_database_connection')
def test_database_connection_view():
    try:
        # Tente fazer uma consulta no banco de dados
        user = User.query.first()
        
        if user:
            # Se um usuário for recuperado com sucesso, exiba suas informações
            return f"Usuário encontrado! Nome: {user.username}, E-mail: {user.email}"
        else:
            return "Nenhum usuário encontrado no banco de dados."
    except Exception as e:
        # Se ocorrer algum erro, exiba uma mensagem de erro
        return f"Erro ao testar a conexão com o banco de dados: {str(e)}"
# Definição do modelo User




    ## ------------------Rota de Login--------------------

#Recuperar o ID do Usuário: Agora, sempre que você precisar do ID do usuário autenticado,
#  você pode acessá-lo via Flask-Login. Aqui está um exemplo de como recuperar o ID do usuário:
def get_user_id():
    if current_user.is_authenticated:
        return current_user.id
    else:
        return None
    


def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                return user
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    conta_criada = request.args.get('conta_criada')
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        # Use a função de autenticação para verificar as credenciais
        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:

                # As credenciais são válidas, o usuário está autenticado com sucesso
                login_user(user)
                return redirect(url_for('perfil'))  # Redireciona para a página de perfil
            else:
                error_message = 'Senha incorreta.'
        else:
            error_message = 'Email não encontrado.'

    return render_template('login.html', conta_criada=conta_criada, error_message=error_message)




# Rota de logout------------------------

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




##------------------------Autenticação Método load_user-------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader

def load_user(user_id):
    # Lógica para carregar um usuário do banco de dados com base no user_id
    return User.query.get(int(user_id))


# Configurar rota estática
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

@app.route('/login', methods=['GET', 'POST'])
@login_required
def login_post():
    if current_user.is_authenticated:
        # Se o usuário já estiver logado, redirecione para a página do perfil
        return redirect(url_for('perfil'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar as credenciais (por exemplo, comparar com o banco de dados)
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Implemente 'check_password' no modelo de usuário
            login_user(user)
            return redirect(url_for('perfil'))  # Redireciona para a página do perfil após o login

    # Renderiza o template de login
    return render_template('login.html')



#autenticação de dois fatores 













#******************************Route******************************
@app.route('/')

@app.route('/home')
def home():
    return render_template('index.html')

#info
# Primeira definição da função info
@app.route('/info')
def info():
    return render_template('info.html')

#info
@app.route('/test_page', methods=['GET', 'POST'])
@login_required
def test_page():
    # Sua lógica para renderizar o formulário aqui
    return render_template('test_page.html')

#TEST
@app.route('/test')
#@login_required
def test_form():
    # Lógica do seu formulário de teste
    return render_template('test.html')



#TEST- FUNÇÃO ------------------------------------------------------------------------------------

def mapear_grupo_idade(idade):
    if idade in [-9, -6, -5, -3, -2, -1, 0, 1, 2, 3, 4, 5]:
        return 'Grupo 0'
    elif idade in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
        return 'Grupo 1'
    elif idade in [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]:
        return 'Grupo 2'
    elif idade in [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]:
        return 'Grupo 3'
    elif idade in [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]:
        return 'Grupo 4'
    elif idade in [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105]:
        return 'Grupo 5'
    




#-----------------------------------------------------------------------------------------------





# Definição da função calcular_probabilidade
def calcular_probabilidade( idade,sexo, raca, escolaridade, estado, cidade, zona,
        comorbidades, internacao_uti,sintomas,grupo_idade):
    probability = 0.0  # Valor inicial da probabilidade

    # Fatores de contribuição igualmente distribuídos
    contribution_per_factor = 100.0 / 12.0  # 14 fatores no total

    # Aumenta a probabilidade com base na idade
    probability += contribution_per_factor


    # Aumenta a probabilidade com base na raça (exemplo: raça negra ou parda)
    if raca in ['branca', 'parda']:
        probability += contribution_per_factor

   # Aumenta a probabilidade para escolaridade 'Fundamental' (valores 1 e 2)
    if escolaridade in ['1', '2']:
        probability += 0.05


    if zona in ['rural']:
        probability += contribution_per_factor
    # Obtenha os sintomas associados à comorbidade NEUROLOGIC
    sintomas_neurologicos = [
        'Nevoa_mental', 'Perda_olfato', 'Perda_paladar',
        'Fadiga', 'Dores_cabeça', 'Problemas_sono',
        'sintomas_neuromusculares', 'Distúrbios_emocionais_psicológicos'
    ]

    # Verifique se pelo menos um dos sintomas NEUROLOGIC está presente
    if any(sintomas.get(sintoma, 0) == 1 for sintoma in sintomas_neurologicos):
        probability += contribution_per_factor


    # Aumenta a probabilidade com base nas comorbidades
    if comorbidades['CARDIOPATI'] == 1:
        probability += contribution_per_factor
    if comorbidades['ASMA'] == 1:
        probability += contribution_per_factor
    if comorbidades['DIABETES'] == 1:
        probability += contribution_per_factor
        
    if comorbidades['NEUROLOGIC'] == 1:
        probability += contribution_per_factor
    
    if comorbidades['DISPNEIA'] == 1:
        probability += contribution_per_factor
    
    if comorbidades['NOSOCOMIAL'] == 1:
        probability += contribution_per_factor

        
        
        
    # Ajuste da probabilidade com base no grupo de idade
    if grupo_idade in ['Grupo 3', 'Grupo 4']:
        probability += 0.1  # Aumenta a probabilidade em 10%

    # Aumenta a probabilidade se o paciente foi internado
    if internacao_uti == 1:
        probability += contribution_per_factor

    # Limita a probabilidade entre 0% e 100%
    probability = max(0.0, min(100.0, probability))

    return probability






# Função para mapear o grupo de idade
def mapear_grupo_idade(idade):
    if idade >= 18 and idade <= 32:
        return 'Grupo de Risco 1'
    elif idade > 32 and idade <= 50:
        return 'Grupo de Risco 2'
    elif idade > 50:
        return 'Grupo de Risco 3'
    else:
        return 'Outro'

@app.route('/test_prob.html', methods=['GET', 'POST'])
@login_required
def test_prob():
    if request.method == 'POST':
        
            #----------
# Lógica para processar os dados do formulário
        nome = request.form['username']
        idade = int(request.form['age'])
        sexo = request.form['gender']
        raca = request.form['race']
        escolaridade = request.form['education']
        estado = request.form['state']
        cidade = request.form['city']
        zona = request.form['zone']
    
        sintomas = {
            'Nevoa_mental': int(request.form.get('Nevoa_mental', 0)),
            'Perda_olfato': int(request.form.get('Perda_olfato', 0)),
            'Perda_paladar': int(request.form.get('Perda_paladar', 0)),
            'Fadiga': int(request.form.get('Fadiga', 0)),
            'Dores_cabeça': int(request.form.get('Dores_cabeça', 0)),
            'Problemas_sono': int(request.form.get('Problemas_sono', 0)),
            'sintomas_neuromusculares': int(request.form.get('sintomas_neuromusculares', 0)),
            'Distúrbios_emocionais_psicológicos': int(request.form.get('Distúrbios_emocionais_psicológicos', 0))
        }
        
        #Verifique se o campo 'hospitalization' está presente nos dados do formulário
        if 'hospitalization' in request.form:
            internacao = int(request.form['hospitalization'])
        else:
            internacao = 0  # Defina internacao como 0 se o campo não estiver presente

            
        comorbidades = {
            'NOSOCOMIAL': int(request.form.get('NOSOCOMIAL', 0)),
            'DISPNEIA': int(request.form.get('DISPNEIA', 0)),
            'CARDIOPATI': int(request.form.get('CARDIOPATI', 0)),
            'ASMA': int(request.form.get('ASMA', 0)),
            'DIABETES': int(request.form.get('DIABETES', 0)),
            'NEUROLOGIC': int(request.form.get('NEUROLOGIC', 0)),
        }
        
        


       # Inicialize a variável probability com um valor padrão
        probability = 0.0  

                
                # Obtenha a idade do formulário
        idade = int(request.form['age'])

        # Mapeie a idade para o grupo correspondente
        grupo_idade = mapear_grupo_idade(idade)

        # Ajuste da probabilidade com base no grupo de idade
        if grupo_idade in ['Grupo 3', 'Grupo 4']:
            probability += 0.1  # Aumenta a probabilidade em 10%
            
            
            
        # Ajuste na probabilidade com base na raça
        if raca in ['1', '4']:  # Verifica se a raça é 'Negra' ou 'Parda'
            probability += 0.05  # Aumenta a probabilidade em 5%

        escolaridade = request.form['education']

        # Aumenta a probabilidade para escolaridade 'Fundamental' (valores 1 e 2)
        if escolaridade in ['1', '2']:
            probability += 0.05  # Aumenta a probabilidade em 5%


        # Se a zona for 'Rural', aumente a probabilidade
        if zona == 'rural':
            probability += 0.05  # Aumenta a probabilidade em 5%





        # Ajuste na probabilidade com base nas comorbidades selecionadas
        if comorbidades['CARDIOPATI'] == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%
        if comorbidades['ASMA'] == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%
        if comorbidades['DIABETES'] == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%
        if comorbidades['NOSOCOMIAL'] == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%
        if comorbidades['NEUROLOGIC'] == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%
        if comorbidades['DISPNEIA'] == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%


            
        # Verifique se o paciente marcou a opção de "Internação na UTI"
        hospitalization = int(request.form.get('UTI', 0))
        
        # Se o paciente marcar a opção de "Internação na UTI", aumente a probabilidade
        if hospitalization == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%





            # Verifique quantos sintomas estão presentes e ajuste a probabilidade
        num_sintomas_presentes = sum(sintomas.values())

        if num_sintomas_presentes > 0:
            # Aumente a probabilidade com base no número de sintomas presentes
            probability += (10 * num_sintomas_presentes)  # Aumenta 10% para cada sintoma presente

        # Faça o cálculo da probabilidade com base nas respostas do paciente
        probability = calcular_probabilidade(idade, sexo, raca, escolaridade, estado, cidade, zona,
        comorbidades,hospitalization,sintomas,grupo_idade)


    # Formate a probabilidade com uma casa decimal e substitua o ponto pela vírgula
        probability_formatted = "{:.1f}%".format(probability).replace(".", ",")


            # Agora, vamos exibir frases com base na probabilidade calculada
        mensagem = ""

        if probability >= 55:
            mensagem = "Você tem uma alta probabilidade de contrair a doença. Consulte um profissional de saúde imediatamente."
        else:
            mensagem = "Sua probabilidade de contrair a doença é relativamente baixa. Continue seguindo as precauções recomendadas."
            
        # Processar os dados do formulário
        nome = request.form['username']
        idade = int(request.form['age'])
        sexo = request.form['gender']
        raca = request.form['race']
        escolaridade = request.form['education']
        estado = request.form['state']
        cidade = request.form['city']
        zona = request.form['zone']

        # Faça o mesmo para os campos de comorbidades
        nosocomial = 'NOSOCOMIAL' in request.form
        dispneia = 'DISPNEIA' in request.form
        cardiopati = 'CARDIOPATI' in request.form
        asma = 'ASMA' in request.form
        diabetes = 'DIABETES' in request.form
        neurologic = 'NEUROLOGIC' in request.form
        
        # Faça o mesmo para os campos de vacinação
        dose_1 = '1_dose' in request.form
        dose_2 = '2_dose' in request.form

       # Verifique se o paciente marcou a opção de "Internação na UTI"
        hospitalization = int(request.form.get('UTI', 0))

        # Se o paciente marcar a opção de "Internação na UTI", aumente a probabilidade
        if hospitalization == 1:
            probability += 0.1  # Aumenta a probabilidade em 10%

 # Verifica se o paciente já existe no banco de dados
        paciente_existente = Paciente.query.filter_by(
            user_id=current_user.id,
            nome=nome,
            idade=idade,
            sexo=sexo,
            raca=raca,
            escolaridade=escolaridade,
            estado=estado,
            cidade=cidade,
            zona=zona,
            nosocomial=comorbidades['NOSOCOMIAL'],
            dispneia=comorbidades['DISPNEIA'],
            cardiopati=comorbidades['CARDIOPATI'],
            asma=comorbidades['ASMA'],
            diabetes=comorbidades['DIABETES'],
            neurologic=comorbidades['NEUROLOGIC'],
            
            hospitalization=internacao
        ).first()

        if paciente_existente:
            teste_existente = Teste.query.filter_by(
                user_id=current_user.id,
                paciente_id=paciente_existente.id,
                probabilidade=probability
            ).first()
            if teste_existente:
                return render_template('test_prob.html', mensagem="Teste já existente para este paciente.")
        
        # Se o paciente não existir ou o teste não existir, crie um novo
        paciente = Paciente(
            user_id=current_user.id,
            nome=nome,
            idade=idade,
            sexo=sexo,
            raca=raca,
            escolaridade=escolaridade,
            estado=estado,
            cidade=cidade,
            zona=zona,
            nosocomial=comorbidades['NOSOCOMIAL'],
            dispneia=comorbidades['DISPNEIA'],
            cardiopati=comorbidades['CARDIOPATI'],
            asma=comorbidades['ASMA'],
            diabetes=comorbidades['DIABETES'],
            neurologic=comorbidades['NEUROLOGIC'],
            hospitalization=internacao,
            sintoma_nevoa_mental=sintomas['Nevoa_mental'],
            sintoma_perda_olfato=sintomas['Perda_olfato'],
            sintoma_perda_paladar=sintomas['Perda_paladar'],
            sintoma_fadiga=sintomas['Fadiga'],
            sintoma_dores_cabeca=sintomas['Dores_cabeça'],
            sintoma_problemas_sono=sintomas['Problemas_sono'],
            sintomas_neuromusculares=sintomas['sintomas_neuromusculares'],
            sintoma_disturbios_emocionais_psicologicos=sintomas['Distúrbios_emocionais_psicológicos']
        )


        db.session.add(paciente)
        db.session.commit()

        # Crie o objeto Teste
        data_do_teste = datetime.now()
        teste = Teste(
            user_id=current_user.id,
            paciente_id=paciente.id,
            nome=nome,
            probabilidade=probability,
            data_do_teste=data_do_teste 
        )

        # Salve o teste no banco de dados
        db.session.add(teste)
        db.session.commit()
    
        # Consulta ao banco de dados para obter o paciente associado a este teste
        paciente = Paciente.query.filter_by(user_id=current_user.id, nome=nome).first()

        # Consulta ao banco de dados para obter os resultados dos testes do usuário
        resultados_testes = Teste.query.filter_by(user_id=current_user.id).all()

       # Após salvar os dados do teste, faça uma consulta ao banco de dados para obter o paciente associado a este teste
        paciente = Paciente.query.filter_by(user_id=current_user.id, nome=nome).first()

        # Após salvar os dados do teste, faça uma consulta ao banco de dados para obter os resultados dos testes do usuário
        resultados_testes = Teste.query.filter_by(user_id=current_user.id).all()


        #Renderize o template e passe form_response como contexto
        return render_template('test_prob.html', probability=probability_formatted, mensagem=mensagem, resultados_testes=resultados_testes)
    else:
        return render_template('test_prob.html', probability="", mensagem="")






## button volta no test_prob.html
@app.route('/voltar', methods=['GET'])
@login_required
def voltar():
    # Lógica para renderizar a página test.html
    return render_template('test.html')



# Routes para mostra o resultados dos teste no Perfil
@app.route('/resultados_testes')
@login_required
def resultados_testes():
    user = current_user  # Obtém o usuário atualmente logado
    # Consulte o banco de dados para recuperar os resultados dos testes associados ao usuário atual
    # Recupere os dados do paciente do banco de dados
    paciente = Paciente.query.filter_by(user_id=current_user.id).first()

    # Consulte o banco de dados para recuperar os resultados dos testes associados ao usuário atual
    resultados = Teste.query.filter_by(user_id=current_user.id).all()
    

    # Renderize o modelo que exibe os resultados dos testes
    return render_template('perfil.html', user=user, resultados_testes=resultados, paciente=paciente)












# Mostra informaçoes do paciente quando clicar em teste!
@app.route('/get_patient_info/<int:patient_id>')
def get_patient_info(patient_id):
    # Consulte o banco de dados para recuperar as informações do paciente com base no ID do paciente
    paciente = Paciente.query.get(patient_id)
    
    if paciente:
        # Convertemos as informações do paciente em um dicionário para retorná-lo como JSON
        paciente_info = {
            'nome': paciente.nome,
            'idade': paciente.idade,
            'sexo': paciente.sexo,
            # Adicione outros campos de informações do paciente conforme necessário
        }
        return jsonify(paciente_info)
    
    return jsonify({'error': 'Paciente não encontrado'}), 404









    #-----------------------------------------------------------------------------------------------
# Gravar informaçoes de teste no perfil:

@app.route('/formulario', methods=['POST'])
def processar_formulario():
    # Lógica para processar os dados do formulário aqui

    # Obtenha os dados do formulário do objeto 'request' e faça o processamento necessário
    nome = request.form['nome']
    idade = int(request.form['idade'])
    # Adicione mais campos do formulário e processamento aqui

    # Assumindo que você tem uma instância do usuário atualmente logado (caso contrário, ajuste esta parte de acordo com a sua lógica de autenticação)
    user = current_user

    # Verifique se o usuário está autenticado (logado)
    if user is not None:
        # Verifique se o usuário já possui um perfil
        user_profile = UserProfile.query.filter_by(user_id=user.id).first()

        if user_profile is None:
            # Se o usuário não possui um perfil, crie um e atribua as informações do formulário
            user_profile = UserProfile(
                user_id=user.id,
                username=nome,
                age=idade,
                # Adicione mais campos do formulário e atribua os valores aqui
            )

            # Adicione o perfil ao banco de dados
            db.session.add(user_profile)
            db.session.commit()
        else:
            # Se o usuário já possui um perfil, atualize as informações do formulário nele
            user_profile.username = nome
            user_profile.age = idade
            # Atualize mais campos do formulário aqui, se necessário

            # Commit as alterações no banco de dados
            db.session.commit()

    # Redirecione para a página de perfil após processar o formulário
    return redirect(url_for('perfil'))



    #perfil
@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    user = current_user  # Obtém o usuário atualmente logado

    paciente = Paciente.query.filter_by(user_id=current_user.id).first()  # Obtém o paciente do banco de dados


    if request.method == 'POST':
        # Obter os dados enviados pelo formulário
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        race = request.form['race']


        # Simule os resultados dos testes (substitua com seus próprios dados)
        resultado_teste_1 = 'Resultado 1'
        resultado_teste_2 = 'Resultado 2'

        # Renderizar o template de perfil e passar os dados para preencher as variáveis
        return render_template('perfil.html', username=username, email=email, password=password,
                            birth_date=birth_date, gender=gender, city=city, state=state, race=race,
                            resultado_teste_1=resultado_teste_1, resultado_teste_2=resultado_teste_2)
    
    # Recupere os dados do paciente do banco de dados
    paciente = Paciente.query.filter_by(user_id=current_user.id).first()
        # Recupere os resultados dos testes do banco de dados para o usuário logado
    resultados_testes = Teste.query.filter_by(user_id=current_user.id).all()

    
    return render_template('perfil.html', user=user, resultados_testes=resultados_testes, paciente=paciente)








#AVATAR
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' in request.files:
        file = request.files['avatar']

        return 'Avatar enviado com sucesso!'
    else:
        return 'Nenhum arquivo de avatar enviado!'



users = {
    'user1': {
        'password_hash': generate_password_hash('password123')
    }
}






#----------------------------------------------
#usuários redefinam
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Verifique se o e-mail existe no banco de dados ou na sua lista de usuários.

        # Se o e-mail existir, envie um e-mail com um link para redefinir a senha.
        # Você pode usar uma biblioteca como Flask-Mail para enviar e-mails.
        # O link deve conter um token seguro que permitirá ao usuário redefinir a senha.

        flash('Verifique seu e-mail para redefinir a senha.', 'success')
        return render_template('login.html')

    return render_template('login.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Verifique se o token é válido e se ainda está dentro do prazo.

    if request.method == 'POST':
        # Obtenha a nova senha do formulário.
        # Atualize a senha do usuário no banco de dados.

        flash('Senha redefinida com sucesso!', 'success')
        return render_template('login.html')

    return render_template('login.html')
# ...




#Recuperação da conta
@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        return 'exists'  # Se o e-mail existir, retorne 'exists'
    else:
        return 'not_exists'  # Se o e-mail não existir, retorne 'not_exists'

@app.route('/recover_account', methods=['POST'])
def recover_account():
    email = request.form.get('email')

    # Verifica se o e-mail existe no banco de dados
    email_exists = request.form.get('email_exists')  # Recebe a resposta da verificação de e-mail

    if email_exists == 'exists':
        # Se o e-mail existir, continue com a lógica para recuperar a conta
        print(f"Solicitada recuperação para o e-mail: {email}")
        # Lógica para enviar e-mail de recuperação aqui
        return 'E-mail de recuperação enviado! Verifique sua caixa de entrada.'
    else:
        return 'E-mail não encontrado no banco de dados. Não foi possível recuperar a conta.'
    
    
    
    
    
    

# PAGINA DE INCRIÇÃO 

# ...

@app.route('/escrever', methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        # Obter os dados do formulário
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        race = request.form['race']

        # Verificar se a senha e a confirmação da senha correspondem
        if password != confirm_password:
            error_message = 'As senhas não correspondem.'
            return render_template('escrever.html', error_message=error_message)

        # Criar uma instância do modelo User com os dados do formulário
        user = User(username=username, email=email, password=password, confirm_password=confirm_password,
                    birth_date=birth_date, gender=gender, city=city, state=state, race=race)

        try:
            # Adicionar o usuário ao banco de dados
            db.session.add(user)
            db.session.commit()

            # Se a conta for criada com sucesso, redirecionar para a página de login com uma mensagem de sucesso
            return redirect(url_for('login', conta_criada=True))
        except IntegrityError:
            # Se ocorrer um erro de integridade (por exemplo, email duplicado), exibir uma mensagem de erro
            error_message = 'O email já está sendo usado. Por favor, use um email diferente.'
            return render_template('escrever.html', error_message=error_message)

    # Se a solicitação for GET, renderizar o formulário de inscrição vazio
    return render_template('escrever.html')

if __name__ == '__main__':
    db.create_all()
    app.config['DEBUG'] = True
    app.run()
