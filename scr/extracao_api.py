import pandas as pd
import requests # type: ignore

offset : int = 0

todos_registros : list = []

while offset < 5000:
    url = f'https://apidadosabertos.saude.gov.br/arboviroses/dengue?nu_ano=2025&limit=20&offset={offset}'
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()  
        registros = dados['parametros']
        if registros == []:
            break
        todos_registros.extend(registros)
        print(f"Dados extraídos: {len(todos_registros)} registros... (Offset: {offset})")
    else:
        print('Erro ao consumir a API')
        break

    offset += 20

df = pd.DataFrame(todos_registros)
df.to_csv('D:\Arquivos de usuarios\Desktop\dados\Projeto-Dengue\data\dengue_2025.csv', index=False, encoding='utf-8')