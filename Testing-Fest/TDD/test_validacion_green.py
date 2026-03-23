# logic_green

def es_mensaje_valido(mensaje):
    if mensaje == "   ":
        return False
    if len(mensaje) > 100:
        return False
    return True

def test_mensaje_valido():
    assert es_mensaje_valido("AS") is True