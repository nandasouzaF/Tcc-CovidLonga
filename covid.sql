SELECT * FROM mydb_covidLonga.user;
SHOW TABLES;
SELECT * FROM comorbidade;
CREATE TABLE comorbidade (
    id INT PRIMARY KEY AUTO_INCREMENT,
    dispneia VARCHAR(60),
    pneumopatia VARCHAR(60),
    cardiopatia VARCHAR(60),
    down VARCHAR(60),
    asma VARCHAR(60),
    diabetes VARCHAR(60),
    neurologica VARCHAR(60),
    obesidade VARCHAR(60)
);
CREATE TABLE sintomas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    olfato VARCHAR(60),
    paladar VARCHAR(60),
    fadiga VARCHAR(60),
    tosse VARCHAR(60)
);
CREATE TABLE vacinacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    primeira_dose VARCHAR(60),
    segunda_dose VARCHAR(60),
    dose_adicional VARCHAR(60)
);

CREATE TABLE internacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status ENUM('Sim', 'Não'),
    data DATE
);


SELECT * FROM user;
-- Adicionar coluna "zona" na tabela "user"
ALTER TABLE user
ADD COLUMN zona ENUM('1-Urbana', '2-Rural', '3-Periurbana', '9-Ignorado')
AFTER city;

-- Definir restrição CHECK para a coluna "zona"
ALTER TABLE user
ADD CONSTRAINT chk_zona CHECK (zona IN ('1-Urbana', '2-Rural', '3-Periurbana', '9-Ignorado'));


-- Definir restrição CHECK para a coluna "race"
ALTER TABLE user
ADD CONSTRAINT chk_race CHECK (race IN ('1- Branco', '2-Preta', '3-Amarela', '4-Parda', '5-Indígena', '9-Ignorado'));
SELECT DISTINCT race
FROM user
WHERE race NOT IN ('1- Branco', '2-Preta', '3-Amarela', '4-Parda', '5-Indígena', '9-Ignorado');


SELECT * FROM user;

