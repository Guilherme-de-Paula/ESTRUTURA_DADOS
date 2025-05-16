# Importações
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
#python -m streamlit run ProjetoLoja.py

# Configurações & setup
st.set_page_config(page_title="Dashboard de Dengue", layout='wide')

df_tratados = pd.read_excel("dados_tratados.xlsx", sheet_name='TRATADOS')
df_residuo = pd.read_excel("dados_tratados.xlsx", sheet_name='RESIDUO')

st.title("Dashboard Casos e Suspeitas de Dengue em São Paulo")

# Pequenos tratamentos
df_tratados['DATA'] = pd.to_datetime(df_tratados['DATA'])
df_tratados['Mes'] = df_tratados['DATA'].dt.strftime('%b')
df_tratados['Ano'] = df_tratados['DATA'].dt.year

# Filtros por ano
st.write("Filtro por ano")
filtroAno = st.sidebar.multiselect(
    "Selecione o ano",
    options=df_tratados['Ano'].unique(),
    default=df_tratados['Ano'].unique(),
    key='Ano'
)

# Filtro por mês
st.write("Filtro por mês")
filtroMes = st.sidebar.multiselect(
    "Selecione o mês",
    options=df_tratados['Mes'].unique(),
    default=df_tratados['Mes'].unique(),
    key='Mes'
)

# Filtro por tipo de lixo
filtroLixo = st.sidebar.multiselect(
    "Selecione o tipo de lixo",
    options=df_tratados["Tipo de lixo"].unique(),
    default=df_tratados["Tipo de lixo"].unique(),
    key="lixo"
)
# municipios = st.sidebar.multiselect(
#     "Municípios",
#     options=df[""].unique(),
#     default=df[""].unique(),
#     key="municipio"

df_filtrado = df_tratados[
    df_tratados["Ano"].isin(filtroAno) &
    df_tratados["Mes"].isin(filtroMes) &
    df_tratados["Tipo de lixo"].isin(filtroLixo)
]
# DF filtrado
# df_filtrado = df[df['Ano'].isin(filtroAno) & df['Mes'].isin(filtroMes)]

st.write("Dados filtrados")
st.dataframe(df_filtrado)


# Cabeçalho
# def Cabecalho(df):
#     st.subheader("Relção da Dengue e a Limpa Brasil")
#     confimados = df["Casos Confirmados"].sum()
#     suspeita = df["Casos Suspeitos"].sum()
    
#     caso1, caso2 = st.columns(2)

#     with caso1:
#         st.metric("Casos Confirmados",value=int(confimados))
#     with caso2:
#         st.metric("Casos com Suspeita",value=int(suspeita))
#     st.markdown("---")

df_selecao = df.query()

def Cabecalho():
    st.subheader("Relção da Dengue e a Limpa Brasil")
    confimados = df["Casos Confirmados"].sum()
    suspeita = df["Casos Suspeitos"].sum()
    
    caso1, caso2 = st.columns(2)

    with caso1:
        st.metric("Casos Confirmados",value=int(confimados))
    with caso2:
        st.metric("Casos com Suspeita",value=int(suspeita))
    st.markdown("---")

# Gráficos
def Grafico(df_filtrado):
    grafico_barras = px.bar(
        df_filtrado,
        x="Meses de casos",
        y="lixo coletado",
        color="Tipo de lixo",
        barmode="group",
        title="Casos nos meses de maior coleta de lixo",
        labels={"Mes": "Mês", "Casos Confirmados": "Casos Confirmados", "Tipo de lixo": "Tipo de Lixo"}
)

    grafico_barras2 = px.bar(
        df_filtrado,
        x="Municípios",
        y="Casos por município",
        color="Ano",
        barmode="group",
        title="Número de casos por município",
        labels={"Município": "Município", "Casos Confirmados": "Casos Confirmados", "Ano": "Ano"}
)

    grafico_area = px.area(
        df_filtrado,
        x="Mes",
        y="Casos Confirmados",
        color="Ano",
        title="Evolução dos Casos Confirmados de Dengue por Mês",
        labels={"Mes": "Mês", "Casos Confirmados": "Casos Confirmados", "Ano": "Ano"}
        
)

grafico_1, grafico_2, grafico_3 = st.columns(2)
with grafico_1:
    st.plotly_chart(grafico_barras)

with grafico_2:
    st.plotly_chart(grafico_barras2)

with grafico_3:
    st.plotly_chart(grafico_area)

def sidebar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title= "Menu",
            options=["Cabecalho", "Grafico"],
            icons=["house", "bar-chart"],
            default_index= 0
        )

    if selecionado == "Cabecalho":
        Cabecalho(df_filtrado)
        #Grafico()
    elif selecionado == "Grafico":
        Grafico(df_filtrado)

sidebar()