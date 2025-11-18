"""
Módulo de comunicación con Raspberry Pi Pico W mediante WiFi
Compatible con el sistema InputHandler existente
Permite control del juego mediante teclado O mando WiFi automáticamente
"""

import socket
import threading
import json
import time
from typing import Callable, Dict, Any, Optional

class PicoCommunication:
    """Cliente de comunicación WiFi con Raspberry Pi Pico W (Mando inalámbrico)"""
    
    def __init__(self, pico_ip: str = "192.168.1.100", pico_port: int = 8080, auto_connect: bool = True, timeout: float = 2.0):
        """
        Inicializa la comunicación con la Pico W
        
        Args:
            pico_ip: Dirección IP de la Raspberry Pi Pico W
            pico_port: Puerto de comunicación
            auto_connect: Si True, intenta conectar automáticamente al crear la instancia
            timeout: Tiempo máximo de espera para la conexión (en segundos)
        """
        self.pico_ip = pico_ip
        self.pico_port = pico_port
        self.connected = False
        self.running = False
        self.receive_thread = None
        self.event_callbacks: Dict[str, Callable] = {}
        self.timeout = timeout
        
        # Auto-conexión al inicializar
        if auto_connect:
            self.connect()
        
    def connect(self) -> bool:
        """
        Intenta conectar con la Raspberry Pi Pico W (mando inalámbrico)
        Si falla, el juego continuará con control de teclado
        
        Returns:
            True si la conexión fue exitosa, False en caso contrario
        """
        try:
            # Crear socket para comunicación
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            
            print(f"🎮 Buscando mando WiFi en {self.pico_ip}:{self.pico_port}...")
            self.socket.connect((self.pico_ip, self.pico_port))
            
            self.connected = True
            self.running = True
            
            # Iniciar hilo para recibir datos
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.receive_thread.start()
            
            print("✓ Mando WiFi conectado - Controles del mando activados")
            return True
            
        except socket.timeout:
            print(f"⌨️  Mando WiFi no detectado - Usando teclado")
            self.connected = False
            return False
        except ConnectionRefusedError:
            print(f"⌨️  Mando WiFi no disponible - Usando teclado")
            self.connected = False
            return False
        except Exception as e:
            print(f"⌨️  Mando WiFi no encontrado - Usando teclado")
            self.connected = False
            return False
    
    def disconnect(self):
        """Cierra la conexión con la Pico W"""
        self.running = False
        self.connected = False
        
        if hasattr(self, 'socket'):
            try:
                self.socket.close()
            except:
                pass
        
        print("Mando WiFi desconectado")
    
    def send_command(self, command: str, data: Any = None) -> bool:
        """
        Envía un comando a la Raspberry Pi Pico W
        
        Args:
            command: Nombre del comando (ej: "led_on", "game_state", etc.)
            data: Datos adicionales para el comando
            
        Returns:
            True si el envío fue exitoso, False en caso contrario
        """
        if not self.connected:
            print("✗ No hay conexión con Pico W")
            return False
        
        try:
            message = {
                "command": command,
                "data": data,
                "timestamp": time.time()
            }
            
            json_str = json.dumps(message) + "\n"
            self.socket.sendall(json_str.encode('utf-8'))
            
            print(f"→ Enviado: {command}")
            return True
            
        except Exception as e:
            print(f"✗ Error al enviar comando: {e}")
            self.connected = False
            return False
    
    def _receive_loop(self):
        """Bucle de recepción de datos (ejecutado en hilo separado)"""
        buffer = ""
        
        while self.running:
            try:
                # Recibir datos
                data = self.socket.recv(1024).decode('utf-8')
                
                if not data:
                    print("✗ Mando WiFi desconectado - Usando teclado")
                    self.connected = False
                    break
                
                buffer += data
                
                # Procesar mensajes completos (separados por \n)
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    
                    try:
                        message = json.loads(line)
                        self._handle_message(message)
                    except json.JSONDecodeError:
                        print(f"✗ Mensaje JSON inválido: {line}")
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"✗ Error en bucle de recepción: {e}")
                self.connected = False
                break
        
        self.running = False
    
    def _handle_message(self, message: Dict):
        """
        Maneja un mensaje recibido de la Pico W
        
        Args:
            message: Diccionario con el mensaje
        """
        print(f"← Recibido: {message}")
        
        event_type = message.get("event", "unknown")
        
        # Llamar al callback registrado para este tipo de evento
        if event_type in self.event_callbacks:
            try:
                self.event_callbacks[event_type](message.get("data"))
            except Exception as e:
                print(f"✗ Error en callback para evento '{event_type}': {e}")
    
    def on_event(self, event_type: str, callback: Callable):
        """
        Registra un callback para un tipo de evento específico
        
        Args:
            event_type: Tipo de evento (ej: "button_press", "sensor_data")
            callback: Función a llamar cuando se reciba el evento
        """
        self.event_callbacks[event_type] = callback
        print(f"✓ Callback registrado para evento: {event_type}")
    
    def is_connected(self) -> bool:
        """Retorna True si está conectado a la Pico W"""
        return self.connected


# Ejemplo de uso y prueba
if __name__ == "__main__":
    # Crear instancia de comunicación
    pico = PicoCommunication(pico_ip="192.168.1.100", pico_port=8080)
    
    # Definir callbacks para eventos
    def on_button_press(data):
        print(f"¡Botón presionado! Datos: {data}")
    
    def on_sensor_data(data):
        print(f"Datos de sensor recibidos: {data}")
    
    # Registrar callbacks
    pico.on_event("button_press", on_button_press)
    pico.on_event("sensor_data", on_sensor_data)
    
    # Conectar
    if pico.connect():
        try:
            # Enviar algunos comandos de prueba
            time.sleep(1)
            pico.send_command("led_on", {"color": "red"})
            
            time.sleep(2)
            pico.send_command("game_state", {"level": 1, "score": 100})
            
            # Mantener programa corriendo
            print("\nPresiona Ctrl+C para salir...")
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nCerrando...")
        finally:
            pico.disconnect()
    else:
        print("No se pudo conectar con la Pico W")
