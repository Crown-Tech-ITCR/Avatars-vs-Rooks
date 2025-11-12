class BuzzerHandler:
    
    def __init__(self, serial_handler):
        self.serial_handler = serial_handler
        self.buzzer_disponible = False
        self.verificar_disponibilidad()
    
    def verificar_disponibilidad(self):
        """Verifica si hay un buzzer disponible"""
        self.buzzer_disponible = self.serial_handler.conectado
        if self.buzzer_disponible:
            print("🔊 Buzzer detectado y listo")
    
    def tocar_victoria(self):
        """Reproduce melodía de victoria en el buzzer"""
        if self.buzzer_disponible:
            try:
                self.serial_handler.enviar_comando("WIN")
            except Exception as e:
                print(f"Error reproduciendo victoria: {e}")
    
    def tocar_derrota(self):
        """Reproduce melodía de derrota en el buzzer"""
        if self.buzzer_disponible:
            try:
                self.serial_handler.enviar_comando("LOSE")
            except Exception as e:
                print(f"Error reproduciendo derrota: {e}")

    def tocar_moneda(self):
        """Reproduce melodía de recoleccion de moneda en el buzzer"""
        if self.buzzer_disponible:
            try:
                self.serial_handler.enviar_comando("COIN")
            except Exception as e:
                print(f"Error reproduciendo moneda: {e}")
    
    def esta_disponible(self):
        """Retorna si el buzzer está disponible"""
        return self.buzzer_disponible