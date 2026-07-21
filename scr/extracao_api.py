import pandas as pd
import requests # type: ignore

offset : int = 0
todos_registros : list = []

while offset < 10000:
    url = f'https://apidadosabertos.saude.gov.br/arboviroses/dengue?limit=100&offset={offset}'
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()  
        registros = dados['parametros']
        if registros == []:
            break
        todos_registros.extend(registros)
        print(f"Dados extraídos: {len(todos_registros)} registros... (Offset: {offset})")
    else:
        print('Erro ao consumir a API de Dengue')
        break

    offset += 20

df_dengue = pd.DataFrame(todos_registros)

url_ibge = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
response = requests.get(url_ibge)
dados_ibge = response.json()

lista_municipios = []
for m in dados_ibge:
    microrregiao = m.get('microrregiao') or {}
    mesorregiao = microrregiao.get('mesorregiao') or {}
    uf = mesorregiao.get('UF') or {}
    sigla_uf = uf.get('sigla', 'Ignorado')

    lista_municipios.append({
        'id': str(m.get('id', ''))[:6], 
        'municipio_nome': m.get('nome', 'Desconhecido'),
        'municipio_uf': sigla_uf
    })

df_ibge = pd.DataFrame(lista_municipios)

df_dengue.to_csv(r'..\data\dengue_2025.csv', index=False, encoding='utf-8')

df_ibge.to_csv(r'..\data\dim_ibge.csv', index=False, encoding='utf-8')

print("Ambas as bases foram exportadas separadamente com sucesso!")