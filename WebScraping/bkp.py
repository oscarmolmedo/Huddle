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

##Para obtener la categoría seguimos otro enlace
category_url = first_page.select_one("h3 a")["href"]
product_url = urljoin(url, category_url)
respuesta2 = requests.get(product_url)
html2 = respuesta2.text
soup2 = BeautifulSoup(html2, "html.parser")
book_details = soup2.select("ul.breadcrumb")
print(book_details)



lista_items = []

for t,p in zip (titulos,price_text):
    items = {}

    title = t['title']
    tipo_moneda ,value = p.text.split("£", 1)
    price_value = float(value)

    items['Titulo'] = title
    items['Precio'] = price_value

    lista_items.append(items)

print(lista_items)

