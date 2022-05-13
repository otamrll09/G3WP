import pandas as pd

# Monta o cabeçalho da planilha
cabecalho_excel = ['Software/Sistema', 'CVE', 'Descrição', 'Severidade', 
                    'Referências para recomendações, soluções e ferramentas',
                    'Configurações de softwares afetadas', 'Data de publicação NVD', 'Link CVE']

# Recebe os dados obtidos via bot webscrapping
textos_site = [['Texto1', 'Texto1', 'Texto1', '8.8 a', 'Texto1', 'Texto1', 'Texto1', 'Texto1'],
               ['Texto2', 'Texto2', 'Texto2', '7.4 b', 'Texto2', 'Texto2', 'Texto2', 'Texto2'],
               ['Texto3', 'Texto3', 'Texto3', '8.5 c', 'Texto3', 'Texto3', 'Texto3', 'Texto3'],
               ['Texto4', 'Texto4', 'Texto4', '5.6 d', 'Texto4', 'Texto4', 'Texto4', 'Texto4'],
               ['Texto5', 'Texto5', 'Texto5', '2.1 e', 'Texto5', 'Texto5', 'Texto5', 'Texto5'],
               ['Texto6', 'Texto6', 'Texto6', '9.5 f', 'Texto6', 'Texto6', 'Texto6', 'Texto6'],]

# Salva os dados em uma planilha do excel
df = pd.DataFrame(textos_site,columns=cabecalho_excel, index=None)

dicionario_dados_obtidos = df.to_dict()
print(dicionario_dados_obtidos['Severidade'])

# df = df[df['Severity']>=7] #selecionando apenas os com severidade grave (que é os maiores q 7)

# print(dicionario_dados_obtidos[df'Severidade'])
