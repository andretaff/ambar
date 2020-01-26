'''
Created on Jan 25, 2020

@author: Taffarello
'''
import unittest
from models import database
import ambar
from sqlalchemy import create_engine
from flask import Flask
import json
from models.cidadeModel import CidadeModel 


TEST_DB = 'unittest.db'

class RouteTests(unittest.TestCase):
    def setUp(self):
        ambar.app.config['TESTING'] = True
        ambar.app.config['WTF_CSRF_ENABLED'] = False
        ambar.app.config['DEBUG'] = False
        ambar.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ TEST_DB
        
        self.client = ambar.app.test_client()
        
        engine = create_engine(ambar.app.config['SQLALCHEMY_DATABASE_URI'])
        database.Session.configure(bind=engine)        
        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)
    
        # Disable sending emails during unit testing
        #ambar.mail.init_app(ambar.app)
        self.assertEqual(ambar.app.debug, False)
        
       
    
    def test_mainPage(self):
        resposta = self.client.get('/', follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
    
    def test_getCidadeWrongParameters(self):
        resposta = self.client.get('/cidade', query_string=dict(id=''), follow_redirects=True)
        dados = json.loads(resposta.get_data(as_text=True))
        
        self.assertEqual(resposta.status_code, 400, 'Retorno sem parâmetro')
        
        self.assertEqual(dados['status'], False, 'Retorno sem parãmetro')
        

        resposta = self.client.get('/cidade', query_string=dict(id='ZZZZ'), follow_redirects=True)
        dados = json.loads(resposta.get_data(as_text=True))
        
        self.assertEqual(resposta.status_code, 400, 'Retorno com parâmetro não numérico')
        self.assertEqual(dados['status'], False, 'Retorno com parâmetro não numérico')
        
        
    def test_getCidadeOk(self):
        resposta = self.client.get('/cidade', query_string=dict(id='3478'), follow_redirects=True)
        dados = json.loads(resposta.get_data(as_text=True))
        self.assertEqual(resposta.status_code, 200, 'Retorno buscando cidade')
        self.assertEqual(dados['status'], True, 'Retorno buscando cidade')
        
        session = database.Session()
        query = session.query(CidadeModel).get(3478)
        self.assertEqual(query.nome, 'São Pedro do Turvo', 'Testando armazenamento da cidade')
             
    def test_getAnaliseOk(self):
        resposta = self.client.get('/analise', query_string=dict(data_inicial='',data_final=''), follow_redirects=True)
        dados = json.loads(resposta.get_data(as_text=True))
        self.assertEqual(resposta.status_code, 400, 'Retorno buscando análise sem params')
        self.assertEqual(dados['status'], False, 'Retorno buscando análise sem params')

        resposta = self.client.get('/analise', query_string=dict(data_inicial='xx',data_final='xxx'), follow_redirects=True)
        dados = json.loads(resposta.get_data(as_text=True))
        self.assertEqual(resposta.status_code, 400, 'Retorno buscando análise com params incorretos')
        self.assertEqual(dados['status'], False, 'Retorno buscando análise com params incorretos')
        
        resposta = self.client.get('/analise', query_string=dict(data_inicial='01/01/2010',data_final='10/10/2009'), follow_redirects=True)
        dados = json.loads(resposta.get_data(as_text=True))
        self.assertEqual(resposta.status_code, 400, 'Retorno buscando análise com params incorretos')
        self.assertEqual(dados['status'], False, 'Retorno buscando análise com params incorretos')       
    
        
    
if __name__ == "__main__":
    unittest.main()    
