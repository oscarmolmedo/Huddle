import os, sqlite3
from dia2 import *


os.system("cls")

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL ,
        precio REAL NOT NULL, 
        rating INTEGER NOT NULL,
        categoria_id TEXT NOT NULL
        
    )
""")




cursor.execute("""
    CREATE TABLE IF NOT EXISTS autores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
""")



cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros_autores (
        libro_id INTEGER NOT NULL,
        autor_id INTEGER NOT NULL,
        PRIMARY KEY (libro_id, autor_id),
        FOREIGN KEY (libro_id) REFERENCES libros(id),
        FOREIGN KEY (autor_id) REFERENCES autores(id)
    );
""")




conexion.commit()

url_categorias = obtener_categorias(url, cursor, conexion)

scrap_all_categories(url_categorias, cursor, conexion)







