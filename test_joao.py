import unittest
import os
from flask import request
from app import app


class TestHomeView(unittest.TestCase):

    # Initial setup
    def setUp(self):
        self.client = app.test_client()
        self.response = self.client.get('/')

    # Login with the given user info
    def login(self, email, password):
        return self.client.post('/login', data={'email': email,
                                                'password': password},
                                follow_redirects=True)

    # Test if "/" redirects to login with status code 302
    def test_get_home(self):
        self.assertEqual(302, self.response.status_code)

    # Test create user page access
    def test_create_page(self):
        # success
        with self.client:
            self.assertEqual(200, self.client.get('/register').status_code)

    # Test login of a random user (can change to test dif users)
    def test_login(self):
        email = 'joaoh@gmail.com'
        password = '123456'
        # success
        with self.client:
            self.assertEqual(200, self.login(email, password).status_code)

    # logout test, must fail due to not being logged in (thus 302 redirect to login status code)
    def test_logout_failed(self):
        with self.client:
            self.assertEqual(302, self.client.get('/logout').status_code)

    # Test contribuir access
    def test_contribuir(self):
        email = 'joao@gmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(302, self.client.get('/contribuir').status_code)

    # Test failed contribuir access due to no login
    def test_contribuir_noLogin_failed(self):
        # success
        with self.client:
            self.client.get('/contribuir', follow_redirects=True)
            self.assertEqual('/login', request.path)

    # Test contribuir access (typo acess, correct way is contribuir)
    def test_contribir(self):
        email = 'joaoh@gmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(404, self.client.get('/contribir').status_code)

    # Test create user, on sucess, redirects to login

    def test_create_user(self):
        # success
        nome_pessoa = 'aa'
        email = 'joao@gmail.com'
        password = 'secret'
        c_password = 'secret'
        # success
        with self.client:
            response = self.client.post('/register', data={'nome_pessoa': nome_pessoa,
                                                           'email': email,
                                                           'password': password,
                                                           'c_password': c_password}).status_code
            self.assertEqual(302, response)
