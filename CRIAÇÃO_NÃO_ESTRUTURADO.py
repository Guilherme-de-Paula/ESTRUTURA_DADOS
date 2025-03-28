# DADOS NÃO ESTRUTURADOS - CRIAÇÃO
# CSV

import pandas as pd

dados_csv = {
    "Nome": ["Carlos", "Paula", "Marcelo", "Maria", "Vivian"],
    "Idade": [23, 35, 43, 33, 50],
    "Cidade": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Fortaleza"]
}

# CRIAR O DATAFRAME (LINHAS E COLUNAS)
df_csv = pd.DataFrame(dados_csv)

# SALVAR EM CSV
df_csv.to_csv("dadosNao.csv", index=False)