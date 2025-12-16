import requests, pandas as pd, os, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

os.system("cls")

url = 'https://books.toscrape.com/'
head = {
    'User-Agent':'MiSraper/1.0 (oscaaraujo96@gmail.com)'
}

print("Obteniendo libros")
respuesta = requests.get(url, headers=head, timeout=10)
respuesta.raise_for_status()

#################################

soup = BeautifulSoup(respuesta.text, "html.parser")
first_page = soup.select_one("ol.row")
titulos_enlace = first_page.select("h3 a")

lista_items = []
enlaces_libros = []

for t in titulos_enlace:

    #Se obtiene categoría del libro
    product_url = urljoin(url, t['href'])
    enlaces_libros.append(product_url)
print(f"Se encontraron un total de {len(enlaces_libros)} libros")

print("Obteniendo detalles de libros")
session2 = requests.Session()
session2.headers.update(head)

for link in enlaces_libros:


    respuesta2 = session2.get(link, timeout=20)
    time.sleep(0.5)
    html2 = respuesta2.text
    soup2 = BeautifulSoup(html2, "html.parser")

    #Definiciones y formateo
    items = {}
    book_details = soup2.select("ul.breadcrumb li a")[2].text
    precio_raw = soup2.select_one("p.price_color").get_text(strip=True)
    print(precio_raw)
    precio = float(precio_raw.replace("£", ""))
    print(precio)

    titulos = soup2.select_one("h1 ").text    

    #Agregamos a diccionario
    items['Titulo'] =       titulos
    items['Precio'] =       float(precio)
    items['Categoria'] =    book_details


    lista_items.append(items)

print(lista_items)