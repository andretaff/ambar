'''
Created on Jan 25, 2020

@author: Taffarello
'''
import json


class Resposta:
    status=True
    status_code = 200
    msg = 'Ok'
    dados = {}
    
    def gerarResposta(self):
        return json.dumps({'status' : self.status, 'mensagem':self.msg, 'dados' : self.dados}),self.status_code