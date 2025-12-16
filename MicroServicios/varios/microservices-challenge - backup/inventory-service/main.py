from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import logging

#Se importa herramientas que creamos
import models, schemas                  #Modelos de DB y esquemas de pydantic
from database import engine, get_db     #Conexion a DB y dependencia

'''INICIALIZACIONES VARIAS'''
#Crear DB
models.Base.metadata.create_all(bind=engine)
#Iniciar Api
app = FastAPI(title='Microservicio de Inventario')
#Esquema de validación
security_scheme = HTTPBearer()
#


'''Registro LOGS'''
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

'''----ENDPOINTS----'''


#Token
INTERNAL_SECRECT_TOKEN = 'token_1234as1##@.'

#Para validar token
def verify_internal_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):

    #Validacion del esquema
    if credentials.scheme.lower() != 'bearer':
        mensaje = 'Error 403 - Esquema de autorización inválido'
        logger.warning(mensaje)
        #HTTPBearer ya maneja este error, esto es una doble verificación con fines practicos
        raise HTTPException(status_code=403, detail='Esquema de autorización inválido')
    
    #Validacion token secreto
    if credentials.credentials != INTERNAL_SECRECT_TOKEN:
        mensaje = 'Error 403 - Token interno invalido'
        logger.warning(mensaje)
        raise HTTPException(status_code=403, detail='Token interno invalido')
    
    return True
         

#Dependencia del endpoint
@app.get('/inventory/{product_id}')
def read_inventory(product_id: int, is_authorized: bool = Depends(verify_internal_token), db: Session = Depends(get_db)):

    inventory_record = db.query(models.Inventario).filter(models.Inventario.product_id == product_id).first()

    if inventory_record is None:
        mensaje = 'Error 404 - No se encontro el registro de stock'
        logger.info(mensaje)
        raise HTTPException(status_code=404, detail='No se encontro el registro de stock')
    
    #Se retorna la cantidad
    return {'product_id': product_id, 'cantidad': inventory_record.cantidad}