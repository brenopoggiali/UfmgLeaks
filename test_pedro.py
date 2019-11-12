import unittest
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


    ## Pages access and redirects
    ##

    # Test if / redirects  302 ("redirects to login")
    def test_get_home(self):
        self.assertEqual(302, self.response.status_code)

    # Test create user page access
    def test_create_page(self):
            # success
            self.assertEqual(200, self.client.get('/register').status_code)

    # Test login of a random user (can change to test dif users)
    def test_login(self):
            email = 'pep445@hotmail.com'
            password = '123456'
            # success
            self.assertEqual(200, self.login(email, password).status_code)
    
    # logout test, must fail due to not being logged in (thus 302 redirect to login status code)
    def test_failed_logout(self):
        with self.client:
            self.assertEqual(302, self.client.get('/logout').status_code)

    # logout test, must redirect to login (thus 302 status code)
    def test_logout(self):
        email = 'pep445@hotmail.com'
        password = '123456'
        with self.client:
            self.login(email, password)
            self.assertEqual(302, self.client.get('/logout').status_code)

    # Test dashboard access
    def test_dashboard(self):
        email = 'pep445@hotmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/dashboard').status_code)

    # Test failed dashboard access due to no login 
    def test_failed_dashboard(self):
        # success
        with self.client:
            self.assertEqual(200, self.client.get('/dashboard', follow_redirects=True).status_code)
            self.assertEqual('/login', request.path)    

    # Test pesquisa access (typo acess, correct way is pesquisar)
    def test_pesquisa(self):
        email = 'pep445@hotmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(404, self.client.get('/pesquisa').status_code)

    # Test pesquisar access
    def test_pesquisar(self):
        email = 'pep445@hotmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/pesquisar').status_code)
    
    # Test failed pesquisar access due to no login 
    def test_failed_pesquisar(self):
        # success
        with self.client:
            self.assertEqual(200, self.client.get('/pesquisar', follow_redirects=True).status_code)
            self.assertEqual('/login', request.path)
    
    # Test pesquisa_result access
    def test_pesquisa_result(self):
        # success
        email = 'pep445@hotmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/pesquisa/result').status_code)
    
 # Test failed pesquisa_result access due to no login 
    def test_failed_pesquisa_result(self):
        # success
        with self.client:
            self.assertEqual(200, self.client.get('/pesquisa/result', follow_redirects=True).status_code)
            self.assertEqual('/login', request.path)

    # Test contribuir access
    def test_contribuir(self):
        email = 'pep445@hotmail.com'
        password = '123456'
        # success
        with self.client:
            self.login(email, password)
            self.assertEqual(200, self.client.get('/contribuir').status_code)

    # Test termos e condicoes access
    def test_termos_e_condicoes(self):
        # success
        with self.client:
            self.assertEqual(200, self.client.get('/termos_condicoes').status_code)

    # Post requests
    #

    # Test create user, on sucess, redirects to login
    def test_create_user(self):
        # success
        nome_pessoa = 'aa'
        email = 'aaa@hotmail.com'
        password = '123456'
        c_password = '123456'
        # success
        with self.client:
            response = self.client.post('/register', data={'nome_pessoa' : nome_pessoa, 
                                                         'email': email,
                                                         'password': password,
                                                         'c_password': c_password}).status_code
            self.assertEqual(302, response)


    # Test post 'tipo de arquivo = Prova' on pesquisa
    #def test_post_pesquisa_tipoArquivo(self):
    #    # success
    #    email = 'pep445@hotmail.com'
    #    password = '123456'
    #    # success
    #    with self.client:
    #        self.login(email, password)
    #        self.assertEqual(200, self.client.post('/pesquisa', data= {'disciplina' : '',
    #                                                                    'tipoArquivo' : 'Prova',
    #                                                                    'ano' : '',
    #                                                                    'semestre' : '',
    #                                                                    'professor': '',
    #                                                                    'departamento':''}).status_code)





