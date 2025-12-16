import requests, pandas as pd, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

os.system("cls")

url = 'https://books.toscrape.com/'
head = {
    'User-Agent':'MiSraper/1.0 (oscaaraujo96@gmail.com)'
}

respuesta = requests.get(url, headers=head, timeout=10)
respuesta.raise_for_status()



#################################
soup = BeautifulSoup(respuesta.text, "html.parser")

first_page = soup.select_one("ol.row")
titulos = first_page.select("h3 a")
price_text = first_page.select("p.price_color")


lista_items = []

for t,p in zip (titulos,price_text):

    #Se obtiene categoría del libro
    product_url = urljoin(url, t['href'])
    respuesta2 = requests.get(product_url, headers=head, timeout=20)
    html2 = respuesta2.text
    soup2 = BeautifulSoup(html2, "html.parser")
    book_details = soup2.select("ul.breadcrumb li a")[2].text

    #Definiciones y formateo
    items = {}
    tipo_moneda ,value = p.text.split("£", 1)

    #Agregamos a diccionario
    items['Titulo'] =       t['title']
    items['Precio'] =       float(value)
    items['Categoria'] =    book_details


    lista_items.append(items)

print(lista_items)