from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


'''Instancia Logger'''
from logger_config import configurar_logger
logger = configurar_logger('PEDIDOS-SERVICE')

'''Instancia de FastApi'''
app = FastAPI(title='Microservicio de Inventario')

'''TOKEN'''
from dependencies import verify_internal_token  #Validacion

'''Base de Datos'''
#Se importa herramientas que creamos
import models, schemas                          #Modelos de DB y esquemas de pydantic
from database import engine, get_db             #Conexion a DB y dependencia
'''INICIALIZACIONES VARIAS'''
#Crear DB
models.Base.metadata.create_all(bind=engine)




'''----ENDPOINTS----'''
#Dependencia del endpoint
@app.get('/inventory/{product_id}')
def read_inventory(product_id: int, is_authorized: bool = Depends(verify_internal_token), db: Session = Depends(get_db)):

    inventory_record = db.query(models.Inventario).filter(models.Inventario.product_id == product_id).first()

    if inventory_record is None:
        mensaje = 'Error 404 - No se encontro el registro de stock'
        logger.info(mensaje)
        raise HTTPException(status_code=404, detail='No se encontro el registro de stock')
    
    logger.info(f'Se consulto exitosamente el producto {product_id}')
    #Se retorna la cantidad
    return {'product_id': product_id, 'cantidad': inventory_record.cantidad}