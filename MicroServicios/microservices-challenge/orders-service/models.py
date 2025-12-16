from sqlalchemy import Column, Integer, String, Float
from database import Base                              #Se importa la clase Base que se creó.

#Definición de la tabla Product
class Orders(Base):
    #Nombre de la tabla
    __tablename__ = "orders"

    #Columnas de la tabla
    id =            Column(Integer, primary_key=True, index=True)
    product_id =    Column(Integer, index=True)
    cantidad =      Column(Integer)
    estado =        Column(String, default='PENDIENTE')