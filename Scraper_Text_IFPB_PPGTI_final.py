import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página dos docentes
url = 'https://www.ifpb.edu.br/ppgti/programa/corpo-docente'

# Faz a requisição para a página
response = requests.get(url)

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Parseia o HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lista para armazenar os dados dos docentes
    dados_docentes = []

    # Encontra todos os elementos h4 que contêm os nomes dos docentes
    h4_elements = soup.find_all('h4')

    for h4 in h4_elements:
        # Inicializa dicionário de informações do docente
        info_docente = {
            'Nome': h4.get_text(strip=True),
            'Lattes': None,
            'E-mail': None,
            'Linha de Pesquisa': None
        }

        # Encontra o parágrafo que contém as informações de cada docente
        paragrafo = h4.find_next_sibling('p')

        if paragrafo:
            # Tenta encontrar o link para o Currículo Lattes
            link_lattes = paragrafo.find('a')
            if link_lattes and 'href' in link_lattes.attrs:
                info_docente['Lattes'] = link_lattes['href']

            # Tenta encontrar o e-mail
            if 'E-mail:' in paragrafo.text:
                try:
                    info_docente['E-mail'] = paragrafo.text.split('E-mail:')[1].split()[0].strip()
                except IndexError:
                    pass  # Em caso de estrutura inesperada, não armazenar e-mail

            # Tenta encontrar a Linha de Pesquisa
            span_linha_pesquisa = paragrafo.find('span')
            if span_linha_pesquisa:
                info_docente['Linha de Pesquisa'] = span_linha_pesquisa.get_text(strip=True)

        # Adiciona as informações coletadas na lista de docentes
        dados_docentes.append(info_docente)

    # Cria um DataFrame com os dados dos docentes
    df_docentes = pd.DataFrame(dados_docentes)

    # Exibe o DataFrame
    print(df_docentes)
else:
    print(f"Erro ao acessar a página: {response.status_code}")
