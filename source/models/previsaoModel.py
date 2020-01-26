'''
Created on Jan 22, 2020

@author: Taffarello
'''
from sqlalchemy import *
from models import database


class PrevisaoModel(database.Base):
    __tablename__ = "Previsao"
    id  = Column(Integer, primary_key=True)
    idCidade = Column(Integer,ForeignKey('Cidade.id'))
    data = Column(Date)
    chuvaPrecipitacao = Column(Integer)
    chuvaProbabilidade = Column(Integer)
    temperaturaMaxima = Column(Integer)
    temperaturaMinima = Column(Integer)
    
    