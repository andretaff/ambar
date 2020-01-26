'''
Created on Jan 21, 2020

@author: Taffarello
'''
import requests
import json
from models import cidadeModel
from models import previsaoModel
from models import database
from application import cidadeController
from application import previsaoController
from application.resposta import Resposta

url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/'
url_end = '/days/15?token='
token = 'b22460a8b91ac5f1d48f5b7029891b53'

def getPrevisaoCidade(idCidade):
    resposta = Resposta()
    try:  
        retorno = requests.get(url+str(idCidade)+url_end+token)
    except:
        resposta.status = False
        resposta.status_code = 500
        resposta.msg = 'Erro ao recuperar dados do webservice'
        return resposta
    
    if retorno.status_code != 200:
        resposta.status = False
        resposta.status_code = 500
        resposta.msg = 'Erro ao recuperar dados do webservice, status: '+str(retorno.status_code) + ' '+retorno.text
        return resposta
    
    dados = retorno.json()
    
     
    try:
        session = database.Session()    
        cidade = cidadeController.getCidade(idCidade, dados,session)
        previsaoController.storePrevisao(cidade, dados,session)
        resposta.dados = {'cidade':cidade.nome}
        session.commit()
    except:
        resposta.status = False
        resposta.msg = 'Erro ao armazenar dados no banco'
    
    
    return resposta
    
    
def getAnalise(dtInicio, dtFim):
    session = database.Session()
    retorno = previsaoController.getAnalise(dtInicio, dtFim, session)
    session.commit()
    return retorno
    
    