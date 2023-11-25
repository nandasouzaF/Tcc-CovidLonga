SELECT * FROM mydb_covidLonga.paciente;


#Para verificar no SQL que um teste foi vinculado a um usuário específico
SELECT * FROM Paciente WHERE user_id = '14';

SELECT * FROM teste WHERE user_id = '14';


# Para ver os usuarios logados
SELECT * FROM mydb_covidLonga.user


