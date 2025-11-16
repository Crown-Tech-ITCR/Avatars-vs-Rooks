from machine import ADC, Pin
import time

class joystick:
    def __init__(self, joystick_x, joystick_y, click):
        self.x = ADC(joystick_x)
        self.y = ADC(joystick_y)
        self.click = Pin(click, Pin.IN, Pin.PULL_UP)
        self.center = 32768 
        self.dead_zone = 5000
        self.last_direction = "Centro"
        self.last_move_time = 0
        self.move_delay = 0.05  # Delay mínimo para movimiento muy rápido
        
        # Para detección de flancos del botón click
        self.ultimo_click = False
    
    def getX(self):
        return self.x.read_u16()
    
    def getY(self):
        return self.y.read_u16()
    
    def getClick(self):
        """Retorna True si el botón ESTÁ presionado actualmente (estado, no flanco)"""
        return not self.click.value()
    
    def getClickPressed(self):
        """Retorna True solo UNA VEZ cuando presionas el botón (detección de flancos)"""
        click_actual = not self.click.value()  # True = presionado
        
        # Detectar flanco de subida (no presionado -> presionado)
        if click_actual and not self.ultimo_click:
            self.ultimo_click = click_actual
            return True
        
        # Actualizar estado
        self.ultimo_click = click_actual
        return False
    
    def getDirection(self):
        x_val = self.getX()
        y_val = self.getY()
        dx = x_val - self.center
        dy = y_val - self.center
        
        if abs(dx) < self.dead_zone and abs(dy) < self.dead_zone:
            return "Centro"
        elif abs(dx) > abs(dy):
            return "Derecha" if dx > 0 else "Izquierda"
        else:
            return "Abajo" if dy > 0 else "Arriba"  # Invertido: dy positivo = Abajo
    
    def getMovement(self):
        current_time = time.time()
        direction = self.getDirection()
        
        if direction == "Centro":
            self.last_direction = "Centro"
            return None
        
        # Permitir movimiento si:
        # 1. Ha pasado el delay mínimo (movimiento continuo en misma dirección)
        # 2. Es una dirección nueva (cambio de dirección inmediato)
        if (current_time - self.last_move_time >= self.move_delay) or \
           (direction != self.last_direction):
            self.last_move_time = current_time
            self.last_direction = direction
            return direction
        
        return None