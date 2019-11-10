import sqlite3
import db as db
import pandas as pd
import app as application
import urllib.parse as parse
from unittest import TestCase
from flask_script import Manager

conn = sqlite3.connect('instance/database.sqlite')

class Tests(TestCase):
    def setUp(self):
        self.app = application.app
        self.client = self.app.test_client()

    def test_default_user(self):
        email = "foo@bar.tld"
        conn = sqlite3.connect('instance/database.sqlite')
        users = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        assert users.size == 1

    def test_get_login(self):
        response = self.client.get("/login")
        assert response.status_code == 200

    def test_post_login(self):
        user = dict(email="foo@bar.tld", password="secret")
        response = self.client.post("/login", data=user)
        redirect = parse.urlparse(response.location).path
        assert response.status_code == 302
        assert redirect == "/dashboard"

    def test_invalid_username(self):
        user = dict(email="foo@bar.tldx", password="secret")
        response = self.client.post("/login", data=user)
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_invalid_password(self):
        user = dict(email="foo@bar.tld", password="secretx")
        response = self.client.post("/login", data=user)
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_logout(self):
        # Login
        user = dict(email="foo@bar.tld", password="secret")
        self.client.post("/login", data=user)
        dashboard = self.client.get("/dashboard")
        assert dashboard.status_code == 200
        # Logout
        logout = self.client.get("/logout")
        dashboard = self.client.get("/dashboard")
        redirect = parse.urlparse(logout.location).path
        assert logout.status_code == 302
        assert dashboard.status_code == 302
        assert redirect == "/login"

    def test_get_register(self):
        response = self.client.get("/register")
        assert response.status_code == 200

    def test_post_register(self):
        # Before register
        new_user = dict(nome_pessoa="John Snow", email="john@snow.com", password="abcdef")
        email = new_user["email"]
        user = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        assert user.size == 0

        # After register
        response = self.client.post("/register", data=new_user)
        redirect = parse.urlparse(response.location).path
        user = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        assert response.status_code == 302
        assert redirect == "/login"
        assert user.size == 1

        # Delete new user from database
        c = conn.cursor()
        c.execute(f"DELETE FROM Users WHERE email='{email}'")
        conn.commit()

    def test_post_register_existing_user(self):
        # Check user exists
        new_user = dict(nome_pessoa="John Snow", email="foo@bar.tld", password="abcdef")
        email = new_user["email"]
        user = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        assert user.size == 1
        # Trying to register again
        response = self.client.post("/register", data=new_user)
        redirect = parse.urlparse(response.location).path
        user = pd.read_sql(f"SELECT email FROM Users WHERE Users.email='{email}'", conn)
        assert response.status_code == 302
        assert redirect == "/register"
        assert user.size == 1

    def test_access_dashboard_without_login(self):
        response = self.client.get("/dashboard")
        redirect = parse.urlparse(response.location).path
        assert response.status_code == 302
        assert redirect == "/login"

    def test_access_search_without_login(self):
        response = self.client.get("/pesquisar")
        redirect = parse.urlparse(response.location).path
        assert response.status_code == 302
        assert redirect == "/login"

    def test_access_contribute_without_login(self):
        response = self.client.get("/contribuir")
        redirect = parse.urlparse(response.location).path
        assert response.status_code == 302
        assert redirect == "/login"

    def test_access_search_result_without_login(self):
        response = self.client.get("/pesquisa/result")
        redirect = parse.urlparse(response.location).path
        assert response.status_code == 302
        assert redirect == "/login"

    def test_access_terms_and_conditions_without_login(self):
        response = self.client.get("/termos_condicoes")
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_access_search_result_with_login(self):
        # Login
        user = dict(email="foo@bar.tld", password="secret")
        self.client.post("/login", data=user)
        # Access search result
        response = self.client.get("/pesquisa/result")
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_access_search_with_login(self):
        # Login
        user = dict(email="foo@bar.tld", password="secret")
        self.client.post("/login", data=user)
        # Access search result
        response = self.client.get("/pesquisar")
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_access_contribute_with_login(self):
        # Login
        user = dict(email="foo@bar.tld", password="secret")
        self.client.post("/login", data=user)
        # Access search result
        response = self.client.get("/contribuir")
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_access_dashboard_with_login(self):
        # Login
        user = dict(email="foo@bar.tld", password="secret")
        self.client.post("/login", data=user)
        # Access search result
        response = self.client.get("/dashboard")
        redirect = response.location
        assert response.status_code == 200
        assert redirect == None

    def test_post_search_with_login(self):
        # Login
        user = dict(email="foo@bar.tld", password="secret")
        self.client.post("/login", data=user)
        # Post search
        data = dict(tipoArquivo='Prova', disciplina='', ano='', semestre='', professor='', departamento='')
        response = self.client.post("/pesquisar", data=data)
        redirect = parse.urlparse(response.location).path
        assert response.status_code == 302
        assert redirect == "/pesquisa/result"


manager = Manager(application.app)
manager.add_option('-c', '--config', dest='config', required=False)
