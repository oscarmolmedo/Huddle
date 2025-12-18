from aiobreaker import CircuitBreaker, CircuitBreakerError 
from datetime import timedelta
import httpx

'''Configuración del Circuit Breaker'''
# Creamos una instancia de CircuitBreaker.
# - fail_max: Número máximo de fallos consecutivos antes de pasar a estado OPEN.
# - reset_timeout: Tiempo en segundos que espera en estado OPEN antes de pasar a HALF-OPEN.
# Aquí estamos permitiendo que los errores 404 de HTTP pasen sin abrir el circuito.
service_circuit_breaker = CircuitBreaker(
    fail_max=3, 
    timeout_duration=timedelta(seconds=30), 
    exclude=[httpx.HTTPStatusError] # Usamos httpx.HTTPStatusError ya que raise_for_status la lanza
)



#Funcion asincrona para llamar a Inventario
@service_circuit_breaker
async def call_external_service (url: str, nombre_servicio: str, service_header ):
    #with se usa para inicializar y liberar el recurso evitando bloqueos y resultados inesperados
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            headers = {'Authorization': f'Bearer {service_header}'}
            #await desencadena un comportamiento sincrono dentro de la funcion asincrona
            response = await client.get(url, headers=headers)

            if response.status_code == 200:
                #return response.json().get('cantidad')
                return response.json()
            elif response.status_code == 403:
                # El servicio remoto respondió que el token es inválido o no autorizado.
                mensaje_error = f'Error de autorización (403) al conectar con {nombre_servicio}. El token interno es inválido.'
                print(mensaje_error)
                # Propagamos el error como una excepción HTTP normal, para ser capturada
                # en el endpoint y no cuente como fallo del Circuit Breaker.
                raise httpx.HTTPStatusError(
                    message=mensaje_error, 
                    request=response.request, 
                    response=response
                )
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
            print(f'Error de conexión o timeout al servicio {nombre_servicio}: {e}')
            # Propagamos la excepción al decorador para que la registre como fallo.
            raise e
        except httpx.HTTPStatusError as e:
            # Esta excepción está en 'exclude' del CB, así que no cuenta como fallo
            # y se propaga directamente al endpoint para ser tratada como 503.
            raise e