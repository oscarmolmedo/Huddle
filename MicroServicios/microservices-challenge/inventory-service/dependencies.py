from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Esquema de seguridad
security_scheme = HTTPBearer()

# Token
INTERNAL_SECRECT_TOKEN = 'token_123@_inventory_to_products'

# Logger
from logger_config import configurar_logger
logger = configurar_logger('AUTH-SERVICE')


def verify_internal_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """
    Función de dependencia para validar el token interno 'Bearer'.
    Si la validación falla, lanza una HTTPException 403.
    """
    #Validacion del esquema
    if credentials.scheme.lower() != 'bearer':
        mensaje = 'Error 403 - Esquema de autorización inválido'
        logger.warning(mensaje)
        raise HTTPException(status_code=403, detail=mensaje)
    
    #Validacion token secreto
    if credentials.credentials != INTERNAL_SECRECT_TOKEN:
        mensaje = 'Error 403 - Token interno invalido'
        logger.warning(mensaje)
        raise HTTPException(status_code=403, detail=mensaje)
    
    logger.info(f'Token correcto | LOGGIN OK')
    return True