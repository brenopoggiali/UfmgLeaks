import unittest
from flask import request
from app import app


class TestHomeView(unittest.TestCase):

    # Initial setup
    def setUp(self):
        self.client = app.test_client()
        self.response = self.client.get('/')

    # Login no sistema
    def login(self, email, password):
        return self.client.post('/login', data={'email': email,
                                                'password': password},
                                follow_redirects=True)


    # Test redirect to login (302)
    def test_get_home(self):
        self.assertEqual(302, self.response.status_code)

    # Test create user page access
    def test_create_page(self):
        # success
        self.assertEqual(200, self.client.get('/register').status_code)

    # Test login of a random user (can change to test dif users)
    def test_login(self):
        email = 'test@gmail.com'
        password = 'test1234'
        # success
        self.assertEqual(200, self.login(email, password).status_code)


    # logout test, must redirect to login (thus 302 status code)
    def test_logout(self):
        email = 'pep445@hotmail.com'
        password = '123456'
        with self.client:
            self.login(email, password)
            self.assertEqual(302, self.client.get('/logout').status_code)

    # Test dashboard access
    def test_dashboard(self):
        email = 'foo@bar.tld'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/dashboard').status_code)


    # Test pesquisar access
    def test_pesquisar(self):
        email = 'test@gmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/pesquisar').status_code)

    # Test pesquisa_result access
    def test_pesquisa_result(self):
        # success
        email = 'test@gmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get(
                '/pesquisa/result').status_code)

    # Test contribuir access
    def test_contribuir(self):
        email = 'test@gmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/contribuir').status_code)

    # Post requests
    #

    # Test create user, on sucess, redirects to login
    def test_create_user(self):
        # success
        nome_pessoa = 'teste_nome'
        email = 'test@gmail.com'
        password = '1111'
        c_password = '1111'
        # success
        with self.client:
            resp = self.client.post('/register', data={'nome_pessoa': nome_pessoa,
                                                           'email': email,
                                                           'password': password,
                                                           'c_password': c_password}).status_code
            self.assertEqual(302, resp)

