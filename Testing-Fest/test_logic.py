from logic import procesar_protocolo, validar_nick, limpiar_mensaje
import pytest

# PRUEBA 1: Caso Positivo - ¿Funciona el protocolo MSG?
def test_protocolo_mensaje_valido():
    tipo, contenido = procesar_protocolo("MSG|hola servidor")
    assert tipo == "MSG"
    assert contenido == "hola servidor"

# PRUEBA 2: Caso Negativo - ¿Qué pasa si envío algo sin el pipe '|'?
def test_protocolo_sin_separador():
    with pytest.raises(ValueError): # Esperamos que falle con esta excepción
        procesar_protocolo("MENSAJE_INVALIDO")

# PRUEBA 3: Validación de Nick
def test_nick_demasiado_corto():
    assert validar_nick("ab") is False

def test_nick_valido():
    assert validar_nick("python_dev") is True

# PRUEBA 4: Limpia espacios del mensaje
def test_mensaje_limpio():
    assert limpiar_mensaje("   Holaaa, como estas.   ") == 'Holaaa, como estas.'