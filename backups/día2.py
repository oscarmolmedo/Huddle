from requests.exceptions import RequestException
import requests, pandas as pd, os, time, sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urljoin


os.system("cls")

conexion = sqlite3.connect("books.db")
cursor = conexion.cursor()

url = 'https://books.toscrape.com/'
head = {
    'User-Agent':'MiSraper/1.0 (oscaaraujo96@gmail.com)'
}
session = requests.session()

###Realiza la conexión y get de forma segura y con reintentos
def safe_get (url, intentos=3, delay=2):
    for i in range(intentos):
        try:
            respuesta = session.get(url, headers=head, timeout=10)
            respuesta.raise_for_status()
            return respuesta
        except RequestException as e:
            print(f"Intento {i+1}] Error en {url}: {e}")
            time.sleep(delay)
    return None


###Se obtiene las categorias del sitio
###Realiza la conexión y get de forma segura y con reintentos
def safe_get (url, intentos=3, delay=2):
    for i in range(intentos):
        try:
            respuesta = session.get(url, headers=head, timeout=10)
            respuesta.raise_for_status()
            return respuesta
        except RequestException as e:
            print(f"Intento {i+1}] Error en {url}: {e}")
            time.sleep(delay)
    return None


###Se obtiene las categorias del sitio
def obtener_categorias (url_base):

    respuesta = safe_get(url_base)
    soup = BeautifulSoup(respuesta.text, "html.parser")
    list_category = soup.select_one("ul.nav")
    data_category = list_category.select("ul li a")

    url_categorias = {}
    for link in data_category[1:]:
        url_category = link["href"]
        url_categorias[link.get_text(strip=True)] = urljoin(url, url_category)
    
    return url_categorias


###Scrap de una categoría
def scrap_categorie (url_categoria, nombre_categoria, db_cursor):
    all_books = []
    
    while True:
        
        resp = safe_get(url_categoria)
        soup = BeautifulSoup(resp.text, "html.parser")
        libros = soup.select("article.product_pod")
        for libro in libros:
            id_libro = 0
            titulo = libro.select_one("h3 a")["title"]
            tipo_moneda ,value = libro.select_one("p.price_color").text.split("£", 1)
            precio = float(value)
            
            _, rating_get = libro.select_one("p.star-rating").get("class", [])
            rating_map = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
            rating = 0
            if rating_get in rating_map:
                rating += rating_map[rating_get]

            all_books.append({"titulo":titulo, "precio":precio, "puntuacion":rating, "categoria":nombre_categoria})
            db_cursor.execute("""
                INSERT INTO libros (name, precio, rating, categoria)
                VALUES (?,?,?,?)    
            """, (titulo, precio, rating, nombre_categoria))
        #buscar boton next
        next_tag = soup.select_one("li.next a")
        if next_tag:
            next_url = urljoin(url_categoria, next_tag["href"])
            url_categoria = next_url
            time.sleep(0.3)
        else:
            break
    return all_books

####Sracp de todas las categorías
def scrap_all_categories(url_categorias, db_cursor, db_conexion):
    for name,dir_categoria in url_categorias.items():
        scrap_categorie(dir_categoria,name, db_cursor)
        print(f"Categoria trabajada {name}")
        db_conexion.commit()

url_categorias = obtener_categorias(url)


print(url_categorias)
# scrap_all_categories(url_categorias)



