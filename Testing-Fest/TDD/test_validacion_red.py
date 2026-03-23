# test_validacion_red.py
#from logic import es_mensaje_valido

def test_no_permite_mensajes_vacios():
    # El requerimiento dice: no enviar mensajes vacíos
    assert es_mensaje_valido("   ") is False

def test_no_permite_mensajes_muy_largos():
    # El requerimiento dice: límite de 100 caracteres
    assert es_mensaje_valido("A" * 101) is False