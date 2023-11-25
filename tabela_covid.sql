USE mydb_covid;

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(60) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    confirm_password VARCHAR(60) NOT NULL,
    birth_date VARCHAR(60) NOT NULL,
    gender VARCHAR(60) NOT NULL,
    city VARCHAR(60) NOT NULL,
    state VARCHAR(60) NOT NULL,
    race VARCHAR(60) NOT NULL
);


CREATE TABLE Paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    idade INT,
    sexo VARCHAR(10),
    raca VARCHAR(10),
    escolaridade VARCHAR(20),
    estado VARCHAR(2),
    cidade VARCHAR(255),
    zona VARCHAR(10),
    nosocomial INT, -- ou TINYINT para comportar valores 0 e 1
    dispneia INT, -- ou TINYINT para comportar valores 0 e 1
    cardiopati INT, -- ou TINYINT para comportar valores 0 e 1
    asma INT, -- ou TINYINT para comportar valores 0 e 1
    diabetes INT,
    neurologic INT, -- ou TINYINT para comportar valores 0 e 1
    sintoma_nevoa_mental INT DEFAULT 0,
    sintoma_perda_olfato INT DEFAULT 0,
    sintoma_perda_paladar INT DEFAULT 0,
    sintoma_fadiga INT DEFAULT 0,
    sintoma_dores_cabeca INT DEFAULT 0,
    sintoma_problemas_sono INT DEFAULT 0,
    sintomas_neuromusculares INT DEFAULT 0,
    sintoma_disturbios_emocionais_psicologicos INT DEFAULT 0,
    dose_1 INT, -- ou TINYINT para comportar valores 0 e 1
    dose_2 INT, -- ou TINYINT para comportar valores 0 e 1
    hospitalization INT DEFAULT 0,
    internacao_hospitalar INT, -- ou TINYINT para comportar valores 0 e 1
    internacao_uti INT, -- ou TINYINT para comportar valores 0 e 1
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id)
);


CREATE TABLE ResultadoTeste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    probabilidade FLOAT,
    mensagem VARCHAR(255),
    data_teste DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(id)
);




CREATE TABLE UserProfile (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    username VARCHAR(100),
    age INT,
    -- Adicione outros campos do formulário e resultados aqui
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Teste (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    paciente_id INT NOT NULL,
    nome VARCHAR(255),
    probabilidade FLOAT,
    data_do_teste DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (paciente_id) REFERENCES Paciente(id)
);


CREATE TABLE  password_reset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    token VARCHAR(255),
    expiration_datetime DATETIME
);


CREATE TABLE resultado_teste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    probabilidade FLOAT,
    mensagem VARCHAR(255),
    data_teste DATETIME,
    user_id INT
);


CREATE TABLE probabilidade (
    idcovidLonga INT AUTO_INCREMENT PRIMARY KEY,
    covid VARCHAR(45),
    probabilidade VARCHAR(10)
);