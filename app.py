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
from models import User

app.config['SQLITE3_DATABASE_URI']=os.path.join(app.instance_path, 'database.sqlite')
db.init_app(app)

## LOGIN ##
@login_manager.user_loader
def user_loader(email):
  conn = sqlite3.connect('instance/database.sqlite')
  users = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
  if not users.size:
    return
  
  user = User()
  user.id = email
  return user

## ROUTES ##
@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login(alert_auth = False, created_user = False):
  if request.method == 'GET':
    if 'alert_auth' in request.args: alert_auth = request.args['alert_auth']
    if 'created_user' in request.args: created_user = request.args['created_user']
    return render_template('login.html', alert_auth=alert_auth, created_user=created_user, wrong_data=False)
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
def register(email_exists = False):
  if request.method == 'GET':
    if 'email_exists' in request.args: email_exists = request.args['email_exists']
    return render_template('register.html', email_exists=email_exists)
  else:
    conn = sqlite3.connect('instance/database.sqlite')
    c = conn.cursor()

    email = request.form['email']
    user = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
    email_in_db = user.size
    if email_in_db:
      return redirect(url_for('register', email_exists=True))
    else:
      nome_pessoa = request.form['nome_pessoa']
      pw_hash = bcrypt.generate_password_hash(request.form['password'])
      pw_hash = str(pw_hash)[2:len(pw_hash)+2]
      c.execute(f"INSERT INTO Users ('nome', 'email', 'encrypted_password') VALUES ('{nome_pessoa}', '{email}', '{pw_hash}')")
      conn.commit()
      return redirect(url_for('login', created_user=True))


@app.route('/dashboard')
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/pesquisar')
@login_required
def pesquisar():
  return render_template('pesquisar.html')

@app.route('/contribuir')
@login_required
def contribuir():
  return render_template('contribuir.html')

@app.route('/termos_condicoes')
def termos_condicoes():
  return render_template('termos_condicoes.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
  return redirect(url_for('login', alert_auth=True))
