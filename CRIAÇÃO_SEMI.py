# SEMI ESTRUTURADO
# JSON

import pandas as pd

dados_json = {
    "Nome": ["Carlos", "Paula", "Marcelo", "Maria", "Vivian"],
    "Idade": [23, 35, 43, 33, 50],
    "Cidade": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Fortaleza"]
}

# CRIAR DATAFRAME (LINHAS E COLUNAS)
df_json = pd.DataFrame(dados_json)

# SALVAR EM JSON
df_json.to_json("dadosSemi.json", orient="records", lines=False)
