# pip install selenium

# módulo para controlar o navegador web
from selenium import webdriver # simula o navegador

# localizador de elementos
from selenium.webdriver.common.by import By 

# serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avançadas (o mover do mouse, clique/arrasta, etc)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera  de forma explicita até que uma condição seja satisfeita (ex: que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

# condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec # tempo de espera para realizar a raspagem sem que aja encavalamento

# trabalhar com dataframe
import pandas as pd

# uso de funções relacionadas ao tempo
import time

# uso de tratamento de exceção
from selenium.common.exceptions import TimeoutException

# definir o caminho do chromedriver
chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

# configuração do WebDriver -   PADRÃO EM RELAÇÃO AS CONFIGURAÇÕES DO WEBDRIVER
                # caminho do navegador
servico = Service(chrome_driver_path) # Inicializar o navegador controlado pelo selenium
controle = webdriver.ChromeOptions() # configurar as opções do navegador 
#controle.add_argument("--headless") # executa o navegador sem abrir a interação
controle.add_argument("--disable-gpu") # evita possíveis erros gráficos
controle.add_argument("--window-size=1920,1080") # define uma resolução fixa, tamanho da tela

# inicialização do WebDriver
executador = webdriver.Chrome(service=servico, options=controle)

# URL inical
url_site = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"
executador.get(url_site)
time.sleep(5) # aguarda 5 segundo para garantir que a pág carregue

# criar um dicionario vazio para armazenar os marcas e preços das cadeiras
dic_produtos = {"marca":[],"preco":[]}

# vamos iniciar na pagina 1 e incrementamos a cada troca de pagina
pagina = 1


# PERCORRER O CODIGO 
while True: # enquanto ouver paginas vai ficar armazenando
    print(f"\n Coletando dados da pagina {pagina}...")

    try:
    # WebDriverWait(driver,10): cria uma espera de até 10 seg
    # until(...): faz com que o codigo espere até que a condição seja verdadeira
    # ec.presence_of_all_elements_located(..): verifica se todos os elementos "productCard" estão acessíveis
    # By.CLASS_NAME,"productCard"
        WebDriverWait(executador,10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard"))
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")

    # busca dos elementos encontrados
    produtos = executador.find_elements(By.CLASS_NAME,"productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{nome} - {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)

        except Exception:
            print("Erro ao coletar dados:", Exception)


# ENCONTRAR BOTÃO DA PROXIMA PÁGINA 
    try:
        # ENCONTRAR O ELEMENTO
        botao_proximo = WebDriverWait(executador, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            executador.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            # CLICAR NO BOTÃO
            executador.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a pagina {pagina}")
            pagina += 1
            time.sleep(5)
        
        else:
            print("Você chegou na ultima pagina!")
            break

    except Exception as e:
        print("Erro ao tentar avançar para a próxima página", e)
        break

# FECHAR O NAVEGADOR
executador.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel("Cadeiras.xlsx", index=False)

print(f"Arquivo 'cadeiras' salvo com sucesso! ({len(df)} produtos capturados!)")

# encontrar o acesso para a proxima pagina
# fechar o navegador
# dataframe
# salvar os dados em csv

