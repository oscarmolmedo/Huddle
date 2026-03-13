import pytest
from unittest.mock import MagicMock
from socket_code.servidor import enviar_a_todos, procesar_comando,clientes, nicks

# --- TEST ENVÍO  ---

def test_procesar_comando_nick_con_mock():
    # 1. Creamos el "Socket de juguete"
    mock_socket_cliente = MagicMock()
    
    # 2. Creamos una dirección falsa (tu función espera una tupla o string)
    fake_addr = ("127.0.0.1", 12345)
    
    # 3. Definimos el mensaje (Protocolo: CMD|nick nombre)
    mensaje_con_nick = "nick Pepe"

    # 4. LLAMAMOS A LA FUNCIÓN REAL
    # Aquí es donde el MagicMock entra en acción reemplazando al socket real
    resultado = procesar_comando(mock_socket_cliente, fake_addr, mensaje_con_nick)

    # 5. VERIFICACIONES
    # ¿La función devolvió True (continuar)?
    assert resultado is True
    # ¿Se guardó el nick en el diccionario global del servidor?
    assert nicks[mock_socket_cliente] == "Pepe"


def test_desconexion_abrupta_broadcast():
    
    
    cliente_roto = MagicMock()
    cliente_ok = MagicMock()
    # Programamos el Mock para que lance un error de socket al intentar enviar
    cliente_roto.sendall.side_effect = Exception("Socket Error")
    
    clientes.append(cliente_roto)
    clientes.append(cliente_ok)
    
    # Al llamar a enviar_a_todos, el bloque try/except de tu servidor
    # debería capturar el error del Mock y eliminarlo de la lista.
    enviar_a_todos("Cliente1Prueba", "mensaje") 

    # Verificamos que el servidor fue "limpio" y sacó al cliente roto
    assert cliente_roto not in clientes

