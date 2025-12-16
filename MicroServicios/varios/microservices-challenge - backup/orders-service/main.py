from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
'''Instancia Logger'''
from logger_config import configurar_logger
logger = configurar_logger('PEDIDOS-SERVICE')

'''Instancia de FastApi'''
app = FastAPI(title='Microservicio de Pedidos')

'''Base de Datos'''
#Se importa herramientas que creamos
import models, schemas                  #Modelos de DB y esquemas de pydantic
from database import engine, get_db     #Conexion a DB y dependencia
#Creamos las tablas en la DB
models.Base.metadata.create_all(bind=engine)


PRODUCTS_SERVICE_URL = 'http://127.0.0.1:8000'
INVENTORY_SERVICE_URL = 'http://127.0.0.1:8001'
INTERNAL_SECRECT_TOKEN = 'token_1234as1##@.'


# Función para hacer llamadas externas con seguridad
async def call_external_service ( url: str, method: str = 'GET', data: dict = None ):
    # Define un timeout de 15 segundos para la llamada completa
    TIMEOUT_LIMIT = 30 
    
    # Usa timeout en la creación del cliente
    async with httpx.AsyncClient(timeout=TIMEOUT_LIMIT) as client:
        try:
            headers = {'Authorization': f'Bearer {INTERNAL_SECRECT_TOKEN}'}
            
            if method == 'GET':
                response = await client.get(url, headers=headers)
            elif method == 'POST':
                # Usa json=data para enviar el cuerpo de la petición
                response = await client.post(url, headers=headers, json=data) 
            else:
                 raise ValueError("Método HTTP no soportado por esta función.")
                
        # Capturamos errores de CONEXIÓN/TIMEOUT (httpx.RequestError)
        # ESTA ES LA EXCEPCIÓN QUE EL CB CUENTA COMO FALLO
        except httpx.RequestError as e:
            print(f'Error de conexión o timeout al servicio de inventario: {e}')
            # Propagamos la excepción al decorador para que la registre como fallo.
            raise e
        except httpx.HTTPStatusError as e:
            # Esta excepción está en 'exclude' del CB, así que no cuenta como fallo
            # y se propaga directamente al endpoint para ser tratada como 503.
            raise e
        
# orders-service/main.py (Endpoint)

@app.post("/orders/", response_model=schemas.OrderBase, status_code=201)
async def create_order(order_data: schemas.OrderBase, db: Session = Depends(get_db)):
    product_id = order_data.product_id
    quantity = order_data.cantidad

    logger.info(f"Iniciando creación de pedido para Producto {product_id} x {quantity}")

    # --- 1. VERIFICAR PRODUCTO (Llamada a Products Service) ---
    product_url = f"{PRODUCTS_SERVICE_URL}/products/{product_id}"
    try:
        # Llama a la función genérica
        product_info = await call_external_service(product_url)
        logger.info(f"Producto  verificado")
    except HTTPException as e:
        # Reenvía el error si el producto no existe (ej: 404 de Products Service)
        raise HTTPException(
            status_code=e.status_code, 
            detail=f"Error en verificación de producto: {e.detail}"
        )
        

    # # que disminuye la cantidad y devuelve el nuevo stock, o falla si no hay suficiente.
    # inventory_reserve_url = f"{INVENTORY_SERVICE_URL}/inventory/reserve"
    # inventory_payload = {"product_id": product_id, "quantity_to_reserve": quantity}

    # try:
    #     # LLAMA al nuevo endpoint de reserva de inventario
    #     # new_stock_info = await call_external_service(inventory_reserve_url, method='POST', data=inventory_payload)
        
    #     # POR AHORA, para no detenernos: Simula la reserva exitosa y continúa.
    #     new_stock_info = {"new_quantity": product_info['stock'] - quantity} 
        
    #     # Debes agregar la lógica de: if new_stock_info['new_quantity'] < 0: raise HTTPException(...)
    #     if product_info['stock'] < quantity:
    #          raise HTTPException(status_code=400, detail="Stock insuficiente.")

    #     logger.info(f"Stock reservado. Nuevo stock: {new_stock_info['new_quantity']}")

    # except HTTPException as e:
    #     # Error en la reserva (ej: stock insuficiente)
    #     raise HTTPException(
    #         status_code=e.status_code, 
    #         detail=f"Fallo en la reserva de stock: {e.detail}"
    #     )


    # --- 3. CREAR PEDIDO LOCALMENTE (DB orders.db) ---
    
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