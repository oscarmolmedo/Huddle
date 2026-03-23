import pytest
from unittest.mock import MagicMock
from socket_code.logic import procesar_protocolo, es_mensaje_valido, validar_nick
import socket_code.servidor as servidor



# --- PRUEBAS UNITARIAS (Funciones Críticas) ---
#Procesar Protocolo
def test_unit_protocolo_valido():
    a,b =procesar_protocolo("CMD|nick") 
    assert a,b is True
def test_unit_protocolo_invalido():
    with pytest.raises(ValueError):
        procesar_protocolo("mensaje_sin_pipe")

#Validar mensaje
def test_unit_es_mensaje_valido():
    assert es_mensaje_valido("Hola como estas? :)") is True
def test_unit_es_mensaje_invalido():
    assert es_mensaje_valido("Hola como estas? :)" * 50) is False

# VALIDAR NICK
def test_unit_nick_valido():
    assert validar_nick("olos") is True
def test_unit_nick_invalido():
    assert validar_nick("H1") is False
    
# --- PRUEBA TDD (Validación de longitud y contenido) ---
#RED
def test_es_mensaje_valido_falla_si_esta_vacio():
    assert es_mensaje_valido("   ") is False

#GREEN
def test_es_mensaje_valido_falla_si_es_muy_largo():
    assert es_mensaje_valido("A" * 101) is False

#--- PRUEBAS DE INTEGRACIÓN (Múltiples clientes y Broadcast) ---
def test_integracion_broadcast_exitoso():
    clientes = []
    servidor.nicks = {}
    
    c1, c2, c3 = MagicMock(), MagicMock(), MagicMock()
    servidor.clientes.extend([c1, c2, c3])
    servidor.nicks[c1], servidor.nicks[c2], servidor.nicks[c3] = "Goku", "Vegeta", "Picolo"
    
    servidor.enviar_a_todos(c1, "Hola")
    
    # C2 debe recibirlo, C1 no (no se envía a sí mismo)
    c2.sendall.assert_called()
    c3.sendall.assert_called()
    c1.sendall.assert_not_called()

# --- PRUEBA DE DESCONEXIÓN (Condición excepcional) ---
def test_integracion_desconexion_abrupta():
    
    emisor  =  MagicMock()
    victima =  MagicMock()
    
    # Forzamos que la víctima falle al recibir
    victima.sendall.side_effect = Exception("Crash")
    
    servidor.clientes.extend([emisor, victima])
    servidor.nicks[emisor], servidor.nicks[victima] = "E", "V"
    
    # El servidor no debe romperse al ejecutar esto
    servidor.enviar_a_todos(emisor, "Test")
    
    # Verificamos que el servidor manejó el error eliminando al cliente
    assert victima not in servidor.clientes