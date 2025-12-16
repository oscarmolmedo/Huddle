from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

url = 'https://books.toscrape.com/'
head = {'User-Agent':'MiScraper/1.0 (oscaaraujo96@gmail.com)'}

respuesta = requests.get(url, headers=head, timeout=10)
respuesta.raise_for_status()
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Seleccionar los contenedores de cada libro
books = soup.select("ol.row article.product_pod")

lista_items = []

for book in books:
    # Extraer título y URL del producto
    link = book.select_one("h3 a")
    title = link["title"]
    product_url = urljoin(url, link["href"])

    # Extraer precio
    price_text = book.select_one("p.price_color").text
    _, value = price_text.split("£", 1)
    price_value = float(value)

    # ----- NUEVO: obtener categoría -----
    respuesta2 = requests.get(product_url, headers=head, timeout=10)
    soup2 = BeautifulSoup(respuesta2.text, 'html.parser')

    breadcrumb = soup2.select("ul.breadcrumb li a")
    categoria = breadcrumb[2].text.strip()  # el 3° <li> contiene la categoría

    # Guardar datos
    lista_items.append({
        "Titulo": title,
        "Precio": price_value,
        "Categoria": categoria
    })

print(lista_items[:3])
