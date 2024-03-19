from bs4 import BeautifulSoup
import pandas as pd

#iMPLEMENTAÇÃO NO HTML LOCAL
# Definindo o caminho para o arquivo HTML que contém as informações que desejamos extrair.
caminho_arquivo = 'ifpb.html'

# Abrindo e lendo o conteúdo do arquivo HTML especificado.
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    conteudo_html = arquivo.read()

#IMPLEMENTAÇÃO NA PÁGINA WEB---------------------------------------
## URL da página dos docentes
#url = 'https://www.ifpb.edu.br/ppgti/programa/corpo-docente'

# Faz a requisição para a página
#response = requests.get(url)

# Verifica se a requisição foi bem sucedida
#if response.status_code == 200:
    # Parseia o HTML da página
#    soup = BeautifulSoup(response.text, 'html.parser')
#------------------------------------------------------------------

    
# Utilizando a biblioteca BeautifulSoup para interpretar (parsear) o conteúdo HTML lido do arquivo.
sopa = BeautifulSoup(conteudo_html, 'html.parser')

# Preparando uma lista vazia para armazenar os dados corrigidos dos docentes.
dados_docentes_final = []

# Procurando todos os elementos 'h4' no conteúdo HTML, que geralmente contêm os nomes dos docentes.
elementos_h4 = sopa.find_all('h4')
for h4 in elementos_h4:
    # Extraindo o texto de cada elemento 'h4', que corresponde ao nome do docente.
    nome_docente = h4.get_text(strip=True)
    
    # Verificando se o texto extraído não está vazio antes de continuar.
    if nome_docente:
        # Criando um dicionário para guardar os dados do docente atual.
        dados_docente = {
            'Nome do Docente do PPGTI IFPB': nome_docente, 
            'Lattes': '', 
            'Email': '', 
            'Linha de Pesquisa': ''
        }
        
        # Buscando o elemento 'p' que vem imediatamente após o 'h4', contendo informações adicionais.
        elemento_p = h4.find_next_sibling('p')
        if elemento_p:
            # Tentando encontrar um link dentro do 'p', o qual contém a URL do currículo Lattes.
            link_lattes = elemento_p.find('a', href=True)
            if link_lattes and 'lattes' in link_lattes['href']:
                dados_docente['Lattes'] = link_lattes['href']

            # Extraindo a linha de pesquisa do texto do 'p', removendo a parte que não é necessária.
            texto_linha_pesquisa = elemento_p.text.split('Currículo Lattes:')[0]
            texto_linha_pesquisa = texto_linha_pesquisa.replace('Linha de Pesquisa:', '').strip()
            dados_docente['Linha de Pesquisa'] = texto_linha_pesquisa

            # Buscando pelo e-mail, que pode estar em um link mailto ou no texto do 'p'.
            link_email = elemento_p.find('a', href=lambda href: href and 'mailto:' in href)
            if link_email:
                dados_docente['Email'] = link_email['href'].split(':')[1]
            elif 'E-mail:' in elemento_p.text:
                texto_email = elemento_p.text.split('E-mail:')[1].split()[0].strip()
                dados_docente['Email'] = texto_email

        # Adicionando o dicionário com os dados do docente à lista de docentes corrigidos.
        dados_docentes_final.append(dados_docente)

# Convertendo a lista de dicionários em um DataFrame do pandas para melhor manipulação e visualização dos dados.
df_dados_docentes_final = pd.DataFrame(dados_docentes_final)

# Especificando o caminho para salvar o DataFrame como um arquivo CSV.
caminho_csv = 'docentes.csv'

# Salvando o DataFrame em um arquivo CSV, garantindo que a codificação seja 'utf-8-sig' para máxima compatibilidade.
df_dados_docentes_final.to_csv(caminho_csv, index=False, encoding='utf-8-sig')

# Imprimindo o DataFrame para verificar se os dados foram extraídos e organizados corretamente.
print(df_dados_docentes_final)
