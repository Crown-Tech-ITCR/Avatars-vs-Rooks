class BuzzerHandler:
    
    def __init__(self, wifi_handler=None):
        self.wifi_handler = wifi_handler
        self.buzzer_disponible = False
        self.verificar_disponibilidad()
    
    def verificar_disponibilidad(self):
        """Verifica si hay un buzzer disponible por WiFi"""
        if self.wifi_handler and self.wifi_handler.is_connected():
            self.buzzer_disponible = True
            print("Buzzer detectado por WiFi y listo")
        else:
            print("Buzzer no disponible (sin conexión WiFi)")
    
    def _enviar_comando(self, comando):
        """Envía comando al buzzer por WiFi"""
        if not self.buzzer_disponible:
            return
        
        try:
            if self.wifi_handler and self.wifi_handler.is_connected():
                self.wifi_handler.pico.send_command(comando)
                print(f"Comando '{comando}' enviado al buzzer")
        except Exception as e:
            print(f"Error enviando comando al buzzer: {e}")
    
    def tocar_victoria(self):
        """Reproduce melodía de victoria en el buzzer"""
        self._enviar_comando("WIN")
    
    def tocar_derrota(self):
        """Reproduce melodía de derrota en el buzzer"""
        self._enviar_comando("LOSE")

    def tocar_moneda(self):
        """Reproduce melodía de recolección de moneda en el buzzer"""
        self._enviar_comando("COIN")
    
    def esta_disponible(self):
        """Retorna si el buzzer está disponible"""
        return self.buzzer_disponible