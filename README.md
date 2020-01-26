# ambar

Programa demonstração Ambar

Uso:
docker pull andretaff/ambar-forecast:latest
python ambar.py


http://localhost:5000/
Apresentação

***** /cidade?id=[idCidade]
Busca e armazena a previsão do tempo da cidade determinada

***** /analise?data_inicial=[dd/mm/yyyy]&data_final=[dd/mm/yyyy]
Retorna a cidade com maior temperatura máxima e as médias pluviométricas de todas as cidades no período

------------------------------------------------------------------------------------------------------------------------------

Estrutura de pastas:
- ambar           - pasta principal e bats de auxílio
  - source        - pasta com os fontes e bat de execução de testes
    - application - pasta com o webservice e controladores
    - models      - pasta com os modelos de dados e arquivo de acesso a banco
    - tests       - testes unitários
-----------------------------------------------------------------------------------------------------------------------------
Arquivos .bat:
- runtests.bat - executa todos os testes unitários
- runnormal.bat - roda o projeto na máquina local
- rebuild.bat - recria a imagem docker
- publicardocker - auto explicativo
- stop.bat - interrompe a execução da imagem docker

