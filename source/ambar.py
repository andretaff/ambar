from flask import Flask, url_for,abort,request
from models import database
from sqlalchemy import create_engine
from application import webservice, resposta
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


@app.route('/')
def index():
    return "Hello World!<br>"+  \
            "serviços disponíveis: <br>"+ \
            "***** /cidade?id=[idCidade]<br> "+\
            " Busca e armazena a previsão do tempo da cidade determinada <br><br><br>" +\
            "***** /analise?data_inicial=[dd/mm/yyyy]&data_final=[dd/mm/yyyy]<br> "+\
            " Retorna a cidade com maior temperatura máxima e as médias pluviométricas de todas as cidades no período "            
                  
                  

@app.route('/cidade')
def getPrevisaoCidade():
    retorno = resposta.Resposta()
    try:
        idCidade = request.args.get('id',None)
        idCidade = int(idCidade)
    except:
        retorno.status=False
        retorno.msg = 'Parâmetros idCidade deve ser numérico'
        retorno.status_code = 400
        return retorno.gerarResposta()        
            
    retorno = webservice.getPrevisaoCidade(idCidade)
    return retorno.gerarResposta()

        
    
@app.route('/analise')        
def getAnalise():
    retorno = resposta.Resposta()
    try:
        dtInicio = request.args.get('data_inicial',None)
        dtFim = request.args.get('data_final',None)
        dtInicio = datetime.strptime(dtInicio,'%d/%m/%Y')
        dtFim = datetime.strptime(dtFim,'%d/%m/%Y')
    except:
        retorno.status=False
        retorno.msg = 'Parâmetros data_inicial e data_final devem estar no formato dd/mm/yyyy'
        retorno.status_code = 400
        return retorno.gerarResposta()
    
    if dtInicio>dtFim:
        retorno.status = False
        retorno.msg = 'Data final não pode ser maior que a data inicial'
        retorno.status_code = 400
        return retorno.gerarResposta()
        
    retorno = webservice.getAnalise(dtInicio,dtFim)
    return retorno.gerarResposta()
        
    
            
        

if __name__ == '__main__':
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    database.Base.metadata.create_all(engine)
    database.Session.configure(bind=engine)
    app.run(host='0.0.0.0',debug=False)