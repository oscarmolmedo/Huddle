from sqlalchemy import Column, Integer, String, Float
from database import Base                              #Se importa la clase Base que se creó.

#Definición de la tabla Product
class Inventario(Base):
    #Nombre de la tabla
    __tablename__ = "inventory"

    #Columnas de la tabla
    id =            Column(Integer, primary_key=True, index=True)
    product_id =    Column(Integer, unique=True, index=True)
    cantidad =      Column(Integer)