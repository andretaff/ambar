'''
Created on Jan 23, 2020

@author: Taffarello
'''
from models.previsaoModel import PrevisaoModel
from models.cidadeModel import CidadeModel
from models import database
import time
from datetime import datetime, timedelta
from sqlalchemy import desc,func
from application.resposta import Resposta

def storePrevisao(cidade,dadosJSon,session):
        
    for diaPrevisao in dadosJSon['data']:
        instanciaPrevisao  = session.query(PrevisaoModel).filter(PrevisaoModel.idCidade==cidade.id).filter(PrevisaoModel.data==diaPrevisao['date']).one_or_none()
        novo = False
        if instanciaPrevisao is None:
            instanciaPrevisao = PrevisaoModel()
            instanciaPrevisao.idCidade = cidade.id
            instanciaPrevisao.data = datetime.strptime(diaPrevisao['date'],'%Y-%m-%d')
            novo = True
            
        instanciaPrevisao.chuvaPrecipitacao = int(diaPrevisao['rain']['precipitation'])
        instanciaPrevisao.chuvaProbabilidade = int(diaPrevisao['rain']['probability'])
        instanciaPrevisao.temperaturaMaxima = int(diaPrevisao['temperature']['max'])
        instanciaPrevisao.temperaturaMinima = int(diaPrevisao['temperature']['min'])
        
        if novo:
            session.add(instanciaPrevisao)
        else:
            session.flush()
    


def getAnalise(dtInicio, dtFim, session):
    resposta = Resposta()
    dtInicio = dtInicio - timedelta(days=1)
    dtFim = dtFim + timedelta(days=1)

    try:
        query = session.query(PrevisaoModel).join(CidadeModel,CidadeModel.id == PrevisaoModel.idCidade).add_columns(CidadeModel.nome,PrevisaoModel.temperaturaMaxima)\
                                        .filter(PrevisaoModel.data<dtFim).filter(PrevisaoModel.data>dtInicio).order_by(desc(PrevisaoModel.temperaturaMaxima)).limit(1)
    except:
        resposta.status = False
        resposta.msg = 'Erro ao recuperar dados do banco'
        resposta.status_code = 500
        return resposta
    query = query.first()
    if query is None:
        resposta.status = False
        resposta.status_code = 200
        resposta.msg = 'Não existem dados para consulta no período'
        return resposta
    nomeCidade = query.nome
    temperatura = query.temperaturaMaxima
    try:
        query = session.query(PrevisaoModel).join(CidadeModel,CidadeModel.id == PrevisaoModel.idCidade).add_columns(CidadeModel.nome,func.avg(PrevisaoModel.chuvaPrecipitacao).label('media'))\
                                        .filter(PrevisaoModel.data<=dtFim).filter(PrevisaoModel.data>=dtInicio).group_by(CidadeModel.nome).order_by(CidadeModel.nome).all()

    except:
        resposta.status=False
        resposta.msg = 'Erro ao recuperar dados do banco'
        resposta.status_code = 500
        return resposta    
    medias = []
    for cidade in query:
        medias.append({'cidade': cidade.nome,'mediaPrecipitacao':"{0:.2f}".format(round(cidade.media,2))})
        

    resposta.dados = {'cidademaxtemp':nomeCidade,'temperatura':temperatura, 'medias': medias}
    
    return resposta
                              
    