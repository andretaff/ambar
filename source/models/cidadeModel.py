from sqlalchemy import *
from models import database
from sqlalchemy.orm import relationship

class CidadeModel(database.Base):
    __tablename__ = "Cidade"
    id  = Column(Integer, primary_key=True)
    estado = Column(String)
    pais = Column(String)
    nome = Column(String)
    
    previsao = relationship('PrevisaoModel')