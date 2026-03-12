import pytest
from unittest.mock import MagicMock
#from socket_code.servidor import enviar_a_todos
# Importamos las listas y funciones de tu servidor
# Nota: Para esto, tu servidor.py no debería ejecutar el bucle 'while True' al importarse.
# (Tip: Pon el bucle principal dentro de un: if __name__ == "__main__":)

def test_agregar_cliente_a_lista():
    # 1. PREPARACIÓN
    # Simulamos un socket de cliente
    mock_socket = MagicMock() 
    lista_clientes = []
    
    # 2. ACCIÓN
    lista_clientes.append(mock_socket)
    
    # 3. VERIFICACIÓN
    assert len(lista_clientes) == 1
    assert mock_socket in lista_clientes