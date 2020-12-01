# 1. Importar as bibliotecas ---------------------------------------------------------------------------
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import json

# 2. Extrair o conteúdo HTML a partir da URL -----------------------------------------------------------
url_busca_uf = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
ufs = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

for uf in ufs:
    payload = {'UF' : uf}
    pagina = requests.post(url_busca_uf, payload)

    # 3. Parsear o conteúdo HTML utilizando a biblioteca BeautifulSoup ---------------------------------
    soup = bs(pagina.text, 'html.parser')

    # 4. Estruturar o conteúdo em um Data Frame utilizando a biblioteca Pandas -------------------------
    table_estados = soup.find_all(name='table')[0]
    df_estados= pd.read_html(str(table_estados))[0]
    df_estados_salvar = df_estados[['UF', 'Faixa de CEP']]

    table_localidades = soup.find_all(name='table')[1]
    df_localidades = pd.read_html(str(table_localidades))[0]
    df_localidades_salvar = df_localidades[['Localidade', 'Faixa de CEP', 'Situação', 'Tipo de Faixa']]

    # 5. Trasnformar os dados em um dicionário de dados próprio ----------------------------------------
    dict_estados_salvar = {}
    dict_estados_salvar['Estados'] = df_estados_salvar.to_dict('records')

    dict_localidades_salvar = {}
    dict_localidades_salvar['Localidades'] = df_localidades_salvar.to_dict('records')

    # 6. Converter e salvar em um arquivo JSON ---------------------------------------------------------
    dict_estados_salvar = json.dumps(dict_estados_salvar, sort_keys=False, indent=3)
    try:
        arquivo_json = open("dados_estados" + uf + ".json", "w")
        arquivo_json.write(dict_estados_salvar)
        arquivo_json.close()
    except Exception as erro:
        print("Ocorreu um erro ao carregaar o arquivo.")
        print("O erro é: {}".format(erro))


    dict_localidades_salvar = json.dumps(dict_localidades_salvar, sort_keys=False, indent=3)
    try:
        arquivo_json = open("dados_localidades" + uf + ".json", "w")
        arquivo_json.write(dict_localidades_salvar)
        arquivo_json.close()
    except Exception as erro:
        print("Ocorreu um erro ao carregaar o arquivo.")
        print("O erro é: {}".format(erro))
    
    time.sleep(3)