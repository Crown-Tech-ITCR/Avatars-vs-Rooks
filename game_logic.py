from Entidades import Avatar, Rafaga, Rook
import numpy as np

class GameLogic:
    """Clase que maneja toda la lógica principal del juego."""
    
    def __init__(self):
        self.shot_tick = 0
        self.shot_interval = 3
        self.juego_terminado = False
        self.avatars_eliminados = 0
        self.puntos_vida_acumulados = 0
        
    def mover_avatars(self, on_game_over_callback=None):
        """Mueve todos los avatars y maneja colisiones con rooks y rafagas."""
        
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Avatar):
                        # Verificar colisiones con rafagas
                        rafagas = [r for r in matriz_juego[f][c] if isinstance(r, Rafaga)]
                        if rafagas:
                            total_dano = sum(r.dano for r in rafagas)
                            # Eliminar rafagas de la celda
                            matriz_juego[f][c] = [p for p in matriz_juego[f][c] if not isinstance(p, Rafaga)]
                            e.take_damage(total_dano)
                            self.puntos_vida_acumulados += total_dano
                            if e.vida <= 0:
                                self.avatars_eliminados += 1
                                continue
                        
                        # Verificar si el avatar llegó al borde superior (game over)
                        if f == 0:
                            if on_game_over_callback:
                                on_game_over_callback()
                            return
                        
                        # Verificar colisión con rook en la fila de destino
                        destino = f - 1
                        rook_dest = [r for r in matriz_juego[destino][c] if isinstance(r, Rook)]
                        if rook_dest:
                            # Avatar ataca al rook
                            e.attack(rook_dest[0])
                            continue
                        
                        # Mover avatar una fila hacia arriba
                        matriz_juego[f][c].remove(e)
                        matriz_juego[destino][c].append(e)
                        e.set_pos(destino, c)

    def disparar_rooks(self):
        """Hace que todos los rooks disparen si pueden."""
        
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Rook):
                        e.tick()  # Actualizar cooldown
                        # Verificar si puede disparar y hay espacio para la rafaga
                        if e.can_shoot() and f + 1 < FILAS:
                            # No disparar si ya hay una rafaga en la celda de destino
                            if not any(isinstance(x, Rafaga) for x in matriz_juego[f + 1][c]):
                                rafaga = e.shoot()
                                matriz_juego[f + 1][c].append(rafaga)

    def mover_rafagas(self):
        """Mueve todas las rafagas hacia abajo."""
        
        # Iterar de abajo hacia arriba para evitar mover la misma rafaga dos veces
        for f in range(FILAS - 1, -1, -1):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Rafaga):
                        matriz_juego[f][c].remove(e)
                        # Mover rafaga una fila hacia abajo
                        if f + 1 < FILAS:
                            matriz_juego[f + 1][c].append(e)
                        # Si la rafaga sale del tablero, simplemente se elimina

    def actualizar_logica_juego(self, on_game_over_callback=None):
        """Actualiza toda la lógica del juego en un tick."""
        if self.juego_terminado:
            return
            
        # Mover avatars y verificar game over
        self.mover_avatars(on_game_over_callback)
        
        # Mover rafagas
        self.mover_rafagas()
        
        # Disparar rooks según el intervalo
        self.shot_tick += 1
        if self.shot_tick >= self.shot_interval:
            self.disparar_rooks()
            self.shot_tick = 0

    def finalizar_juego(self):
        """Marca el juego como terminado."""
        self.juego_terminado = True

    def reiniciar_logica(self):
        """Reinicia la lógica del juego."""
        self.shot_tick = 0
        self.juego_terminado = False
        reset_matriz_juego()

    def get_avatars_eliminados(self):
        """Devuelve el número de avatars eliminados."""
        return self.avatars_eliminados

    def get_puntos_vida_acumulados(self):
        """Devuelve los puntos de vida acumulados."""
        return self.puntos_vida_acumulados

    def reset_estadisticas(self):
        """Reinicia las estadísticas del juego."""
        self.avatars_eliminados = 0
        self.puntos_vida_acumulados = 0

#CONFIGURACIONES DEL JUEGO

# Dimensiones del tablero
FILAS = 9
COLUMNAS = 5
TAM_CASILLA = 70

# Nivel actual (modificado desde MainMenu)
NIVEL_ACTUAL = 1

# Configuración base
DURACION_BASE = 60             # duración base en segundos del nivel 1
VELOCIDAD_BASE = 1000           # velocidad base en ms (para el bucle principal)
AUMENTO_DURACION = 0.25         # +25% duración por nivel
AUMENTO_VELOCIDAD = 0.15        # +15% de rapidez (menos tiempo entre actualizaciones)

# Tiempos base de regeneración (ms)
TIEMPOS_BASE_AVATARS = {
    "flechador": 3000,
    "escudero": 4000,
    "lenador": 10000,
    "canibal": 12000
}

# --------------------------------------------------------------
# FUNCIONES PARA CALCULAR CONFIGURACIONES SEGÚN EL NIVEL
# --------------------------------------------------------------

def calcular_duracion_nivel(nivel: int) -> int:
    """Devuelve la duración del nivel (en segundos)."""
    return int(DURACION_BASE * ((1 + AUMENTO_DURACION) ** (nivel - 1)))


def calcular_velocidad_nivel(nivel: int) -> int:
    """Devuelve la velocidad de actualización (ms)."""
    return int(VELOCIDAD_BASE * ((1 - AUMENTO_VELOCIDAD) ** (nivel - 1)))


def calcular_tiempos_regeneracion(nivel: int) -> dict:
    """Devuelve los tiempos de regeneración por tipo de avatar (ms)."""
    factor = (1 - AUMENTO_VELOCIDAD) ** (nivel - 1)
    return {k: int(v * factor) for k, v in TIEMPOS_BASE_AVATARS.items()}


def get_config_nivel(nivel: int) -> dict:
    """Devuelve toda la configuración derivada del nivel."""
    return {
        "duracion": calcular_duracion_nivel(nivel),
        "velocidad": calcular_velocidad_nivel(nivel),
        "tiempos_regeneracion": calcular_tiempos_regeneracion(nivel)
    }


# FUNCIÓN PARA ACTUALIZAR CONFIGURACIÓN GLOBAL SEGÚN NIVEL_ACTUAL

def aplicar_configuracion_global():
    """Actualiza las variables globales del juego según NIVEL_ACTUAL."""
    global DURACION_NIVEL, VELOCIDAD_NIVEL, TIEMPOS_REGENERACION
    conf = get_config_nivel(NIVEL_ACTUAL)
    DURACION_NIVEL = conf["duracion"]
    VELOCIDAD_NIVEL = conf["velocidad"]
    TIEMPOS_REGENERACION = conf["tiempos_regeneracion"]

# Inicializamos los valores globales una vez
aplicar_configuracion_global()


# Matriz global del juego
matriz_juego = [[[] for _ in range(COLUMNAS)] for _ in range(FILAS)]

def reset_matriz_juego():
    """Reinicia la matriz del juego."""
    global matriz_juego
    matriz_juego = [[[] for _ in range(COLUMNAS)] for _ in range(FILAS)]


def get_matriz_juego():
    """Devuelve la matriz actual del juego."""
    return matriz_juego


def set_nivel_actual(nivel: int):
    """Establece el nivel actual del juego."""
    global NIVEL_ACTUAL
    NIVEL_ACTUAL = nivel
    aplicar_configuracion_global()