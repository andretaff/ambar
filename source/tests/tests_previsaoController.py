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
from application import previsaoController 
from application import cidadeController
from models.cidadeModel import CidadeModel
from models.previsaoModel import PrevisaoModel
from datetime import datetime

TEST_DB = 'unittest.db'

class PrevisaoControllerTests(unittest.TestCase):
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
    
    def test_storePrevisao(self):    
        # para fins de teste, preciso de uma cidade previamente cadastrada antes de simular as inserções de previsão
        with open('./tests/jsonForecast.txt', 'r') as f:
            dadosForecast = json.load(f) 
        
        session = database.Session()
        cidade = cidadeController.getCidade(dadosForecast['id'], dadosForecast,session)         
        
        previsaoController.storePrevisao(cidade,dadosForecast,session)
        previsao = session.query(PrevisaoModel).join(CidadeModel,CidadeModel.id == PrevisaoModel.idCidade).add_columns(CidadeModel.nome.label('nome'),PrevisaoModel.temperaturaMaxima.label('tempmax'))\
                                    .filter(CidadeModel.id == dadosForecast['id']).order_by(PrevisaoModel.data).limit(1)
        previsao = previsao.first()
        self.assertEqual(previsao.tempmax, dadosForecast['data'][0]['temperature']['max'], 'Verificando se a previsão está sendo armazenada corretamente')
        session.rollback()
        
    def test_getAnalise(self):
        with open('./tests/jsonForecast.txt', 'r') as f:
            dadosForecast = json.load(f) 
        
        session = database.Session()
        cidade = cidadeController.getCidade(dadosForecast['id'], dadosForecast,session)         
        
        previsaoController.storePrevisao(cidade,dadosForecast,session)
        
        session.commit()
        
        with open('./tests/jsonForecastOutro.txt', 'r') as f:
            dadosForecast2 = json.load(f) 

        cidade = cidadeController.getCidade(dadosForecast2['id'], dadosForecast2,session)         
        
        previsaoController.storePrevisao(cidade,dadosForecast2,session)
        
        session.commit()
        
        dtIni = dadosForecast['data'][0]['date']
        maxtemp = -1
        cidade = dadosForecast['name']
        acumulado = 0.0
        contador = 0
        for item in dadosForecast['data']:
            dtFim = item['date']
            if item['temperature']['max']>maxtemp:
                maxtemp = item['temperature']['max']
            acumulado = acumulado + item['rain']['precipitation']
            contador = contador + 1
        mediaCidade1 = acumulado/contador
        acumulado = 0.0
        contador = 0
        for item in dadosForecast2['data']:
            if item['temperature']['max']>maxtemp:
                maxtemp = item['temperature']['max']
                cidade = dadosForecast2['name']
            acumulado = acumulado + item['rain']['precipitation']
            contador = contador + 1
        mediaCidade2 = acumulado/contador

        retorno = previsaoController.getAnalise(datetime.strptime(dtIni,'%Y-%m-%d'),datetime.strptime(dtFim,'%Y-%m-%d'),session)
        print(retorno.msg)
        
        self.assertEqual(retorno.status, True, 'temperatura max')
        self.assertEqual(retorno.dados['cidademaxtemp'],cidade,'temperatura max')
        self.assertEqual(retorno.dados['temperatura'],maxtemp,'temperatura max')        
        if retorno.dados['medias'][0]['cidade']==dadosForecast['name']:
            self.assertEqual(retorno.dados['medias'][0]['mediaPrecipitacao'], "{0:.2f}".format((mediaCidade1)), 'media precipitação')
            self.assertEqual(retorno.dados['medias'][1]['mediaPrecipitacao'], "{0:.2f}".format((mediaCidade2)), 'media precipitação')
        else:
            self.assertEqual(retorno.dados['medias'][1]['mediaPrecipitacao'], "{0:.2f}".format((mediaCidade1)), 'media precipitação')
            self.assertEqual(retorno.dados['medias'][0]['mediaPrecipitacao'], "{0:.2f}".format((mediaCidade2)), 'media precipitação')
        
        
if __name__ == "__main__":
    unittest.main()            