class InputHandler:
    
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        
        self.cursor_fila = 0
        self.cursor_columna = 0
        
        self.joystick_detectado = False
        
        self.callback_mover_cursor = None
        self.callback_click_joystick = None
        
        self.ultimo_click_joystick = False

        self.ultima_direccion = "Centro"
    
    def marcar_joystick_detectado(self):
        self.joystick_detectado = True
        print("🎮 Joystick detectado - cursor activado")
    
    def hay_joystick(self):
        return self.joystick_detectado
    
    def set_callback_mover_cursor(self, callback):
        self.callback_mover_cursor = callback
    
    def set_callback_click_joystick(self, callback):
        self.callback_click_joystick = callback
    
    def mover_cursor(self, direccion):
        if direccion == "Arriba" and self.cursor_fila > 0:
            self.cursor_fila -= 1
        elif direccion == "Abajo" and self.cursor_fila < self.filas - 1:
            self.cursor_fila += 1
        elif direccion == "Izquierda" and self.cursor_columna > 0:
            self.cursor_columna -= 1
        elif direccion == "Derecha" and self.cursor_columna < self.columnas - 1:
            self.cursor_columna += 1
        
        if self.callback_mover_cursor:
            self.callback_mover_cursor(self.cursor_fila, self.cursor_columna)
    
    def procesar_comando_joystick(self, comando):
        try:
            partes = comando.split(',')
            if len(partes) != 2:
                return
            
            direccion = partes[0]
            click = int(partes[1])
            
            if direccion != "Centro":
                if self.ultima_direccion == "Centro":
                    self.mover_cursor(direccion)
                    self.ultima_direccion = direccion
                else:
                    #volvio al centro, actualizamos ultima direccion para permitir movimiento
                    self.ultima_direccion = "Centro"

            if click == 1 :
                if not self.ultimo_click_joystick:
                    if self.callback_click_joystick:
                        self.callback_click_joystick(self.cursor_fila, self.cursor_columna)
                self.ultimo_click_joystick = True
            else:
                self.ultimo_click_joystick = False
            
        except Exception as e:
            print(f"Error procesando comando: {e}")
    
    def get_posicion_cursor(self):
        return self.cursor_fila, self.cursor_columna