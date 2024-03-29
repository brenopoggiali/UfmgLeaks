from models import User
from flask_bcrypt import Bcrypt
import db
import os
import sqlite3
import datetime
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, \
                        login_required, current_user

app = Flask(__name__)
app.jinja_options = {}
app.secret_key = 'super secret string'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# DATABASE ##

app.config['SQLITE3_DATABASE_URI'] = os.path.join(app.instance_path,
                                                  'database.sqlite')
db.init_app(app)

# LOGIN ##
@login_manager.user_loader
def user_loader(email):
    conn = sqlite3.connect('instance/database.sqlite')
    users = pd.read_sql(
        f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
    if not users.size:
        return
    user = User()
    user.id = email
    return user

# ROUTES ##
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login(alert_auth=False, created_user=False):
    if request.method == 'GET':
        if 'alert_auth' in request.args:
            alert_auth = request.args['alert_auth']
        if 'created_user' in request.args:
            created_user = request.args['created_user']
        return render_template('login.html', alert_auth=alert_auth,
                               created_user=created_user, wrong_data=False)
    else:
        conn = sqlite3.connect('instance/database.sqlite')
        email = request.form['email']
        user = pd.read_sql(
            f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        email_in_db = user.size
        pw_hash = pd.read_sql(
            f"SELECT encrypted_password FROM Users \
              WHERE Users.email='{email}'", conn)
        if email_in_db and bcrypt.check_password_hash(
            pw_hash.iloc[0]['encrypted_password'],
            request.form['password']
        ):
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html',
                                   alert_auth=True,
                                   wrong_data=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register(email_exists=False):
    if request.method == 'GET':
        if 'email_exists' in request.args:
            email_exists = request.args['email_exists']
        return render_template('register.html', email_exists=email_exists)
    else:
        conn = sqlite3.connect('instance/database.sqlite')
        c = conn.cursor()

        email = request.form['email']
        user = pd.read_sql(
            f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        email_in_db = user.size
        if email_in_db:
            return redirect(url_for('register', email_exists=True))
        else:
            nome_pessoa = request.form['nome_pessoa']
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            pw_hash = str(pw_hash)[2:len(pw_hash)+2]
            c.execute(
                f"INSERT INTO Users ('nome', 'email', 'encrypted_password') \
                VALUES ('{nome_pessoa}', '{email}', '{pw_hash}')")
            conn.commit()
            return redirect(url_for('login', created_user=True))


@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('instance/database.sqlite')
    meus_arquivos = pd.read_sql(
        f"SELECT Arquivo.nome, Arquivo.tipo, Disciplina.nome, \
        Arquivo.professor, ano, semestre \
        FROM Arquivo JOIN Users ON Arquivo.id_contribuinte = Users.id \
        JOIN Disciplina ON Arquivo.id_disciplina = Disciplina.id \
        WHERE Users.email='{current_user.id}' \
        ORDER BY Arquivo.id DESC LIMIT 100", conn)
    arquivos_gerais = pd.read_sql(
        f"SELECT Arquivo.nome, Users.nome, Arquivo.tipo, Disciplina.nome, \
        Arquivo.professor, ano, semestre \
        FROM Arquivo JOIN Users ON Arquivo.id_contribuinte = Users.id \
        JOIN Disciplina ON Arquivo.id_disciplina = Disciplina.id \
        ORDER BY Arquivo.id DESC LIMIT 10", conn)
    return render_template('dashboard.html',
                           meus_arquivos=meus_arquivos,
                           arquivos_gerais=arquivos_gerais)


@app.route('/pesquisar',  methods=['GET', 'POST'])
@login_required
def pesquisar():
    if request.method == 'GET':
        conn = sqlite3.connect('instance/database.sqlite')
        disciplinas = pd.read_sql(
            "SELECT nome FROM Disciplina ORDER BY nome", conn)
        return render_template('pesquisar.html', disciplinas=disciplinas)
    else:
        arquivo = request.form['tipoArquivo']
        if(arquivo == ''):
            arquivo = False

        disciplina = request.form['disciplina']
        if(disciplina == ''):
            disciplina = False

        ano = request.form['ano']
        if(ano == ''):
            ano = False

        semestre = request.form['semestre']
        if(semestre == ''):
            semestre = False

        professor = request.form['professor']
        if(professor == ''):
            professor = False

        departamento = request.form['departamento']
        if(departamento == ''):
            departamento = False
        return redirect(url_for('pesquisa_result',
                        arquivo=arquivo.capitalize(),
                        departamento=departamento,
                        disciplina=disciplina,
                        professor=professor,
                        semestre=semestre,
                        ano=ano))


@app.route('/pesquisa/result')
@login_required
def pesquisa_result(arquivo='False', disciplina='False', ano='False',
                    semestre='False', professor='False', departamento='False'):

    conn = sqlite3.connect('instance/database.sqlite')
    query = f"SELECT Arquivo.tipo, Disciplina.nome as disciplina, \
    Arquivo.nome as arquivo,Arquivo.Ano,Arquivo.semestre,Arquivo.professor, \
    Departamento.nome as departamento \
    FROM Arquivo JOIN Disciplina \
    ON Arquivo.id_disciplina=Disciplina.id JOIN Departamento \
    ON Disciplina.id_departamento=Departamento.id"

    # Grab passed arguments
    if 'arquivo' in request.args:
        arquivo = request.args['arquivo']
    if 'disciplina' in request.args:
        disciplina = request.args['disciplina']
    if 'ano' in request.args:
        ano = request.args['ano']
    if 'semestre' in request.args:
        semestre = request.args['semestre']
    if 'professor' in request.args:
        professor = request.args['professor']
    if 'departamento' in request.args:
        departamento = request.args['departamento']

    if(arquivo != 'False'):
        query = query+f" WHERE Arquivo.tipo='{arquivo}'"

    if(disciplina != 'False'):
        query = query+f" AND Disciplina.nome='{disciplina}'"

    if(ano != 'False'):
        query = query+f" AND Arquivo.nome={ano}"

    if(semestre != 'False'):
        query = query+f" AND Arquivo.semestre={semestre}"

    if(professor != 'False'):
        query = query+f" AND Arquivo.professor='{professor}'"

    if(departamento != 'False'):
        query = query+f" AND Departamento.nome='{departamento}'"

    result = pd.read_sql(query, conn)
    return render_template('pesquisa_result.html', result=result)


app.config['UPLOAD_DEST'] = os.getcwd() + '/uploads'


@app.route('/contribuir', methods=['GET', 'POST'])
@login_required
def contribuir():
    conn = sqlite3.connect('instance/database.sqlite')
    c = conn.cursor()
    disciplinas = pd.read_sql(
        "SELECT nome FROM Disciplina ORDER BY nome", conn)
    cursos = pd.read_sql(
        "SELECT nome FROM Curso ORDER BY nome", conn)

    today = datetime.datetime.now()
    year = today.year
    semester = ((today.month-1)//6)+1

    if request.method == 'GET':
        return render_template('contribuir.html',
                               disciplinas=disciplinas,
                               semester=semester,
                               cursos=cursos,
                               year=year)

    elif request.method == 'POST':
        disciplina = request.form["disciplina"]
        tipoArquivo = request.form["tipoArquivo"].capitalize()
        ano = request.form["ano"]
        semestre = request.form["semestre"]
        professorName = request.form["professorName"]

        user_id = current_user.get_id()
        user_id = pd.read_sql(f"SELECT id FROM Users WHERE email='{user_id}'",
                              conn).iloc[0]["id"]

        disciplina_id = pd.read_sql(
            f"SELECT id FROM Disciplina WHERE nome='{disciplina}'", conn)

        if 'fileUpload' in request.files:
            file = request.files['fileUpload']
            newFileName = '-'.join(file.filename.split())
            if os.path.exists(os.getcwd() + '/uploads') is False:
                os.makedirs('uploads')
            file.save(os.path.join(
                app.config["UPLOAD_DEST"], str(today.microsecond) + "_"
                + newFileName))
            fileName = str(today.microsecond) + "_" + newFileName
        else:
            fileName = "no_file_selected"

        c.execute(
            f"INSERT INTO Arquivo ('id_contribuinte', 'nome', 'link', \
            'id_disciplina', 'tipo', 'professor', 'ano', 'semestre') \
            VALUES ('{user_id}', '{fileName}', '{fileName}', \
            '{disciplina_id.iloc[0]['id']}', '{tipoArquivo}', \
            '{professorName}', '{ano}', '{semestre}' )")

        conn.commit()

        return render_template('contribuir.html',
                               disciplinas=disciplinas,
                               semester=semester,
                               cursos=cursos,
                               year=year)


@app.route('/termos_condicoes')
def termos_condicoes():
    return render_template('termos_condicoes.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login', alert_auth=True))
