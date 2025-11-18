from machine import Pin, PWM
import time

# Diccionario de frecuencias de notas musicales
NOTAS = {
    'REST': 0,
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
    'C6': 1047, 'D6': 1175, 'E6': 1319, 'F6': 1397, 'G6': 1568, 'A6': 1760, 'B6': 1976
}

class buzzer:
    def __init__(self, pin=15, volumen_global=4587):
        # Configurar pin como salida en LOW 
        self.pin_buzzer = Pin(pin, Pin.OUT)
        self.pin_buzzer.value(0)
        
        # Luego configurar PWM
        self.buzzer = PWM(self.pin_buzzer)
        self.buzzer.freq(1000)
        self.buzzer.duty_u16(0)
        
        # Volumen 
        self.volumen_global = volumen_global
    
    def tocar_nota(self, frecuencia, duracion_seg, volumen=None):
        """Toca una nota con control de volumen"""
        if volumen is None:
            volumen = self.volumen_global
        
        if frecuencia > 0:
            self.buzzer.freq(frecuencia)
            self.buzzer.duty_u16(volumen)
            time.sleep(duracion_seg)
            # Pequeña pausa entre notas para evitar saturación
            self.buzzer.duty_u16(0)
            time.sleep(0.01)
        else:
            # Silencio (REST)
            self.buzzer.duty_u16(0)
            time.sleep(duracion_seg)
    
    def melodia_victoria(self):
        """Melodía de victoria - Fanfarria Triunfal"""
        secuencia = [
            ('C5', 0.128), ('E5', 0.128), ('G5', 0.128), ('C6', 0.298),
            ('REST', 0.085),
            ('G5', 0.128), ('C6', 0.34),
            ('REST', 0.128),
            ('E5', 0.102), ('G5', 0.102), ('C6', 0.102), ('E6', 0.425),
            ('REST', 0.085),
            ('C6', 0.17), ('G5', 0.17), ('C6', 0.51)
        ]
        for nota, duracion in secuencia:
            self.tocar_nota(NOTAS[nota], duracion)
    
    def melodia_derrota(self):
        """Melodía de derrota - Lamento Dramático"""
        secuencia = [
            ('G5', 0.34), ('F5', 0.34), ('E5', 0.34),
            ('REST', 0.085),
            ('D5', 0.298), ('C5', 0.298), ('B4', 0.298),
            ('REST', 0.085),
            ('A4', 0.255), ('G4', 0.255), ('F4', 0.255),
            ('REST', 0.085),
            ('E4', 0.425), ('D4', 0.425), ('C4', 0.68)
        ]
        for nota, duracion in secuencia:
            self.tocar_nota(NOTAS[nota], duracion)
    
    def melodia_moneda(self):
        """Melodía de recolección de moneda estilo Mario"""
        secuencia = [
            ('B5', 0.068), ('E6', 0.213)
        ]
        for nota, duracion in secuencia:
            self.tocar_nota(NOTAS[nota], duracion)
    
    def apagar(self):
        """Detiene el buzzer"""
        self.buzzer.duty_u16(0)