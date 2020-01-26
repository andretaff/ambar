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
from application import cidadeController 


TEST_DB = 'unittest.db'

class CidadeControllerTests(unittest.TestCase):
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
    
    def test_getCidadeInexistente(self):
        dados = {'name': 'Test','state' : 'sp', 'country':'braz','id':555}
        session = database.Session()
        cidade = cidadeController.getCidade(dados['id'], dados,session) 
        self.assertEqual(cidade.id, dados['id'], 'recuperando cidade do banco')
        self.assertEqual(cidade.nome, dados['name'], 'recuperando cidade do banco')
        self.assertEqual(cidade.estado, dados['state'], 'recuperando cidade do banco')
        self.assertEqual(cidade.pais, dados['country'], 'recuperando cidade do banco')
        
    def test_getCidadeExistente(self):
        dados = {'name': 'Test','state' : 'sp', 'country':'braz','id':999}
        session = database.Session()
        cidadeController.getCidade(dados['id'], dados,session)
        session.commit()
        cidade = cidadeController.getCidade(dados['id'], dados,session) #fazendo duas vezes para simular uma cidade já cadastrada
         
        self.assertEqual(cidade.id, dados['id'], 'recuperando cidade do banco')
        self.assertEqual(cidade.nome, dados['name'], 'recuperando cidade do banco')
        self.assertEqual(cidade.estado, dados['state'], 'recuperando cidade do banco')
        self.assertEqual(cidade.pais, dados['country'], 'recuperando cidade do banco')

        
if __name__ == "__main__":
    unittest.main()    
        