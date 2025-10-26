from Entidades import Avatar, Rafaga, Rook
import numpy as np

class GameLogic:
    """Clase que maneja toda la lógica principal del juego."""
    
    def __init__(self):
        self.shot_tick = 0
        self.shot_interval = 12
        self.juego_terminado = False
        self.avatars_eliminados = 0
        self.puntos_vida_acumulados = 0
        
    def mover_avatars(self, on_game_over_callback=None):
        """Mueve todos los avatars y maneja colisiones con rooks y rafagas."""
        
        for f in range(FILAS):
            for c in range(COLUMNAS):
                # Crear copia para evitar problemas de iteración
                entidades_en_celda = list(matriz_juego[f][c])
                
                for e in entidades_en_celda:
                    if isinstance(e, Avatar):
                        # Actualizar cooldown de movimiento
                        e.tick()
                        
                        # 1. VERIFICAR colisiones con rafagas en la posición ACTUAL
                        rafagas_actual = [r for r in matriz_juego[f][c] if isinstance(r, Rafaga)]
                        if rafagas_actual:
                            total_dano = sum(r.dano for r in rafagas_actual)
                            # Eliminar todas las ráfagas que impactaron
                            for rafaga in rafagas_actual:
                                if rafaga in matriz_juego[f][c]:
                                    matriz_juego[f][c].remove(rafaga)
                        
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
                        
                        # Verificar si puede moverse (cooldown)
                        if not e.can_move():
                            continue
                        
                        destino = f - 1
                        
                        # Verificar colisión con rook en la fila de destino
                        rook_dest = [r for r in matriz_juego[destino][c] if isinstance(r, Rook)]
                        if rook_dest:
                            # Avatar ataca al rook pero NO se mueve
                            e.attack(rook_dest[0])
                            continue
                        
                        # Verificar si hay otro avatar en la casilla destino
                        avatar_dest = [a for a in matriz_juego[destino][c] if isinstance(a, Avatar)]
                        if avatar_dest:
                            # No puede moverse, casilla ocupada por otro avatar
                            continue
                        
                        # 2. VERIFICAR colisiones con rafagas en la posición DESTINO
                        rafagas_destino = [r for r in matriz_juego[destino][c] if isinstance(r, Rafaga)]
                        if rafagas_destino:
                            total_dano_destino = sum(r.dano for r in rafagas_destino)
                            # Eliminar ráfagas del destino
                            for rafaga in rafagas_destino:
                                if rafaga in matriz_juego[destino][c]:
                                    matriz_juego[destino][c].remove(rafaga)
                        
                            e.take_damage(total_dano_destino)
                            self.puntos_vida_acumulados += total_dano_destino
                            if e.vida <= 0:
                                self.avatars_eliminados += 1
                                # Remover avatar de posición actual si murió
                                if e in matriz_juego[f][c]:
                                    matriz_juego[f][c].remove(e)
                                continue
                        
                        # 3. MOVER avatar si no murió
                        if e in matriz_juego[f][c]:
                            matriz_juego[f][c].remove(e)
                            matriz_juego[destino][c].append(e)
                            e.set_pos(destino, c)
                            e.reset_move_cooldown()  # Reiniciar cooldown después de moverse

    def mover_rafagas(self):
        """Mueve todas las rafagas hacia abajo y verifica colisiones."""
        # Recorrer desde abajo hacia arriba para evitar procesar la misma ráfaga dos veces
        for f in range(FILAS - 1, -1, -1):
            for c in range(COLUMNAS):
                # Crear copia de la lista para evitar problemas al modificar durante iteración
                entidades_en_celda = list(matriz_juego[f][c])
                
                for e in entidades_en_celda:
                    if isinstance(e, Rafaga):
                        # Actualizar cooldown de movimiento
                        e.tick()
                        
                        # VERIFICAR COLISIÓN CON AVATARS EN LA MISMA CELDA
                        avatars_en_celda = [avatar for avatar in matriz_juego[f][c] if isinstance(avatar, Avatar)]
                        
                        if avatars_en_celda:
                            # COLISIÓN DETECTADA: Aplicar daño y eliminar ráfaga
                            for avatar in avatars_en_celda:
                                avatar.take_damage(e.dano)
                                self.puntos_vida_acumulados += e.dano
                                if avatar.vida <= 0:
                                    self.avatars_eliminados += 1
                            
                            # ELIMINAR LA RÁFAGA tras el impacto
                            if e in matriz_juego[f][c]:
                                matriz_juego[f][c].remove(e)
                            continue  # NO mover esta ráfaga
                        
                        # Verificar si puede moverse (cooldown)
                        if not e.can_move():
                            continue
                        
                        # Si no hay colisión, mover la ráfaga hacia abajo
                        if e in matriz_juego[f][c]:
                            matriz_juego[f][c].remove(e)
                            destino_f = f + 1
                            
                            if destino_f < FILAS:
                                # Verificar colisión en destino ANTES de mover
                                avatars_en_destino = [avatar for avatar in matriz_juego[destino_f][c] if isinstance(avatar, Avatar)]
                                
                                if avatars_en_destino:
                                    # COLISIÓN EN DESTINO: Aplicar daño y destruir ráfaga
                                    for avatar in avatars_en_destino:
                                        avatar.take_damage(e.dano)
                                        self.puntos_vida_acumulados += e.dano
                                        if avatar.vida <= 0:
                                            self.avatars_eliminados += 1
                                    # La ráfaga se destruye al impactar, NO se mueve
                                else:
                                    # NO hay colisión: mover ráfaga normalmente
                                    matriz_juego[destino_f][c].append(e)
                                    e.set_pos(destino_f, c)
                                    e.reset_move_cooldown()  # Reiniciar cooldown después de moverse
                            # Si destino_f >= FILAS, la ráfaga sale del tablero y se elimina

    def disparar_rooks(self):
        """Hace que todos los rooks disparen si pueden."""
        for f in range(FILAS):
            for c in range(COLUMNAS):
                # Crear copia para evitar problemas de iteración
                entidades_en_celda = list(matriz_juego[f][c])
                
                for e in entidades_en_celda:
                    if isinstance(e, Rook):
                        e.tick()  # Actualizar cooldown
                        
                        if e.can_shoot():
                            # La ráfaga aparece en la fila siguiente hacia abajo
                            destino_f = f + 1
                            
                            if destino_f < FILAS:
                                # Verificar si hay avatar en la celda de destino (disparo directo)
                                avatars_adyacentes = [avatar for avatar in matriz_juego[destino_f][c] if isinstance(avatar, Avatar)]
                                
                                if avatars_adyacentes:
                                    # DISPARO DIRECTO: Aplicar daño inmediatamente
                                    rafaga_temporal = e.shoot()
                                    if rafaga_temporal:
                                        for avatar in avatars_adyacentes:
                                            avatar.take_damage(rafaga_temporal.dano)
                                            self.puntos_vida_acumulados += rafaga_temporal.dano
                                            if avatar.vida <= 0:
                                                self.avatars_eliminados += 1
                                        # NO agregar la ráfaga al tablero - se destruye inmediatamente
                                else:
                                    # NO hay avatar: crear ráfaga normalmente
                                    # Verificar que no haya otra ráfaga ya en el destino
                                    rafagas_existentes = [r for r in matriz_juego[destino_f][c] if isinstance(r, Rafaga)]
                                    if not rafagas_existentes:
                                        rafaga = e.shoot()
                                        if rafaga:
                                            rafaga.set_pos(destino_f, c)
                                            rafaga.reset_move_cooldown()  # Iniciar con cooldown completo
                                            matriz_juego[destino_f][c].append(rafaga)
                                            
    def actualizar_logica_juego(self, on_game_over_callback=None):
        """Actualiza toda la lógica del juego en un tick."""
        if self.juego_terminado:
            return
        
        # ORDEN CRÍTICO PARA GARANTIZAR DETECCIÓN DE COLISIONES:
        # 1. Disparar rooks (con detección inmediata para avatars adyacentes)
        self.shot_tick += 1
        if self.shot_tick >= self.shot_interval:
            self.disparar_rooks()
            self.shot_tick = 0
        
        # 2. Mover avatars (verificando colisiones con rafagas)
        self.mover_avatars(on_game_over_callback)
        
        # 3. Mover ráfagas (con detección de colisiones durante el movimiento)
        self.mover_rafagas()

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
VELOCIDAD_BASE = 250           # velocidad base en ms (para el bucle principal)
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