import requests #È a biblioteca em python mais popular para interagir com APIs web 
import pandas as pd # Biblioteca necessária para carregar os dados no formato dataframe

def listar_cidades_amapa():
    
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/16/municipios" # URL da API do IBGE para obter os municípios por estado (código do Amapá é 16)

    try:
        
        response = requests.get(url)# Faz a requisição GET para a API do IBGE

        
        if response.status_code == 200:# Verifica se a requisição foi bem sucedida (código 200)
            
            cidades_json = response.json()# Carrega o JSON retornado pela API
            
            lista_cidades = [cidade['nome'] for cidade in cidades_json]# Cria uma lista com os nomes das cidades

            df_cidades = pd.DataFrame(lista_cidades, columns=['Cidades']) # Cria um DataFrame com a lista de cidades

            print(df_cidades)# Exibe o DataFrame no terminal
        else:
            print(f"Erro ao acessar a API do IBGE: Código {response.status_code}")#Notifica se houve erro ao acessar a API
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")#Notifica se houve erro no pedido de informação para a API

listar_cidades_amapa()# Chama a função