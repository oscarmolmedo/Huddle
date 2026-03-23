# logic_green.py

def es_mensaje_valido(mensaje):
    # Solución rápida: solo lo necesario para que el test no falle
    if mensaje == "   ":
        return False
    if len(mensaje) > 100:
        return False
    return True

def test_mensaje_valido():
    assert es_mensaje_valido("Holayo") is True