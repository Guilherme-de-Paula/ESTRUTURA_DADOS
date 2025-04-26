
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException
import re

chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

servico = Service(chrome_driver_path) 
controle = webdriver.ChromeOptions() 
controle.add_argument("--disable-gpu") 
controle.add_argument("--window-size=1920,1080") 

drive = webdriver.Chrome(service=servico, options=controle)

url_site = "https://www.kabum.com.br/perifericos/headset-gamer/sem-fio"
drive.get(url_site)
time.sleep(5) 

dic_produtos = {"titulo":[],"preco":[], "Preco Original":[], "Recurso":[], "Marcas":[]}

pagina = 1

while True: 
    print(f"\n Coletando dados da pagina {pagina}...")

    try:
        WebDriverWait(drive,10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard"))
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")
        break

    produtos = drive.find_elements(By.CLASS_NAME,"productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco_str = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()
            preco_abaixo = float(preco_str.replace("R$", "").replace(".", "").replace(",", ".").strip()) 
            original_str = produto.find_element(By.CLASS_NAME, "oldPriceCard").text.strip()
            original = float(original_str.replace("R$", "").replace(".", "").replace(",", ".").strip()) 

            recurso = re.search(r'(Dolby)', nome, re.IGNORECASE)
            marca = re.search(r' (Astro) | (Astro Gaming) | (Corsair) | (Fallen) | (Force One) | (Havit) | (Hyperx) | (JABRA) | (JBL) | (Lenovo) | (Logitech) | (Logitech G) | (Outros) | (QCY) | (Razer) | (Redragon) | (Sony) | (Steelseries)', nome, re.IGNORECASE )

            recurso = recurso.group(0).capitalize() if recurso else 'Não apresenta esse recurso'  
            marca = marca.group(0).upper()  if marca else 'Marca não encontrada'     
            
            if preco_abaixo > 0:

                print(f"{nome} - {preco_str} - {original} - {recurso} - {marca}") 

                dic_produtos["titulo"].append(nome)
                dic_produtos["preco"].append(preco_abaixo)
                dic_produtos["Preco Original"].append(original)
                dic_produtos["Recurso"].append(recurso)
                dic_produtos["Marcas"].append(marca)

        except Exception:
            
            print("Erro ao coletar dados:", Exception)

    try:
        botao_proximo = WebDriverWait(drive, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            drive.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            drive.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a pagina {pagina}")
            pagina += 1
            time.sleep(5)
        
        else:
            print("Você chegou na ultima pagina!")
            break

    except Exception as e:
        print("Erro ao tentar avançar para a próxima página", e)
        break

drive.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel("Headsets.xlsx", index=False)

print(f"Arquivo 'Headsets' salvo com sucesso! ({len(df)} produtos capturados!)")