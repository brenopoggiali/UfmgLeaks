CREATE TABLE Users (
    id_user INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    encrypted_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Users ("email", "nome", "encrypted_password") VALUES
("foo@bar.tld", "Usuário Teste", "$2b$12$9wVjTgsFGMex73gvCNn.HepYrvrrSTK8hqiNJxOda4NPrrEr4HxIm");
