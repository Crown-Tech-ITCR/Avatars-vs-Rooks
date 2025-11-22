"""
WiFiHandler - Adaptador para control WiFi del juego
Integra PicoCommunication con InputHandler para control transparente
El juego funciona con teclado si el mando WiFi no está conectado
"""

from pico_communication import PicoCommunication
from typing import Callable, Optional

class WiFiHandler:
    """
    Handler que adapta los comandos WiFi de la Pico W al formato InputHandler
    Permite control del juego mediante mando WiFi de forma transparente
    """
    
    def __init__(self, pico_ip: str = "192.168.1.100", pico_port: int = 8080, timeout: float = 2.0):
        """
        Inicializa el handler WiFi
        
        Args:
            pico_ip: IP de la Raspberry Pi Pico W (mando inalámbrico)
            pico_port: Puerto de comunicación
            timeout: Tiempo máximo de espera para conectar (segundos)
        """
        self.pico = PicoCommunication(pico_ip=pico_ip, pico_port=pico_port, 
                                     auto_connect=True, timeout=timeout)
        self.input_handler = None
        
        # Registrar callbacks para eventos de la Pico W inmediatamente
        # Los handlers verificarán si input_handler está configurado
        if self.pico.is_connected():
            self.pico.on_event("joystick", self._handle_joystick)
            self.pico.on_event("button", self._handle_button)
    
    def set_input_handler(self, input_handler):
        """
        Conecta este WiFiHandler con el InputHandler del juego
        
        Args:
            input_handler: Instancia de InputHandler del juego
        """
        self.input_handler = input_handler
        
        # Marcar que el "joystick" (mando WiFi) está detectado
        if self.pico.is_connected():
            self.input_handler.marcar_joystick_detectado()
            print("✓ Mando WiFi integrado con InputHandler")
    
    def _handle_joystick(self, data):
        """
        Maneja comandos del joystick desde la Pico W
        Convierte formato de Pico W a formato InputHandler
        """
        if not self.input_handler:
            # Si aún no se configuró, simplemente ignorar (eventos tempranos)
            return
        
        comando = data.get("comando", "")
        
        # El comando ya viene en formato compatible: "Direccion,Click"

        self.input_handler.procesar_comando_joystick(comando)
    
    def _handle_button(self, data):
        """
        Maneja comandos de botones desde la Pico W
        Convierte formato de Pico W a formato InputHandler
        """
        if not self.input_handler:
            # Si aún no se configuró, simplemente ignorar (eventos tempranos)
            return
        
        comando = data.get("comando", "")
        print(f"🔘 WiFiHandler recibió botón: {comando}")
        
        # El comando ya viene en formato compatible: "BTN,TIPO"
        # Ejemplo: "BTN,ARENA" o "BTN,FUEGO"
        self.input_handler.procesar_comando_joystick(comando)
        print(f"   → Comando enviado a InputHandler")
    
    def is_connected(self) -> bool:
        """Retorna True si el mando WiFi está conectado"""
        return self.pico.is_connected()
    
    def send_game_state(self, level: int, score: int, lives: int):
        """
        Envía el estado actual del juego al mando WiFi
        Útil para displays o LEDs en el mando
        
        Args:
            level: Nivel actual
            score: Puntuación actual
            lives: Vidas/puntos de vida actuales
        """
        if self.pico.is_connected():
            self.pico.send_command("game_state", {
                "level": level,
                "score": score,
                "lives": lives
            })
    
    def send_game_over(self, won: bool):
        """
        Notifica al mando WiFi que el juego terminó
        
        Args:
            won: True si ganó, False si perdió
        """
        if self.pico.is_connected():
            self.pico.send_command("game_over", {"won": won})
    
    def send_level_complete(self, level: int):
        """
        Notifica al mando WiFi que se completó un nivel
        
        Args:
            level: Nivel completado
        """
        if self.pico.is_connected():
            self.pico.send_command("level_complete", {"level": level})
            # Efecto visual en el mando (LED parpadeo)
            self.pico.send_command("led_blink", {"duration": 0.3})
    
    def led_on(self):
        """Enciende el LED del mando WiFi"""
        if self.pico.is_connected():
            self.pico.send_command("led_on")
    
    def led_off(self):
        """Apaga el LED del mando WiFi"""
        if self.pico.is_connected():
            self.pico.send_command("led_off")
    
    def led_blink(self, duration: float = 0.5):
        """
        Hace parpadear el LED del mando WiFi
        
        Args:
            duration: Duración del parpadeo en segundos
        """
        if self.pico.is_connected():
            self.pico.send_command("led_blink", {"duration": duration})
    
    def disconnect(self):
        """Desconecta el mando WiFi"""
        if self.pico:
            self.pico.disconnect()


# Función de utilidad para integración rápida
def create_wifi_handler(pico_ip: str = "192.168.1.100", pico_port: int = 8080) -> Optional[WiFiHandler]:
    """
    Crea y retorna un WiFiHandler configurado
    Si no se puede conectar, retorna None y el juego usa teclado
    
    Args:
        pico_ip: IP de la Raspberry Pi Pico W
        pico_port: Puerto de comunicación
        
    Returns:
        WiFiHandler si la conexión fue exitosa, None si se usa teclado
    """
    wifi_handler = WiFiHandler(pico_ip=pico_ip, pico_port=pico_port)
    
    if wifi_handler.is_connected():
        return wifi_handler
    else:
        return None
