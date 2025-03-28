# DADOS ESTRUTURADO - CRIAÇÃO
# EXCEL
# pip install pandas (instalação da biblioteca)
# pip install openpyxl (instalação da biblioteca do Excel)


import pandas as pd

# ESTRUTURA DE DICIONÁRIO
dados_planilha1 = {
    "Nome": ["Carlos", "Paula", "Marcelo", "Maria", "Vivian"],
    "Idade": [23, 35, 43, 33, 50],
    "Cidade": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Fortaleza"]
}
# CRIA UM DATAFRAME (LINHAS E COLUNAS)
df_planilha1 = pd.DataFrame(dados_planilha1)

# SALVAR NO EXCEL
with pd.ExcelWriter("dadosEstruturados.xlsx") as writer:
    df_planilha1.to_excel(writer, sheet_name="Planilha1", index=False)

