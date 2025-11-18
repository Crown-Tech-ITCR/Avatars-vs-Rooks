"""
Test simple para botón en GP12
Presiona el botón y verás un mensaje en la consola
"""
from machine import Pin
import time

# Configurar botón en GP12 con resistencia pull-up
boton = Pin(12, Pin.IN, Pin.PULL_UP)

print("=" * 40)
print("TEST BOTÓN GP12")
print("=" * 40)
print("Presiona el botón conectado al pin GP12")
print("Presiona Ctrl+C para salir")
print("=" * 40)

ultimo_estado = 1  # Pull-up: 1 = no presionado, 0 = presionado

try:
    while True:
        estado_actual = boton.value()
        
        # Detectar cambio de estado (flanco)
        if estado_actual != ultimo_estado:
            if estado_actual == 0:
                # Botón presionado
                print("🔴 BOTÓN PRESIONADO")
            else:
                # Botón soltado
                print("⚪ Botón soltado")
            
            ultimo_estado = estado_actual
        
        time.sleep(0.05)  # 50ms de delay

except KeyboardInterrupt:
    print("\n✓ Test finalizado")
