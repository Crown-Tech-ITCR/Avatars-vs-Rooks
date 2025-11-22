"""
Código para Raspberry Pi Pico W (MicroPython)
Servidor WiFi para control del juego Avatars vs Rooks
Fusiona funcionalidad WiFi con el sistema de Joystick, Buzzer y Botones existente

HARDWARE:
- Joystick en pines GP26, GP27, GP22
- Buzzer en pin GP15
- Botones Rooks en pines GP16, GP17, GP18, GP19
- Boton pausa en pin GP14
- Boton monedas en GP13

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
from Buzzer import buzzer
from Botones import botones

# ============= CONFIGURACIÓN WiFi =============
# Aquí se cambia la red de acuerdo a la del momento
WIFI_SSID = "Tigo"         
WIFI_PASSWORD = "123456789"  
SERVER_PORT = 8080                   

# ============= CONFIGURACIÓN DE HARDWARE =============

# LED integrado de la Pico W (util para pruebas)
led = Pin("LED", Pin.OUT)

# Inicializar hardware
stick = joystick(27, 26, 22)       
buzzer_hw = buzzer(15)
botones_hw = botones(16, 17, 18, 19)
boton_pausa = Pin(14, Pin.IN, Pin.PULL_UP)
boton_monedas = Pin(13, Pin.IN, Pin.PULL_UP)
ultimo_estado_pausa = 1
ultimo_estado_moneda = 1

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
        print(f'Conectado a WiFi')
        print(f'IP de la Pico W: {ip}')
        print(f'Puerto: {SERVER_PORT}')
        print(f'\n>>> Usa esta IP en tu juego: {ip} <<<\n')
        return wlan, ip
    else:
        print('No se pudo conectar a WiFi')
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
    
    # ===== COMANDOS DEL BUZZER =====
    
    if command == "WIN":
        # Victoria - melodía de victoria
        buzzer_hw.melodia_victoria()
        print("Melodía de victoria")
        
    elif command == "LOSE":
        # Derrota - melodía de derrota
        buzzer_hw.melodia_derrota()
        print("Melodía de derrota")
        
    elif command == "COIN":
        # Moneda obtenida
        buzzer_hw.melodia_moneda()
        print("Melodía de moneda")
    
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
        
        
    elif command == "game_over":
        # El juego terminó
        won = data.get("won", False)
        print(f" Juego terminado. ¿Ganó? {won}")
        
        # Reproducir melodía correspondiente
        if won:
            buzzer_hw.melodia_victoria()
        else:
            buzzer_hw.melodia_derrota()
    
    elif command == "level_complete":
        # Nivel completado
        level = data.get("level", 0)
        print(f"Nivel {level} completado!")
        
        # Efecto de celebración
        buzzer_hw.melodia_victoria()
    
    elif command == "ping":
        # Responder a ping
        send_event(client_socket, "pong", {"timestamp": time.time()})
        print("Pong enviado")
    
    else:
        print(f"Comando desconocido: {command}")

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
        print(f"Error al enviar evento: {e}")
        return False

# ============= LECTURA DE JOYSTICK Y BOTONES =============
def leer_joystick_y_botones():
    """
    Lee el joystick y botones usando las clases existentes
    Retorna el comando en formato compatible con InputHandler
    """
    global ultimo_estado_pausa
    global ultimo_estado_moneda
    
    try:
        # Leer botón de pausa
        estado_pausa = boton_pausa.value()
        pausa_presionada = (estado_pausa == 0 and ultimo_estado_pausa == 1)
        ultimo_estado_pausa = estado_pausa  # ← SIEMPRE actualizar
        
        if pausa_presionada:
            return "BTN,PAUSA"
        
        # Leer boton de recolectar monedas
        estado_moneda = boton_monedas.value()
        moneda_presionada = (estado_moneda == 0 and ultimo_estado_moneda == 1)
        ultimo_estado_moneda = estado_moneda  # ← SIEMPRE actualizar
        
        if moneda_presionada:
            return "BTN,MONEDA"
        
        # Leer botones de rooks
        boton = botones_hw.leer_estado()
        if boton:
            return f"BTN,{boton}"
        
        # Leer joystick
        movement = stick.getMovement()
        click = stick.getClick()
        direction = stick.getDirection()
        
        # Si hay movimiento, enviar con el estado del click
        if movement and movement != "Centro":
            return f"{movement},{int(click)}"
        
        # Si no hay movimiento pero el joystick está en una dirección (no centro)
        # Y hay click, enviar eso
        if click and direction != "Centro":
            return f"{direction},1"
        
        # Si estamos en centro y hay click, enviar click en centro
        if click:
            return f"Centro,1"
        
        # Enviar Centro, 0 cuando no hay click para resetear el estado
        return f"Centro,0"
    
    except Exception as e:
        print(f"Error leyendo hardware: {e}")
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
            print(f'\n Cliente conectado desde {client_addr}')
            
            # LED de confirmación
            led.on()
            time.sleep(0.5)
            led.off()
            
            # Bucle de comunicación con el cliente
            buffer = ""
            
            # Configurar socket como no bloqueante
            client_socket.setblocking(False)
            
            while True:
                try:
                    # Intentar recibir datos (no bloqueante)
                    try:
                        data = client_socket.recv(1024)
                        
                        if data:
                            buffer += data.decode('utf-8')
                            
                            # Procesar mensajes completos
                            while "\n" in buffer:
                                line, buffer = buffer.split("\n", 1)
                                
                                try:
                                    command_dict = json.loads(line)
                                    handle_command(command_dict, client_socket)
                                except json.JSONDecodeError as e:
                                    print(f"JSON inválido: {e}")
                    
                    except OSError as e:
                        # EAGAIN o EWOULDBLOCK = No hay datos disponibles (normal en modo no bloqueante)
                        # Errno 11 = EAGAIN, Errno 35 = EWOULDBLOCK (Mac), Errno 10035 = WSAEWOULDBLOCK (Windows)
                        if e.args[0] not in [11, 35, 10035]:
                            print(f'Error de socket: {e}')
                            raise
                    
                    # Leer joystick y botones usando el hardware existente
                    comando = leer_joystick_y_botones()
                    if comando:
                        # Determinar si es botón o joystick
                        if comando.startswith("BTN,"):
                            send_event(client_socket, "button", {"comando": comando})
                            print(f"{comando}")
                        else:
                            send_event(client_socket, "joystick", {"comando": comando})
                            print(f"{comando}")
                    
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
    
    # Parpadeo inicial de la ras al iniciar el juego
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
