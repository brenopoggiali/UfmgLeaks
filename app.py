from flask import Flask, escape, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
  return redirect(url_for('login'))

@app.route('/login', methods=('GET','POST'))
def login():
  return render_template('login.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
  return render_template('register.html')

