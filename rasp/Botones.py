from machine import Pin

class botones:
    def __init__(self, pin_arena=16, pin_roca=17, pin_fuego=18, pin_agua=19):
        self.btn_arena = Pin(pin_arena, Pin.IN, Pin.PULL_UP)
        self.btn_roca = Pin(pin_roca, Pin.IN, Pin.PULL_UP)
        self.btn_fuego = Pin(pin_fuego, Pin.IN, Pin.PULL_UP)
        self.btn_agua = Pin(pin_agua, Pin.IN, Pin.PULL_UP)
        
        # Estados previos para detectar flancos
        self.ultimo_arena = 1
        self.ultimo_roca = 1
        self.ultimo_fuego = 1
        self.ultimo_agua = 1
    
    def leer_estado(self):
        """Retorna el botón presionado (flanco de subida)"""
        arena = not self.btn_arena.value()
        roca = not self.btn_roca.value()
        fuego = not self.btn_fuego.value()
        agua = not self.btn_agua.value()
        
        boton_presionado = None
        
        # Detectar flancos (0 → 1)
        if arena and not self.ultimo_arena:
            boton_presionado = "ARENA"
        elif roca and not self.ultimo_roca:
            boton_presionado = "ROCA"
        elif fuego and not self.ultimo_fuego:
            boton_presionado = "FUEGO"
        elif agua and not self.ultimo_agua:
            boton_presionado = "AGUA"
        
        # Actualizar estados
        self.ultimo_arena = arena
        self.ultimo_roca = roca
        self.ultimo_fuego = fuego
        self.ultimo_agua = agua
        
        return boton_presionado