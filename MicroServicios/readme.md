---Especificaciones para ejecutar servicios----
rgba(30, 114, 210, 0.67) cada archivo main esta en su respectiva carpeta
#Orders-Service
uvicorn main:app --reload --port 8002

#Products-Service
-uvicorn main:app --reload --port 8000

#Inventory-Service
uvicorn main:app --reload --port 8001


ODERS       #Nivel mas alto
    ⬇️
PRODUCTS
    ⬇️
INVENTARIO  #Nivel mas bajo