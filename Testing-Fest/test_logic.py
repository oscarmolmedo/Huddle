from socket_code.logic import procesar_protocolo, validar_nick, limpiar_mensaje, es_mensaje_valido
import pytest

# --- LOGICA DE FORMATO CORRECTO TIPO|CONTENIDO ---
# Caso Positivo
def test_protocolo_mensaje_valido():
    tipo, contenido = procesar_protocolo("MSG|hola servidor")
    assert tipo == "MSG"
    assert contenido == "hola servidor"

# Caso Negativo
def test_protocolo_sin_separador():
    with pytest.raises(ValueError): # Esperamos que falle con esta excepción
        procesar_protocolo("MENSAJE_INVALIDO")


# --- LOGICA DE NICKS ---
# Caso Positivo
def test_nick_valido():
    assert validar_nick("python_dev") is True

# Caso Negativo
def test_nick_demasiado_corto():
    assert validar_nick("ab") is False


# --- LOGICA DE LIMPIAR MENSAJE ---
# Caso Positivo
def test_mensaje_limpio():
    assert limpiar_mensaje("   Holaaa, como estas.   ") == 'Holaaa, como estas.'

# Caso Negativo (Error de Tipo)
def test_mensaje_limpio_tipo_incorrecto():
    assert limpiar_mensaje(3232322) is False# Los números no tienen el método .strip()


# --- LOGICA DE LIMPIAR MENSAJE ---
# Caso Positivo
    mensaje = "Aa" * 50
    assert es_mensaje_valido(mensaje) is True

# Caso Negativo
def test_mensaje_texto_valido():
    mensaje = "Aa" * 101
    assert es_mensaje_valido(mensaje) is False
