from aiobreaker import CircuitBreaker, CircuitBreakerError 
from datetime import timedelta
import httpx

'''Configuración del Circuit Breaker'''
# Creamos una instancia de CircuitBreaker.
# - fail_max: Número máximo de fallos consecutivos antes de pasar a estado OPEN.
# - reset_timeout: Tiempo en segundos que espera en estado OPEN antes de pasar a HALF-OPEN.
# Aquí estamos permitiendo que los errores 404 de HTTP pasen sin abrir el circuito.
inventory_circuit_breaker = CircuitBreaker(
    fail_max=3, 
    timeout_duration=timedelta(seconds=10), 
    exclude=[httpx.HTTPStatusError] # Usamos httpx.HTTPStatusError ya que raise_for_status la lanza
)

'''Conexion a Inventario'''
INVENTORY_SERVICE_URL = 'http://127.0.0.1:8001'
INTERNAL_SECRECT_TOKEN = 'token_1234as1##@.'


#Funcion asincrona para llamar a Inventario
@inventory_circuit_breaker
async def get_inventory_quantity (product_id : int ):
    async with httpx.AsyncClient() as client:
        try:
            headers = {'Authorization': f'Bearer {INTERNAL_SECRECT_TOKEN}'}
            response = await client.get(f'{INVENTORY_SERVICE_URL}/inventory/{product_id}', headers=headers)

            if response.status_code == 200:
                return response.json().get('cantidad')
            elif response.status_code == 404:
                # Éxito lógico (no cuenta como fallo para el CB)
                return 0
            else:
                # Lanza httpx.HTTPStatusError. Como NO es de conexión y está en 'exclude',
                # el CB lo considera un éxito, pero el endpoint debe manejar este error.
                response.raise_for_status()
                
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