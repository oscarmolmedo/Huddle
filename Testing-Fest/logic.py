
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
    return mensaje.strip()