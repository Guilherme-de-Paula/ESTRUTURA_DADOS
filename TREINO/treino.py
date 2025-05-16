from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

caminho_driver = "C:\Program Files\chromedriver-win64\chromedriver.exe"  

servico = Service(caminho_driver)
controle = webdriver.ChromeOptions()
controle.add_argument('--disable-gpu')
controle.add_argument('window-size=1920,1080')


executor = webdriver.Chrome(service=servico, options=controle)
url_site = "https://masander.github.io/AlimenticiaLTDA-financeiro/"
executor.get(url_site)

time.sleep(3)

def extrair_tabela_html(driver):
    """Extrai dados da tabela visível na página atual."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabela = soup.find('table')
    if tabela:
        df = pd.read_html(str(tabela))[0]
        return df
    return None

try:
    print("\nColetando dados da página Orçamento...")
    df_orcamento = extrair_tabela_html(executor)
    if df_orcamento is not None:
        df_orcamento.to_excel("Orcamento.xlsx", index=False)
        print("Tabela de Orçamento salva com sucesso!")
    else:
        print("Não foi possível encontrar a tabela de Orçamento.")
except Exception as e:
    print("Erro ao extrair tabela de Orçamento:", e)


try:
    botao_proximo = WebDriverWait(executor, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[text()='Orçamentos']"))
    )
    executor.execute_script("arguments[0].click();", botao_proximo)
    print("\nIndo para a página Despesas...")
    time.sleep(3)

    df_despesas = extrair_tabela_html(executor)
    if df_despesas is not None:
        df_despesas.to_excel("Despesas.xlsx", index=False)
        print("Tabela de Despesas salva com sucesso!")
    else:
        print("Não foi possível encontrar a tabela de Despesas.")
except Exception as e:
    print("Erro ao extrair tabela de Despesas:", e)

executor.quit()

