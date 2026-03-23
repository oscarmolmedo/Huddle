
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
    Retorna True o False
    """
    return len(nombre.strip()) >= 3

def es_mensaje_valido(mensaje):
    """
    .strip() si devuelve algo es True. Si queda "" devuelve False.
    Si mensaje es valido verifica longitud de cadena
    """
    #OPCIÓN COMPACTA
    return bool(mensaje.strip() and len(mensaje) <= 100)

def limpiar_mensaje(mensaje):
    """
    Limpia espacios de mensaje.
    """
    return mensaje.strip()