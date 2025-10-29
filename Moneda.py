import time

class Moneda:
    "Clase que representa una moneda en el tablero."
    
    def __init__(self, valor, fila, col, tiempo_limite):
        """
        Inicializa una moneda.
        
        Args:
            valor (int): Valor de la moneda (25, 50 o 100)
            fila (int): Fila en el tablero
            col (int): Columna en el tablero
            tiempo_limite (float): Tiempo en segundos antes de desaparecer
        """
        self.tipo = "moneda"
        self.valor = valor
        self.posicion = (fila, col)
        self.tiempo_creacion = time.time()
        self.tiempo_limite = tiempo_limite
        self.activa = True
        
        # Posición visual
        from game_logic import TAM_CASILLA
        self.x_visual = col * TAM_CASILLA + TAM_CASILLA // 2
        self.y_visual = fila * TAM_CASILLA + TAM_CASILLA // 2
    
    def esta_expirada(self):
        "Verifica si la moneda ha expirado."
        tiempo_transcurrido = time.time() - self.tiempo_creacion
        return tiempo_transcurrido >= self.tiempo_limite
    
    def get_tiempo_restante(self):
        "Retorna el tiempo restante antes de expirar."
        tiempo_transcurrido = time.time() - self.tiempo_creacion
        return max(0, self.tiempo_limite - tiempo_transcurrido)
    
    def recoger(self):
        "Marca la moneda como inactiva (recogida)."
        self.activa = False
        return self.valor