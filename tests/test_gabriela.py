import sqlite3
import app as application
from unittest import TestCase
from flask_script import Manager

conn = sqlite3.connect('instance/database.sqlite')


class Tests(TestCase):
    def setUp(self):
        self.app = application.app
        self.client = self.app.test_client()

    # verifica se existe erro ao inserir uma disciplina em um curso inexistente
    def test_custo_existente(self):
        try:
            conn.execute(
                "INSERT INTO Curso_Disciplina('id_curso', 'id_disciplina') " +
                "VALUES ((select id from Curso where " +
                "nome='Curso inexistente'), " +
                "(select id from Disciplina where codigo = 'ECN076'));")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica possibilildade de inserir novo curso
    def test_criar_novo_curso(self):
        try:
            conn.execute("INSERT INTO Curso ('nome') VALUES " +
                         "('Novo curso');")
            assert True
        except sqlite3.IntegrityError:
            assert False

    # verifica impossibilidade de inserir um departamento sem código
    def test_obrig_cod_dep(self):
        try:
            conn.execute("INSERT INTO Departamento('nome') VALUES " +
                         "('Departamento sem código');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um departamento repetido
    def test_departamento_repetido(self):
        try:
            conn.execute("INSERT INTO Departamento('id','nome') VALUES " +
                         "('DCC','Ciência da Computação');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir uma disciplina sem código
    def test_disciplina_sem_codigo(self):
        try:
            conn.execute(
                "INSERT INTO Disciplina('nome', 'id_departamento') VALUES " +
                "('Disciplina sem código','DCC')")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir uma disciplina sem nome
    def test_disciplina_sem_nome(self):
        try:
            conn.execute(
                "INSERT INTO Disciplina('codigo', 'id_departamento') VALUES " +
                "('DCC666','DCC')")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir uma disciplina sem departamento
    def test_disciplina_sem_departamento(self):
        try:
            conn.execute("INSERT INTO Disciplina('codigo', 'nome') VALUES " +
                         "('000000','Disciplina sem departamento')")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade inserir disciplina em departamento inexistente
    def test_disciplina_em_dep_inexistente(self):
        try:
            conn.execute(
                "INSERT INTO Disciplina('codigo','nome','id_departamento') " +
                "VALUES ('000000','Disciplina em departamento inexistente', " +
                "(SELECT id from Departamento where nome='Dep inexistente'))")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um usuário sem email
    def test_usuario_sem_email(self):
        try:
            conn.execute(
                "INSERT INTO Users ('nome', 'encrypted_password') VALUES " +
                "('Usuário Teste', '$2b$12$9wVjTgsFGMex73gvCNn.HepYrvrrST" +
                "K8hqiNJxOda4NPrrEr4HxIm');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um usuário sem nome
    def test_usuario_sem_nome(self):
        try:
            conn.execute(
                "INSERT INTO Users ('email', 'encrypted_password') VALUES " +
                "('foo@bar.tld', '$2b$12$9wVjTgsFGMex73gvCNn.HepYrvrrSTK8hqi" +
                "NJxOda4NPrrEr4HxIm');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um usuário sem senha
    def test_usuario_sem_senha(self):
        try:
            conn.execute("INSERT INTO Users ('email', 'nome') VALUES " +
                         "('foo@bar.tld', 'Usuário Teste');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um arquivo sem contribuinte
    def test_arquivo_sem_contribuinte(self):
        try:
            conn.execute(
                "INSERT INTO Arquivo ('nome', 'link', 'id_disciplina', " +
                "'tipo', 'ano', 'semestre', 'professor') VALUES " +
                "('Prova 1', '0000001', (select id from Disciplina " +
                "where nome = 'MATEMATICA DISCRETA' ), 'Prova', 2018, 1, " +
                "'Loureiro');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um arquivo com link repetido
    def test_arquivo_link_repetido(self):
        try:
            conn.execute(
                "INSERT INTO Arquivo ('id_contribuinte', 'nome','link', " +
                "'id_disciplina', 'tipo', 'ano', 'semestre', 'professor') " +
                "VALUES (1,'Prova 1','link aqui',(select id from Disciplina " +
                "where nome = 'MATEMATICA DISCRETA' ), 'Prova', 2018, 1," +
                "'Loureiro');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um arquivo sem disciplina
    def test_arquivo_sem_disciplina(self):
        try:
            conn.execute(
                "INSERT INTO Arquivo ('id_contribuinte', 'nome', 'link'," +
                "'id_disciplina', 'tipo', 'ano', 'semestre', 'professor') " +
                "VALUES (1, 'Prova 1', '0000002', (select id from Disciplina" +
                " where nome = 'DISCIPLINA INEXISTENTE' ), 'Prova', 2018, 1," +
                "'Loureiro');")
            assert False
        except sqlite3.IntegrityError:
            assert True

    # verifica impossibilidade de inserir um arquivo sem tipo
    def test_arquivo_sem_tipo(self):
        try:
            conn.execute(
                "INSERT INTO Arquivo ('id_contribuinte', 'nome', 'link'," +
                "'id_disciplina', 'ano', 'semestre', 'professor') VALUES " +
                "(1, 'Prova 1', '0000003', (select id from Disciplina " +
                "WHERE nome = 'MATEMATICA DISCRETA' ), 2018, 1, 'Loureiro');")
            assert False
        except sqlite3.IntegrityError:
            assert True


manager = Manager(application.app)
manager.add_option('-c', '--config', dest='config', required=False)

if __name__ == '__main__':
    manager.run()
