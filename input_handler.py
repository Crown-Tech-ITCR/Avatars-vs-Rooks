import random

class InputHandler:
    
    def __init__(self, filas, columnas):
        self.instance_id = random.randint(1000, 9999)  # ID único para rastrear instancias
        print(f"🆔 InputHandler creado con ID: {self.instance_id}")
        
        self.filas = filas
        self.columnas = columnas
        
        self.cursor_fila = 0
        self.cursor_columna = 0
        
        self.joystick_detectado = False
        
        #callbacks de cada componente
        self.callback_mover_cursor = None
        self.callback_click_joystick = None
        self.callback_boton_rook = None
        self.callback_boton_pausa = None
        self.callback_boton_monedas = None
        
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
    
    def set_callback_boton_pausa(self, callback):
        """Configura callback para el botón de pausa"""
        self.callback_boton_pausa = callback   

    def set_callback_boton_monedas(self,callback):
         """Configura callback para el botón de monedas"""
         self.callback_boton_monedas = callback
        
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
            
            # Detectar comandos de botones (BTN,ARENA / BTN,ROCA / BTN,PAUSA / etc)
            if parte1 == "BTN":
                # Botón de pausa tiene prioridad
                if parte2 == "PAUSA":
                    print(f"[ID:{self.instance_id}] Botón de pausa detectado")
                    if self.callback_boton_pausa:
                        self.callback_boton_pausa()
                    else:
                        print(f"[ID:{self.instance_id}] No hay callback configurado para pausa")
                    return
                
                # Botón de monedas
                if parte2 == "MONEDA":
                    print(f"[ID:{self.instance_id}] Botón de monedas detectado")
                    if self.callback_boton_monedas:
                        self.callback_boton_monedas()
                    else:
                        print(f"[ID:{self.instance_id}] No hay callback configurado para monedas")
                    return
                
                # Botones de rooks
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