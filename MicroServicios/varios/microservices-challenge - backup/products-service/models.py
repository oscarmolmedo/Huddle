from sqlalchemy import Column, Integer, String, Float
from database import Base                              #Se importa la clase Base que se creó.

#Definición de la tabla Product
class Product(Base):
    #Nombre de la tabla
    __tablename__ = "products"

    #Columnas de la tabla
    id =            Column(Integer, primary_key=True, index=True)
    name =          Column(String, index=True)
    description =    Column(String)
    price =         Column(Float)
    stock =         Column(Integer)                                 #tabla temporal, se maneja desde inventario