import serial
import serial.tools.list_ports
import threading
import time


class SerialHandler:
    
    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.puerto = None
        self.conectado = False
        self.callback = None
        self._thread_activo = False
        
    def buscar_pico(self):
        """"Busca el peruto en donde se encuentra conectada las raspberry pi pico w"""
        puertos = serial.tools.list_ports.comports()
        
        for puerto in puertos:
            descripcion_lower = puerto.description.lower()
            identificadores = ["usb serial", "pico", "rp2040", "raspberry"]
            
            if any(identificador in descripcion_lower for identificador in identificadores):
                return puerto.device
        
        return None
    
    def conectar(self):
        """Intenta realizar la conexión con el puerto encontrado"""
        try:
            puerto_detectado = self.buscar_pico()
            
            if puerto_detectado:
                self.puerto = serial.Serial(puerto_detectado, self.baudrate, timeout=0.1)
                self.conectado = True
                print(f"Joystick conectado en {puerto_detectado}")
                return True
            else:
                print("Joystick no detectado - usando mouse")
                return False
                
        except Exception as e:
            print(f"Error conectando joystick: {e}")
            self.conectado = False
            return False
    
    def leer_comando(self):
        """Lee el comando recibido para tomar decisiones en base a el"""
        if not self.conectado or not self.puerto:
            return None
        
        try:
            if self.puerto.in_waiting > 0:
                linea = self.puerto.readline().decode('utf-8').strip()
                if ',' in linea:
                    return linea
                    
        except serial.SerialException:
            self.conectado = False
        except UnicodeDecodeError:
            pass
        except Exception:
            self.conectado = False
        
        return None
    
    def iniciar_lectura_continua(self, callback):
        """Inicia el thread que permite la lectura continua"""
        self.callback = callback
        self._thread_activo = True
        thread = threading.Thread(target=self._bucle_lectura, daemon=True)
        thread.start()
    
    def _bucle_lectura(self):
        """Bucle de lectura para recibir los comandos"""
        while self._thread_activo:
            if self.conectado:
                comando = self.leer_comando()
                if comando and self.callback:
                    self.callback(comando)
            time.sleep(0.05)
    
    def desconectar(self):
        """Deactiva el thread"""
        self._thread_activo = False
        if self.puerto:
            self.puerto.close()
        self.conectado = False

    def enviar_comando(self, comando):
        """Envía un comando de texto a la Raspberry Pi Pico"""
        if not self.conectado or not self.puerto:
            return False  # No está conectado
        
        try:
            mensaje = f"{comando}\n" 
            self.puerto.write(mensaje.encode('utf-8')) 
            self.puerto.flush() 
            return True
        except Exception as e:
            print(f"Error enviando comando '{comando}': {e}")
            return False