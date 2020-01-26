'''
Created on Jan 21, 2020

@author: Taffarello
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

global Base
global Session
Base = declarative_base()
Session = sessionmaker()

