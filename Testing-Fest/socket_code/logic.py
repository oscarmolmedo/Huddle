
def procesar_protocolo(data_decodificada):
    """
    Recibe: "MSG|Hola" o "CMD|nick Pepe"
    Retorna: Tupla (tipo, contenido)
    Lanza: ValueError si el formato es incorrecto
    """
    if "|" not in data_decodificada:
        raise ValueError("Formato incorrecto: falta el separador '|'")
    
    partes = data_decodificada.split("|", 1)
    return partes[0], partes[1]

def validar_nick(nombre):
    """
    Retorna True si el nick es válido (3 o más caracteres), 
    False de lo contrario.
    """
    return len(nombre.strip()) >= 3

def limpiar_mensaje(mensaje):
    """
    Limpia todos los espacios al principio y final
    de la cadena
    """
    if isinstance(mensaje, str):
        return mensaje.strip()
    else:
        return False

def es_mensaje_valido(mensaje):
    """
    .strip() si devuelve algo es True. Si queda "" devuelve False.
    Si mensaje es valido verifica longitud de cadena
    """
    #OPCIÓN LARGA
    # es_valido = bool(mensaje.strip())

    # if es_valido:
    #     if len(mensaje) > 100:
    #         return False
    #     else:
    #         return True
    # else:
    #     return es_valido

    #OPCIÓN COMPACTA
    return bool(mensaje.strip() and len(mensaje) <= 100)