from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
'''Instancia Logger'''
from logger_config import configurar_logger
logger = configurar_logger('PRODUCTOS-SERVICE')

'''Instancia de FastApi'''
app = FastAPI(title='Microservicio de Productos')

'''Base de Datos'''
#Se importa herramientas que creamos
import models, schemas                  #Modelos de DB y esquemas de pydantic
from database import engine, get_db     #Conexion a DB y dependencia
#Creamos las tablas en la DB
models.Base.metadata.create_all(bind=engine)

'''Circuit Breaker'''
from circuit_breaker import get_inventory_quantity, CircuitBreakerError


'''----ENDPOINTS----'''
#CONSULTAR PRODUCTO por ID (GET /products/{product_id})
@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no se encuentra")

    try:
        stock_actual = await get_inventory_quantity(product_id)
        
    # 1. EL CIRCUITO ESTÁ ABIERTO (OPEN)
    except CircuitBreakerError:
        # A partir del 6to intento, esto se dispara INSTANTÁNEAMENTE sin hacer la llamada.
        logger.error(f"✅ Circuit Breaker ABIERTO (OPEN). Evitando llamada al servicio de Inventario.")
        raise HTTPException(status_code=503, detail="Servicio de Inventario no disponible (Circuit Breaker Abierto)")
    
    # 2. FALLO DE CONEXIÓN MIENTRAS SE CUENTA (CLOSED o HALF-OPEN)
    except httpx.RequestError as e:
        # Estos son los fallos 1, 2, 3, 4, 5. El CB aún está en estado CLOSED o HALF-OPEN.
        # El CB registra el fallo y lanza la excepción original (RequestError) al endpoint.
        logger.warning(f"⚠️ Fallo de conexión (CB contando): {type(e).__name__}: {e}")
        raise HTTPException(status_code=503, detail="Servicio de Inventario no disponible (Fallo de conexión)")
        
    # 3. ERROR LÓGICO DE SERVIDOR (5xx) EXCLUIDO
    except httpx.HTTPStatusError as e:
        # Esto ocurre si el Inventario devuelve 5xx. El CB lo ignora (exclude) y se propaga al endpoint.
        raise HTTPException(status_code=503, detail="Servicio de Inventario fallando internamente (Error 5xx)")


    product_data = schemas.Product.from_orm(db_product).model_dump()
    product_data['stock'] = stock_actual
    logger.info(f'Se consulto exitosamente {product_data} ')
    return product_data

#CREAR PRODUCTO (POST '/products')
@app.post("/products/", response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db:Session = Depends(get_db)):
    
    #Mapear el esquema Pydantic a un objeto SQLAlchemy Model
    db_product = models.Product(**product.model_dump())

    #Agregar el objeto a la sesion
    db.add(db_product)
    #Para guardar
    db.commit()
    #Recargar el objeto para obtener el ID generado por la DB
    db.refresh(db_product)

    #Devolver el objeto creado
    logger.info(f'Se agrego {db_product} exitosamente a la DB')
    return db_product

#ACTUALIZAR PRODUCTO por ID (PUT /products/{id})
@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id : int, product: schemas.ProductCreate, db:Session = Depends(get_db)):
    
    #Buscar producto
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    #Si no encuentra producto
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no se encuentra")


    #Actualizar producto obtenido
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock = product.stock

    #Para guardar
    db.commit()
    #Recargar el objeto para obtener el ID generado por la DB
    db.refresh(db_product)

    logger.info(f'Se actualizo exitosamente el producto {db_product}')
    return db_product

#ELIMINAR PRODUCTO por ID (DELETE /products/{id})
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id : int, db:Session = Depends(get_db)):
    
    #Buscar producto
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    #Si no encuentra producto
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Producto con ID {product_id} no se encuentra")
    
    #Eliminamos el registro
    if db.delete(db_product):
        logger.warning(f'Se elimino el producto {db_product}')
    #Para guardar
    db.commit()

    #retornamos vacío | fastapi devuelve 204
    return