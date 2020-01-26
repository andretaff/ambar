'''
Created on Jan 23, 2020

@author: Taffarello
'''

from models.cidadeModel import CidadeModel
from models import database

'''Retorna uma instância de cidade do banco. Caso não exista, armazena'''

def getCidade(id, dadosJSon,session):
    cidade = session.query(CidadeModel).get(id)
    if cidade is None:
        cidade = CidadeModel()
        cidade.nome = dadosJSon['name'].strip()
        cidade.estado = dadosJSon['state'].strip()
        cidade.pais = dadosJSon['country'].strip()
        cidade.id = id
        session.add(cidade)
    return cidade
    