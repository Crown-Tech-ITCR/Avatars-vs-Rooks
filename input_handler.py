class InputHandler:
    
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        
        self.cursor_fila = 0
        self.cursor_columna = 0
        
        self.joystick_detectado = False
        
        #callbacks de cada componente
        self.callback_mover_cursor = None
        self.callback_click_joystick = None
        self.callback_boton_rook = None
        
        self.ultimo_click_joystick = False

        self.ultima_direccion = "Centro"
    
    def marcar_joystick_detectado(self):
        self.joystick_detectado = True
        print("🎮 Joystick detectado - cursor activado")
    
    def hay_joystick(self):
        return self.joystick_detectado
    
    def set_callback_mover_cursor(self, callback):
        """Configura callback para leer el movimiento del cursor del joystick"""
        self.callback_mover_cursor = callback
    
    def set_callback_click_joystick(self, callback):
        """Configura callback para el click de joystick"""
        self.callback_click_joystick = callback

    def set_callback_boton_rook(self, callback):
        """Configura callback para botones de selección de rooks"""
        self.callback_boton_rook = callback
    
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
            
            parte1 = partes[0]
            parte2 = partes[1]
            
            # Detectar comandos de botones (BTN,ARENA / BTN,ROCA / etc)
            if parte1 == "BTN":
                if self.callback_boton_rook:
                    self.callback_boton_rook(parte2)
                return
            
            # Comandos normales de joystick
            direccion = parte1
            click = int(parte2)
            
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