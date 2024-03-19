import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página dos docentes
url = 'https://www.ifpb.edu.br/ppgti/programa/corpo-docente'

# Faz a requisição para a página
response = requests.get(url)

# Parseia o HTML da página se a resposta for bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra todos os elementos h4 que contêm os nomes dos docentes
    h4_elements = soup.find_all('h4')

    # Extrai o texto de cada elemento h4
    names = [h4.get_text(strip=True) for h4 in h4_elements]

    # Cria um DataFrame com os nomes dos docentes
    df = pd.DataFrame(names, columns=['Nome'])

    # Aqui você pode salvar o DataFrame em um arquivo CSV, exibir ou fazer o que precisar com ele
    print(df)
else:
    print(f"Erro ao acessar a página: {response.status_code}")
