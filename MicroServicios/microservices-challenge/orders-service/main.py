from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
'''Instancia Logger'''
from logger_config import configurar_logger
logger = configurar_logger('PEDIDOS-SERVICE')

'''Instancia de FastApi'''
app = FastAPI(title='Microservicio de Pedidos')

'''TOKEN'''
token = 'token_123@_products_to_orders'

'''Base de Datos'''
#Se importa herramientas que creamos
import models, schemas                  #Modelos de DB y esquemas de pydantic
from database import engine, get_db     #Conexion a DB y dependencia
#Creamos las tablas en la DB
models.Base.metadata.create_all(bind=engine)

'''Circuit Breaker'''
#call_external_service implementado con CB devuelve cuerpo json del servicio en cuestión.
#Debemos de filtrar la respuesta.
from circuit_breaker import call_external_service, CircuitBreakerError


  

'''----ENDPOINTS----'''
#Obtiene datos de products-service y guarda en DB local
@app.post("/orders/", response_model=schemas.OrderBase, status_code=201)
async def create_order(order_data: schemas.OrderBase, db: Session = Depends(get_db)):
    product_id = order_data.product_id
    quantity = order_data.cantidad

    logger.info(f"Iniciando creación de pedido para Producto {product_id} x {quantity}")

    # --- 1. VERIFICAR PRODUCTO (Llamada a Products Service) ---
    try:
        # Llama a la función genérica
        PRODUCTS_SERVICE_URL = f'http://127.0.0.1:8000/products/{product_id}'
        product_info = await call_external_service(PRODUCTS_SERVICE_URL, 'PRODUCTS-SERVICE', token)
        logger.info(f"Producto  verificado{product_info}")

        if product_info:
            # 3.1. Crear el objeto de la DB
            db_order = models.Orders(
                product_id=product_id, 
                cantidad=quantity
            )

            # 3.2. Guardar en la DB
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            
            logger.info(f"Pedido {db_order.id} creado con éxito.")

            return db_order
        else:
            raise HTTPException(status_code=404, detail='Id Producto no existe en Products-Service')


    # 1. EL CIRCUITO ESTÁ ABIERTO (OPEN)
    except CircuitBreakerError:
        # A partir del tercer intento, esto se dispara INSTANTÁNEAMENTE sin hacer la llamada.
        logger.error(f"✅ Circuit Breaker ABIERTO (OPEN). Evitando llamada al servicio de Productos.")
        raise HTTPException(status_code=503, detail="Servicio de Productos no disponible (Circuit Breaker Abierto)")
    
    # 2. FALLO DE CONEXIÓN MIENTRAS SE CUENTA (CLOSED o HALF-OPEN)
    except httpx.RequestError as e:
        # Estos son los fallos 1, 2, 3, 4, 5. El CB aún está en estado CLOSED o HALF-OPEN.
        # El CB registra el fallo y lanza la excepción original (RequestError) al endpoint.
        logger.warning(f"⚠️ Fallo de conexión (CB contando): {type(e).__name__}: {e}")
        raise HTTPException(status_code=503, detail="Servicio de Productos no disponible (Fallo de conexión)")
        
    # 3. ERROR LÓGICO DE SERVIDOR (5xx) EXCLUIDO
    except httpx.HTTPStatusError as e:
        # Esto ocurre si el Productos devuelve 5xx. El CB lo ignora (exclude) y se propaga al endpoint.
        raise HTTPException(status_code=503, detail="Servicio de Productos fallando internamente (Error 5xx)")

    # --- 3. CREAR PEDIDO LOCALMENTE (DB orders.db) ---
    