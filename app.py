
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import db
import json
import os
import sqlite3
import datetime
import pandas as pd
from flask import Flask, flash, escape, request, render_template, redirect, url_for
from flask_wtf.file import FileField
from wtforms import SubmitField
from flask_wtf import Form
from flask_login import LoginManager, login_user, logout_user, login_required, login_required, current_user, UserMixin
from flask_uploads import UploadSet, configure_uploads, ALL

app = Flask(__name__)
app.secret_key = 'super secret string'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

## DATABASE ##
app.config['SQLITE3_DATABASE_URI'] = os.path.join(
    app.instance_path, 'database.sqlite')
db.init_app(app)

## LOGIN ##


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    conn = sqlite3.connect('instance/database.sqlite')
    users = pd.read_sql(
        f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
    if not users.size:
        return

    user = User()
    user.id = email
    user.user_id = email
    return user


@login_manager.request_loader
def request_loader(request):
    conn = sqlite3.connect('instance/database.sqlite')
    email = request.form.get('email')
    users = pd.read_sql(
        f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
    if not users.size:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    pw_hash = pd.read_sql(
        f"SELECT encrypted_password FROM Users WHERE Users.email='{email}'", conn)
    if bcrypt.check_password_hash(pw_hash.iloc[0]['encrypted_password'], request.form['password']):
        user.is_authenticated = bcrypt.generate_password_hash(
            request.form['password']) == pw_hash.iloc[0]['encrypted_password']
        return user
    else:
        return


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login(alert_auth=False):
    if request.method == 'GET':
        if 'alert_auth' in request.args:
            alert_auth = request.args['alert_auth']
        return render_template('login.html', alert_auth=alert_auth, wrong_data=False)
    else:
        conn = sqlite3.connect('instance/database.sqlite')
        email = request.form['email']
        id = pd.read_sql(
            f"SELECT id FROM Users WHERE Users.email='{email}'", conn)
        email_in_db = id.size
        pw_hash = pd.read_sql(
            f"SELECT encrypted_password FROM Users WHERE Users.email='{email}'", conn)
        if email_in_db and bcrypt.check_password_hash(pw_hash.iloc[0]['encrypted_password'], request.form['password']):
            user = User()
            user.id = email
            user.email = email
            print("id:", id)
            user.user_id = id.iloc[0]['id']
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', alert_auth=True, wrong_data=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/pesquisar')
@login_required
def pesquisar():
    return render_template('pesquisar.html')


allFiles = UploadSet()

app.config['UPLOADED_FILES_DEST'] = 'uploads'
configure_uploads(app, allFiles)


@app.route('/contribuir', methods=['GET', 'POST'])
# @login_required
def contribuir():
    conn = sqlite3.connect('instance/database.sqlite')
    c = conn.cursor()
    disciplinas = pd.read_sql( "SELECT nome FROM Disciplina ORDER BY nome", conn)
    today = datetime.datetime.now()
    year = today.year
    semester = ((today.month-1)//6)+1

    if request.method == 'GET':
        return render_template('contribuir.html', disciplinas=disciplinas, year=year, semester=semester)

    elif request.method == 'POST':
        disciplina = request.form["disciplina"]
        professorName = request.form["professorName"]
        curso = request.form["curso"]
        fileName = request.form["fileName"]
        tipoArquivo = request.form["tipoArquivo"]
        ano = request.form["ano"]
        semestre = request.form["semestre"]

        user_id = current_user.get_id()
        disciplina_id = pd.read_sql(
            f"SELECT id FROM Disciplina WHERE nome='{disciplina}'", conn)

        c.execute(
            f"INSERT INTO Arquivo ('id_contribuinte', 'nome', 'link', 'id_disciplina', 'tipo', 'professor') VALUES ('{user_id}', '{fileName}', '{fileName}', '{disciplina_id.iloc[0]['id']}', '{tipoArquivo}', '{professorName}' )")

        conn.commit()

        if 'fileUpload' in request.files:
            file = request.files['fileUpload']
            f = allFiles.save(file)

        return render_template('contribuir.html', disciplinas=disciplinas, year=year, semester=semester)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login', alert_auth=True))
