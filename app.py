import os
import sqlite3
import pandas as pd
from flask import Flask, escape, request, render_template, redirect, url_for
from flask_login import (LoginManager, login_user, logout_user, login_required,
            login_required, current_user, UserMixin)
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'super secret string'
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

## DATABASE ##
import db
app.config['SQLITE3_DATABASE_URI']=os.path.join(app.instance_path, 'database.sqlite')
db.init_app(app)

## LOGIN ##
class User(UserMixin):
  pass


@login_manager.user_loader
def user_loader(email):
  conn = sqlite3.connect('instance/database.sqlite')
  users = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
  if not users.size:
    return
  
  user = User()
  user.id = email
  return user


@login_manager.request_loader
def request_loader(request):
  conn = sqlite3.connect('instance/database.sqlite')
  email = request.form.get('email')
  users = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
  if not users.size:
    return

  user = User()
  user.id = email

  # DO NOT ever store passwords in plaintext and always compare password
  # hashes using constant-time comparison!
  pw_hash = pd.read_sql(f"SELECT encrypted_password FROM Users WHERE Users.email='{email}'", conn)
  if bcrypt.check_password_hash(pw_hash.iloc[0]['encrypted_password'], request.form['password']):
    user.is_authenticated = bcrypt.generate_password_hash(request.form['password']) == pw_hash.iloc[0]['encrypted_password']
    return user
  else:
    return

@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login(alert_auth = False):
  if request.method == 'GET':
    if 'alert_auth' in request.args: alert_auth = request.args['alert_auth']
    return render_template('login.html', alert_auth=alert_auth, wrong_data=False)
  else:
    conn = sqlite3.connect('instance/database.sqlite')
    email = request.form['email']
    user = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
    email_in_db = user.size
    pw_hash = pd.read_sql(f"SELECT encrypted_password FROM Users WHERE Users.email='{email}'", conn)
    if email_in_db and bcrypt.check_password_hash(pw_hash.iloc[0]['encrypted_password'], request.form['password']):
      user = User()
      user.id = email
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
  conn = sqlite3.connect('instance/database.sqlite')
  meus_arquivos = pd.read_sql(f"SELECT Arquivo.nome, Arquivo.tipo, Disciplina.nome, Arquivo.professor, ano, semestre \
                                FROM Arquivo JOIN Users ON Arquivo.id_contribuinte = Users.id \
                                JOIN Disciplina ON Arquivo.id_disciplina = Disciplina.id \
                                WHERE Users.email='{current_user.id}' ORDER BY Arquivo.id DESC LIMIT 100", conn)
  arquivos_gerais = pd.read_sql(f"SELECT Arquivo.nome, Users.nome, Arquivo.tipo, Disciplina.nome, Arquivo.professor, \
                                ano, semestre \
                                FROM Arquivo JOIN Users ON Arquivo.id_contribuinte = Users.id \
                                JOIN Disciplina ON Arquivo.id_disciplina = Disciplina.id \
                                ORDER BY Arquivo.id DESC LIMIT 10", conn)
  return render_template('dashboard.html', meus_arquivos = meus_arquivos, arquivos_gerais = arquivos_gerais)



@app.route('/pesquisar')
@login_required
def pesquisar():
  return render_template('pesquisar.html')

@app.route('/contribuir')
@login_required
def contribuir():
  return render_template('contribuir.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
  return redirect(url_for('login', alert_auth=True))
