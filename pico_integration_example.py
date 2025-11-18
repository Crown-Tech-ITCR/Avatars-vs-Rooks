"""
Ejemplo de integración de Raspberry Pi Pico W con el juego
Este archivo muestra cómo integrar la comunicación en diferentes partes del juego
"""

import tkinter as tk
from pico_communication import PicoCommunication

class GameWithPico:
    """Ejemplo de cómo integrar Pico W en el juego"""
    
    def __init__(self, root):
        self.root = root
        self.pico = None
        
        # Intentar conectar con Pico W
        self.setup_pico_connection()
        
    def setup_pico_connection(self):
        """Configura la conexión con la Pico W"""
        # Cambia esta IP por la que te muestre tu Pico W
        PICO_IP = "192.168.1.100"  # ← IMPORTANTE: Cambiar por tu IP
        PICO_PORT = 8080
        
        self.pico = PicoCommunication(pico_ip=PICO_IP, pico_port=PICO_PORT)
        
        # Registrar callbacks para eventos de la Pico W
        self.pico.on_event("button_press", self.on_pico_button)
        self.pico.on_event("sensor_data", self.on_pico_sensor)
        
        # Intentar conectar
        if self.pico.connect():
            print("✓ Pico W integrada exitosamente")
            # Enviar señal de inicio
            self.pico.send_command("game_state", {"status": "started"})
        else:
            print("⚠ Juego iniciado sin Pico W")
            self.pico = None
    
    # ========== CALLBACKS DE EVENTOS DE PICO W ==========
    
    def on_pico_button(self, data):
        """Maneja eventos de botones desde la Pico W"""
        button = data.get("button", "unknown")
        print(f"Botón de Pico W presionado: {button}")
        
        # Ejemplo: diferentes acciones según el botón
        if button == "A":
            self.action_place_rook()
        elif button == "B":
            self.action_pause_game()
    
    def on_pico_sensor(self, data):
        """Maneja datos de sensores desde la Pico W"""
        print(f"Datos de sensor: {data}")
        # Aquí puedes procesar datos de sensores
    
    # ========== MÉTODOS DE EJEMPLO DEL JUEGO ==========
    
    def action_place_rook(self):
        """Acción: colocar un rook"""
        print("Acción: Colocar rook desde Pico W")
        # Aquí llamarías a tu lógica de colocar rook
    
    def action_pause_game(self):
        """Acción: pausar el juego"""
        print("Acción: Pausar juego desde Pico W")
        # Aquí llamarías a tu lógica de pausa
    
    # ========== ENVIAR ESTADO DEL JUEGO A PICO W ==========
    
    def update_game_state(self, level, score, lives):
        """Envía el estado actual del juego a la Pico W"""
        if self.pico and self.pico.is_connected():
            self.pico.send_command("game_state", {
                "level": level,
                "score": score,
                "lives": lives
            })
    
    def on_game_over(self, won):
        """Notifica a la Pico W cuando el juego termina"""
        if self.pico and self.pico.is_connected():
            self.pico.send_command("game_over", {
                "won": won
            })
    
    def on_level_complete(self, level):
        """Notifica a la Pico W cuando se completa un nivel"""
        if self.pico and self.pico.is_connected():
            self.pico.send_command("level_complete", {
                "level": level
            })
            # Efecto visual en Pico W
            self.pico.send_command("led_blink", {"duration": 0.3})
    
    def cleanup(self):
        """Limpia recursos al cerrar el juego"""
        if self.pico:
            self.pico.disconnect()


# ========== INTEGRACIÓN CON GAME_INTERFACE.PY ==========

"""
Para integrar con tu game_interface.py, agrega esto en la clase GameInterface:

1. En __init__:
    self.pico = None
    self.setup_pico()

2. Agrega este método:
    def setup_pico(self):
        from pico_communication import PicoCommunication
        
        PICO_IP = "192.168.1.100"  # Cambiar por tu IP
        self.pico = PicoCommunication(pico_ip=PICO_IP, pico_port=8080)
        
        # Registrar eventos
        self.pico.on_event("button_press", self.handle_pico_button)
        
        # Conectar
        if self.pico.connect():
            print("✓ Pico W conectada")
        else:
            self.pico = None
    
    def handle_pico_button(self, data):
        button = data.get("button")
        
        if button == "A":
            # Colocar rook del tipo seleccionado
            if hasattr(self, 'colocar_rook_seleccionado'):
                self.colocar_rook_seleccionado()
        
        elif button == "B":
            # Pausar/reanudar
            self.toggle_pause()

3. En el método de actualización del juego (donde actualizas puntos, vida, etc.):
    if self.pico and self.pico.is_connected():
        self.pico.send_command("game_state", {
            "score": self.puntos,
            "level": self.nivel,
            "lives": self.vidas
        })

4. Al cerrar el juego (en volver_menu o similar):
    if self.pico:
        self.pico.disconnect()
"""


# ========== EJEMPLO SIMPLE DE PRUEBA ==========

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba Pico W")
    root.geometry("400x300")
    
    # Crear instancia
    game = GameWithPico(root)
    
    # Botones de prueba
    tk.Button(
        root,
        text="Enviar LED ON",
        command=lambda: game.pico.send_command("led_on") if game.pico else None
    ).pack(pady=10)
    
    tk.Button(
        root,
        text="Enviar LED OFF",
        command=lambda: game.pico.send_command("led_off") if game.pico else None
    ).pack(pady=10)
    
    tk.Button(
        root,
        text="Enviar Estado del Juego",
        command=lambda: game.update_game_state(level=1, score=100, lives=3)
    ).pack(pady=10)
    
    tk.Label(
        root,
        text="Presiona los botones físicos de la Pico W\npara ver eventos en la consola",
        pady=20
    ).pack()
    
    # Al cerrar
    def on_closing():
        game.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
