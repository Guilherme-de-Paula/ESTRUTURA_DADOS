import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações Iniciais
st.set_page_config(page_title = "Dashboard de Vendas", page_icon="", layout="wide")

# Carregar os dados
df = pd.read_excel("Vendas.xlsx")

# Qualquer modificação na página, usar o streamlit

# Filtros
# Sidebar
st.sidebar.header("Selecione os filtros")

# Filtro por Loja
lojas = st.sidebar.multiselect(
    "Lojas", # Label, Titulo
    # Opções do filtro
    options = df["ID Loja"].unique(),
    # Opção que vem por padrão no filtro
    default = df["ID Loja"].unique(),
    # Chave unica
    key = "loja"
)

# Filtro do Produto
produtos = st.sidebar.multiselect(
    "Produtos",
    options = df["Produto"].unique(),
    default = df["Produto"].unique(),
    key = "produto"
)

# Filtrar o DataFrame de acordo com as opções selecionadas
df_selecao = df.query("`ID Loja` in @lojas and Produto in @produtos") # Verifica os filtros aplicados

# Gráficos e na função da página
def Home():
    st.title("Faturamento das Lojas")

    total_vendas = df["Quantidade"].sum()
    media = df["Quantidade"].mean()
    mediana = df["Quantidade"].median()

    total1, total2, total3 = st.columns(3) # Trabalhando com colunas ou paginações
    with total1:
        # Apresentar indicadores rápidos
        st.metric("Total Vendido", value = int(total_vendas))

    with total2:
        st.metric("Média por Produto", value = f"{media:.1f}")

    with total3:
        st.metric("Mediana", value = int(mediana))

    st.markdown("---")

def Graficos():
        # Criar um gráfico de barras, mostrando a quantidade de produtos por loja
        fig_barras = px.bar(
            df_selecao,
            x = "Produto",
            y = "Quantidade",
            color = "ID Loja",
            barmode = "group", 
            title = "Quantidade de Produtos Vendidos por Loja"
        )

        # Grafico de linha, com o total de vendas por loja
        fig_linhas = px.line(
            df_selecao.groupby(["ID Loja"]).sum(numeric_only = True).reset_index(), # não é necessário ter alteração
            x = "ID Loja",
            y = "Quantidade",
            title = "Total de Vendas por Loja"
        )

        grafi1, grafi2 = st.columns(2)
        with grafi1:
            st.plotly_chart(fig_barras, use_container_width = True)

        with grafi2:
            st.plotly_chart(fig_linhas, use_container_width = True)

def sideBar():
        with st.sidebar:
            selecionado = option_menu(
                menu_title = "Menu",
                options = ["Home", "Gráficos"],
                icons = ["house", "bar-chart"],
                default_index = 0

            )

        if selecionado == "Home":
            Home()
            Graficos()
        elif selecionado == "Gráficos":
            Graficos()
    
sideBar()


