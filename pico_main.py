"""
Código para Raspberry Pi Pico W (MicroPython)
Servidor WiFi para control del juego Avatars vs Rooks
Fusiona funcionalidad WiFi con el sistema de Joystick, Buzzer y Botones existente

INSTRUCCIONES DE INSTALACIÓN:
1. Instala Thonny IDE (https://thonny.org/)
2. Conecta tu Pico W vía USB
3. En Thonny, selecciona MicroPython (Raspberry Pi Pico)
4. Sube este archivo como main.py en la Pico W
5. Sube también: Joystick.py, Buzzer.py, Botones.py
6. Modifica WIFI_SSID y WIFI_PASSWORD con tus credenciales
7. Reinicia la Pico W

HARDWARE:
- Joystick en pines GP26, GP27, GP22
- Buzzer en pin GP15
- Botones en pines GP16, GP17, GP18, GP19
"""

import network
import socket
import json
import time
import sys
import select
from machine import Pin

# Importar clases del hardware
from Joystick import joystick
from Buzzer import buzzer as BuzzerClass
from Botones import botones

# ============= CONFIGURACIÓN WiFi =============
WIFI_SSID = "TU_WIFI_AQUI"          # Cambia esto por tu red WiFi
WIFI_PASSWORD = "TU_PASSWORD_AQUI"   # Cambia esto por tu contraseña
SERVER_PORT = 8080                    # Puerto del servidor

# ============= CONFIGURACIÓN DE HARDWARE =============
# LED integrado de la Pico W (indicador de estado)
led = Pin("LED", Pin.OUT)

# Inicializar hardware
stick = joystick(27, 26, 22)        # Y, X, Click
buzzer_hw = BuzzerClass(15)         # Buzzer en GP15
botones_hw = botones(16, 17, 18, 19)  # Botones en GP16-19

print("✓ Hardware inicializado")
print("  - Joystick: GP26(X), GP27(Y), GP22(Click)")
print("  - Buzzer: GP15")
print("  - Botones: GP16-19")

# ============= FUNCIONES WiFi =============
def connect_wifi():
    """Conecta la Pico W a WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'Conectando a {WIFI_SSID}...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Esperar conexión (timeout 10 segundos)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print('.', end='')
        
        print()
    
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f'✓ Conectado a WiFi')
        print(f'✓ IP de la Pico W: {ip}')
        print(f'✓ Puerto: {SERVER_PORT}')
        print(f'\n>>> Usa esta IP en tu juego: {ip} <<<\n')
        return wlan, ip
    else:
        print('✗ No se pudo conectar a WiFi')
        return None, None

# ============= MANEJO DE COMANDOS =============
def handle_command(command_dict, client_socket):
    """
    Procesa comandos recibidos del juego
    
    Args:
        command_dict: Diccionario con el comando
        client_socket: Socket del cliente para respuestas
    """
    command = command_dict.get("command", "")
    data = command_dict.get("data", {})
    
    print(f"← Comando recibido: {command}")
    
    # ===== COMANDOS DEL BUZZER (Compatibles con picow.py) =====
    
    if command == "WIN":
        # Victoria - melodía de victoria
        buzzer_hw.melodia_victoria()
        print("  → Melodía de victoria")
        
    elif command == "LOSE":
        # Derrota - melodía de derrota
        buzzer_hw.melodia_derrota()
        print("  → Melodía de derrota")
        
    elif command == "COIN":
        # Moneda obtenida
        buzzer_hw.melodia_moneda()
        print("  → Melodía de moneda")
    
    # ===== COMANDOS DEL LED =====
    
    elif command == "led_on":
        # Encender LED
        led.on()
        print("  → LED encendido")
        
    elif command == "led_off":
        # Apagar LED
        led.off()
        print("  → LED apagado")
        
    elif command == "led_blink":
        # Parpadear LED
        duration = data.get("duration", 0.5)
        for _ in range(3):
            led.on()
            time.sleep(duration)
            led.off()
            time.sleep(duration)
        print(f"  → LED parpadeó 3 veces")
    
    # ===== COMANDOS DE ESTADO DEL JUEGO =====
    
    elif command == "game_state":
        # Recibir estado del juego
        level = data.get("level", 0)
        score = data.get("score", 0)
        lives = data.get("lives", 0)
        print(f"  → Nivel: {level}, Puntos: {score}, Vidas: {lives}")
        
        # Aquí puedes actualizar un display LCD, LEDs, etc.
        
    elif command == "game_over":
        # El juego terminó
        won = data.get("won", False)
        print(f"  → Juego terminado. ¿Ganó? {won}")
        
        # Reproducir melodía correspondiente
        if won:
            buzzer_hw.melodia_victoria()
        else:
            buzzer_hw.melodia_derrota()
    
    elif command == "level_complete":
        # Nivel completado
        level = data.get("level", 0)
        print(f"  → Nivel {level} completado!")
        
        # Efecto de celebración
        buzzer_hw.melodia_victoria()
        for _ in range(3):
            led.on()
            time.sleep(0.1)
            led.off()
            time.sleep(0.1)
    
    elif command == "ping":
        # Responder a ping
        send_event(client_socket, "pong", {"timestamp": time.time()})
        print("  → Pong enviado")
    
    else:
        print(f"  ⚠ Comando desconocido: {command}")

# ============= ENVÍO DE EVENTOS =============
def send_event(client_socket, event_type, data=None):
    """
    Envía un evento al juego (PC)
    
    Args:
        client_socket: Socket del cliente
        event_type: Tipo de evento (ej: "button_press")
        data: Datos del evento
    """
    try:
        message = {
            "event": event_type,
            "data": data,
            "timestamp": time.time()
        }
        
        json_str = json.dumps(message) + "\n"
        client_socket.send(json_str.encode('utf-8'))
        return True
    except Exception as e:
        print(f"✗ Error al enviar evento: {e}")
        return False

# ============= LECTURA DE JOYSTICK Y BOTONES =============
def leer_joystick_y_botones():
    """
    Lee el joystick y botones usando las clases existentes
    Retorna el comando en formato compatible con InputHandler
    """
    try:
        # Leer botones de rooks primero (tienen prioridad)
        boton = botones_hw.leer_estado()
        if boton:
            return f"BTN,{boton}"
        
        # Leer joystick
        movement = stick.getMovement()
        click = stick.getClick()
        direction = stick.getDirection()
        
        # Siempre retornar la posición actual (movimiento o dirección)
        if movement and movement != "Centro":
            # Hay movimiento (Arriba, Abajo, Izquierda, Derecha)
            return f"{movement},{int(click)}"
        elif click:
            # Click en el centro
            return f"Centro,1"
        else:
            # Sin movimiento significativo, retornar None para no saturar
            return None
    
    except Exception as e:
        print(f"✗ Error leyendo hardware: {e}")
        return None

# ============= SERVIDOR PRINCIPAL =============
def start_server(ip):
    """Inicia el servidor TCP"""
    addr = socket.getaddrinfo(ip, SERVER_PORT)[0][-1]
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(addr)
    server_socket.listen(1)
    
    print(f'Servidor escuchando en {ip}:{SERVER_PORT}')
    print('Esperando conexión del juego...\n')
    
    while True:
        try:
            # Aceptar conexión
            client_socket, client_addr = server_socket.accept()
            print(f'\n✓ Cliente conectado desde {client_addr}')
            
            # LED de confirmación
            led.on()
            time.sleep(0.5)
            led.off()
            
            # Bucle de comunicación con el cliente
            buffer = ""
            
            while True:
                try:
                    # Recibir datos
                    data = client_socket.recv(1024)
                    
                    if not data:
                        print('✗ Cliente desconectado')
                        break
                    
                    buffer += data.decode('utf-8')
                    
                    # Procesar mensajes completos
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        
                        try:
                            command_dict = json.loads(line)
                            handle_command(command_dict, client_socket)
                        except json.JSONDecodeError as e:
                            print(f"✗ JSON inválido: {e}")
                    
                    # Leer joystick y botones usando el hardware existente
                    comando = leer_joystick_y_botones()
                    if comando:
                        # Determinar si es botón o joystick
                        if comando.startswith("BTN,"):
                            send_event(client_socket, "button", {"comando": comando})
                            print(f"  🔘 {comando}")
                        else:
                            send_event(client_socket, "joystick", {"comando": comando})
                            print(f"  🕹️  {comando}")
                    
                    # Pequeño delay para no saturar (50ms = 20 lecturas por segundo)
                    time.sleep(0.05)
                    
                except OSError as e:
                    print(f'✗ Error de socket: {e}')
                    break
            
            # Cerrar conexión del cliente
            client_socket.close()
            led.off()
            print('Esperando nueva conexión...\n')
            
        except KeyboardInterrupt:
            print('\nServidor detenido')
            break
        except Exception as e:
            print(f'✗ Error en servidor: {e}')
            time.sleep(1)
    
    server_socket.close()

# ============= PROGRAMA PRINCIPAL =============
def main():
    """Función principal"""
    print('='*50)
    print('Raspberry Pi Pico W - Servidor de Juego')
    print('='*50)
    
    # Parpadeo inicial
    for _ in range(3):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
    
    # Conectar a WiFi
    wlan, ip = connect_wifi()
    
    if ip:
        # Iniciar servidor
        try:
            start_server(ip)
        except Exception as e:
            print(f'✗ Error fatal: {e}')
            led.on()  # LED encendido = error
    else:
        print('No se pudo iniciar el servidor')
        # Parpadeo de error
        while True:
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)

# Ejecutar
if __name__ == "__main__":
    main()
