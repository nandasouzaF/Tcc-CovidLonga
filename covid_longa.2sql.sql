SELECT * FROM mydb_covidLonga.coviLonga;
ALTER TABLE coviLonga RENAME TO probabilidade;


SHOW TABLES;
CREATE TABLE resultado_teste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    probabilidade FLOAT,
    mensagem VARCHAR(255),
    data_teste DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE paciente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    idade INT NOT NULL,
    sexo VARCHAR(10) NOT NULL,
    gestante VARCHAR(3),
    raca VARCHAR(10) NOT NULL,
    data_sintomas DATE NOT NULL,
    escolaridade VARCHAR(20) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    zona VARCHAR(10) NOT NULL,
    diarreia BOOLEAN,
    perda_olfato BOOLEAN,
    perda_paladar BOOLEAN,
    fadiga BOOLEAN,
    tosse BOOLEAN,
    outro_sintoma BOOLEAN,
    nosocomial BOOLEAN,
    dispneia BOOLEAN,
    pneumopati BOOLEAN,
    cardiopati BOOLEAN,
    sind_down BOOLEAN,
    asma BOOLEAN,
    diabetes BOOLEAN,
    neurologic BOOLEAN,
    renal BOOLEAN,
    obesidade BOOLEAN,
    dose_1 BOOLEAN,
    dose_2 BOOLEAN,
    dose_3 BOOLEAN,
    dose_4 BOOLEAN,
    hospitalization BOOLEAN DEFAULT FALSE,
    internacao_hospitalar BOOLEAN,
    internacao_uti BOOLEAN,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

SELECT * FROM Paciente
SHOW TABLES;

SELECT * FROM mydb_covidLonga.user

CREATE TABLE teste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nome VARCHAR(255),
    probabilidade FLOAT,
    paciente_id INT, -- Adiciona a coluna paciente_id

    FOREIGN KEY (user_id) REFERENCES user(id), -- Chave estrangeira para a tabela user
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) -- Chave estrangeira para a tabela paciente
);

ALTER TABLE teste
ADD data_do_teste DATETIME DEFAULT CURRENT_TIMESTAMP;


#chave estrageira na tabela teste
ALTER TABLE Teste
ADD CONSTRAINT fk_paciente_id
FOREIGN KEY (paciente_id)
REFERENCES Paciente(id);


DELETE FROM Teste WHERE paciente_id IS NULL;

# TABELA PARA REDEFINIR SENHA
CREATE TABLE password_reset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    token VARCHAR(255) NOT NULL,
    expiration_datetime DATETIME NOT NULL
);



ALTER TABLE paciente
DROP COLUMN gestante,
DROP COLUMN data_sintomas,
DROP COLUMN diarreia,
DROP COLUMN perda_olfato,
DROP COLUMN perda_paladar,
DROP COLUMN fadiga,
DROP COLUMN tosse,
DROP COLUMN outro_sintoma,
DROP COLUMN pneumopati,
DROP COLUMN sind_down,
DROP COLUMN renal,
DROP COLUMN obesidade,
DROP COLUMN dose_3,
DROP COLUMN dose_4;




ALTER TABLE paciente
ADD COLUMN sintoma_nevoa_mental INT DEFAULT 0,
ADD COLUMN sintoma_perda_olfato INT DEFAULT 0,
ADD COLUMN sintoma_perda_paladar INT DEFAULT 0,
ADD COLUMN sintoma_fadiga INT DEFAULT 0,
ADD COLUMN sintoma_dores_cabeca INT DEFAULT 0,
ADD COLUMN sintoma_problemas_sono INT DEFAULT 0,
ADD COLUMN sintomas_neuromusculares INT DEFAULT 0,
ADD COLUMN sintoma_disturbios_emocionais_psicologicos INT DEFAULT 0;


SELECT * FROM Paciente;


SHOW COLUMNS FROM paciente;



DROP TABLE Paciente;

