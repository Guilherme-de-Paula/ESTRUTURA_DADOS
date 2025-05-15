import requests
from bs4 import BeautifulSoup
import pandas as pd


# URL do site a ser acessado
url = "http://books.toscrape.com/"

# Fazer a requisição HTTP
response = requests.get(url)

# Certificar que o conteúdo seja interpretado com o padrão utf-8
response.encoding = "utf-8"

# Criar um objeto Beatifulsoup para analisar o HTML
soup = BeautifulSoup(response.text, "html.parser")

# Criar uma lista para armazenar os dados
books_data = []

# Encontrar os elementos que contêm a tag com a classe product_pod
books = soup.find_all("article", class_= "product_pod")
#                      tag/html   css
for book in books:
    title = book.h3.a.attrs["title"]
    price = book.find("p", class_="price_color").text
    books_data.append([title, price])

df = pd.DataFrame(books_data, columns=["Titulo", "Preço"])

df.to_excel("Livros.xlsx", index=False) # criação de arquivo csv
print("Dados salvos no arquivo Livros.xlsx com sucesso")