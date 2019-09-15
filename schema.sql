CREATE TABLE Users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    encrypted_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Arquivo (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_contribuinte INTEGER NOT NULL,
    nome VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL UNIQUE,
    id_disciplina INTEGER NOT NULL,
    tipo VARCHAR(255) NOT NULL,
    professor VARCHAR(255),
    FOREIGN KEY (id_contribuinte) REFERENCES Users,
    FOREIGN KEY (id_disciplina) REFERENCES Disciplina
);

CREATE TABLE Departamento (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE Disciplina (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    id_departamento INTEGER NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES Departamento

);

CREATE TABLE Curso (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE Curso_Disciplina (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_curso VARCHAR(255) NOT NULL,
    id_disciplina VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES Curso,
    FOREIGN KEY (id_disciplina) REFERENCES Disciplina
);

INSERT INTO Users ("email", "nome", "encrypted_password") VALUES
("foo@bar.tld", "Usuário Teste", "$2b$12$9wVjTgsFGMex73gvCNn.HepYrvrrSTK8hqiNJxOda4NPrrEr4HxIm");

INSERT INTO Curso ("nome") VALUES
("Ciência da Computação");

INSERT INTO Departamento("nome") VALUES
('Matemática'),
('Ciências Administrativas'),
('Ciência da Computação'),
('Ciências Econômicas'),
('Estatística'),
('Física');

INSERT INTO Disciplina("codigo", "nome", "id_departamento") VALUES
('MAT038',' Geometria Analítica e Álgebra Linear',1),
('CAD011',' Administração',2),
('DCC203',' Programação e Desenvolvimento de Software I',3),
('DCC638',' Introdução à Lógica Computacional',3),
('DCC050',' Introdução à Ciência da Computação',3),
('MAT001',' Cálculo Diferencial e Integral I',1),
('ECN140',' Introdução à Economia',4),
('DCC204',' Programação e Desenvolvimento de Software II',3),
('DCC639',' Álgebra Linear Computacional',3),
('DCC111',' Matemática Discreta',3),
('MAT039',' Cálculo Diferencial e Integral II',1),
('EST032',' Probabilidade',5),
('DCC205',' Estruturas de Dados',3),
('DCC114',' Introdução aos Sistemas Lógicos',3),
('DCC011',' Introdução a Bancos de Dados',3),
('MAT034',' Álgebra A',1),
('DCC212',' Introdução a Ciência dos Dados',3),
('DCC206',' Algoritmos I',3),
('DCC006',' Organização de Computadores I',3),
('DCC129',' Fundamentos da Teoria de Computação',3),
('MAT040',' Equações Diferenciais C',1),
('DCC207',' Algoritmos II',3),
('DCC024',' Linguagens de Programação',3),
('DCC035',' Pesquisa Operacional',3),
('FIS_A',' Introdução à Física Estatística Computacional',6),
('DCC603',' Engenharia de Software',3),
('DCC605',' Sistemas Operacionais',3),
('DCC053',' Compiladores I',3),
('DCC636',' Ética na Computação',3),
('DCC___',' Introdução à Inteligência Artificial',3),
('DCC___',' Fundamentos de Sistemas Paralelos e Distribuídos',3),
('DCC023',' Redes de Computadores',3),
('DCC637',' Computação e Sociedade',3),
('DCC604',' Projeto Orientado em Computação I',3),
('DCC009',' Projeto Orientado em Computação II',3);


INSERT INTO Curso_Disciplina("id","id_curso", "id_disciplina") VALUES
(1,1,1),
(2,1,2),
(3,1,3),
(4,1,4),
(5,1,5),
(6,1,6),
(7,1,7),
(8,1,8),
(9,1,9),
(10,1,10),
(11,1,11),
(12,1,12),
(13,1,13),
(14,1,14),
(15,1,15),
(16,1,16),
(17,1,17),
(18,1,18),
(19,1,19),
(20,1,20),
(21,1,21),
(22,1,22),
(23,1,23),
(24,1,24),
(25,1,25),
(26,1,26),
(27,1,27),
(28,1,28),
(29,1,29),
(30,1,30),
(31,1,31),
(32,1,32),
(33,1,33),
(34,1,34),
(35,1,35);

INSERT INTO Arquivo ("id_contribuinte", "nome", "link", "id_disciplina", "tipo", "professor") VALUES

(1, "Prova 1 - teste", "link aqui", 4, "Prova", "Loureiro"),
(1, "TP Final", "link aqui2", 4, "Trabalho", "Loureiro");