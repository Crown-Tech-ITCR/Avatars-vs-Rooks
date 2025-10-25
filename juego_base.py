import tkinter as tk
import random
import numpy as np

# ==========================================================
# CONFIGURACIÓN GLOBAL DEL JUEGO
# ==========================================================

# Dimensiones del tablero
FILAS = 9
COLUMNAS = 5
TAM_CASILLA = 70

# ------------------ CONFIGURACIÓN DE NIVELES ------------------

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


# --------------------------------------------------------------
# FUNCIÓN PARA ACTUALIZAR CONFIGURACIÓN GLOBAL SEGÚN NIVEL_ACTUAL
# --------------------------------------------------------------
def aplicar_configuracion_global():
    """Actualiza las variables globales del juego según NIVEL_ACTUAL."""
    global DURACION_NIVEL, VELOCIDAD_NIVEL, TIEMPOS_REGENERACION
    conf = get_config_nivel(NIVEL_ACTUAL)
    DURACION_NIVEL = conf["duracion"]
    VELOCIDAD_NIVEL = conf["velocidad"]
    TIEMPOS_REGENERACION = conf["tiempos_regeneracion"]

# Inicializamos los valores globales una vez
aplicar_configuracion_global()

# --------------------------------------------------------------
# MATRIZ GLOBAL DEL JUEGO
# --------------------------------------------------------------
matriz_juego = [[[] for _ in range(COLUMNAS)] for _ in range(FILAS)]


# ==========================================================
# CLASES DE ENTIDADES
# ==========================================================

class Entidad:
    """Clase base para todas las entidades del juego (rooks, avatars, etc.)."""
    def __init__(self, tipo: str, vida: int = 10, dano: int = 1, movil: bool = False):
        self.tipo = tipo
        self.vida = vida
        self.dano = dano
        self.posicion = None  # (fila, col)
        self.movil = movil

    def set_pos(self, fila, col):
        self.posicion = (fila, col)

    def take_damage(self, cantidad: int):
        self.vida -= cantidad
        if self.vida <= 0:
            if self.posicion is not None:
                f, c = self.posicion
                if self in matriz_juego[f][c]:
                    matriz_juego[f][c].remove(self)
                self.posicion = None

    def tick(self):
        pass


class Rook(Entidad):
    """Rook base: no se desplaza, puede disparar si su cooldown está a cero."""
    def __init__(self, vida: int = 10, dano: int = 10, shot_cooldown_max: int = 0, costo: int = 0):
        super().__init__("rook", vida=vida, dano=dano, movil=False)
        self.shot_cooldown = 0
        self.shot_cooldown_max = shot_cooldown_max
        self.costo = costo
        self.color = "green"

    def can_shoot(self) -> bool:
        return self.shot_cooldown == 0

    def shoot(self):
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano)

    def tick(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1


# Tipos de Rooks
class RookRoca(Rook):
    def __init__(self):
        super().__init__(vida=12, dano=4, shot_cooldown_max=0, costo=100)
        self.tipo = "rook_roca"
        self.color = "gray"


class RookFuego(Rook):
    def __init__(self):
        super().__init__(vida=12, dano=8, shot_cooldown_max=0, costo=150)
        self.tipo = "rook_fuego"
        self.color = "orange"


class RookAgua(Rook):
    def __init__(self):
        super().__init__(vida=15, dano=10, shot_cooldown_max=0, costo=150)
        self.tipo = "rook_agua"
        self.color = "cyan"


class RookArena(Rook):
    def __init__(self):
        super().__init__(vida=8, dano=2, shot_cooldown_max=0, costo=50)
        self.tipo = "rook_arena"
        self.color = "yellow"


# ==========================================================
# CLASES DE AVATARS
# ==========================================================

class Avatar(Entidad):
    """Avatar base: se desplaza (movil=True) y puede regenerarse/atacar.
       move_cooldown_max = ticks a esperar después de moverse (0 = se mueve cada tick)."""
    def __init__(self, vida: int = 10, dano: int = 10, regeneracion: int = 0, move_cooldown_max: int = 1):
        super().__init__("avatar", vida=vida, dano=dano, movil=True)
        self.regeneracion = regeneracion
        self.move_cooldown_max = move_cooldown_max
        # Iniciar el cooldown igual al máximo para evitar que el avatar se mueva inmediatamente tras generarlo
        self.move_cooldown = self.move_cooldown_max

    def attack(self, objetivo):
        if hasattr(objetivo, "take_damage"):
            objetivo.take_damage(self.dano)

    def tick(self):
        if self.regeneracion and self.vida > 0:
            self.vida += self.regeneracion
        # movimiento controlado en mover_avatars mediante move_cooldown


class AvatarFlechador(Avatar):
    def __init__(self):
        # Flechador = ligeramente más lento
        super().__init__(vida=5, dano=2, regeneracion=2, move_cooldown_max=3)
        self.tipo = "avatar_flechador"
        self.color = "orange"


class AvatarEscudero(Avatar):
    def __init__(self):
        # Escudero = intermedio
        super().__init__(vida=10, dano=3, regeneracion=1, move_cooldown_max=2)
        self.tipo = "avatar_escudero"
        self.color = "blue"


class AvatarCanibal(Avatar):
    def __init__(self):
        # Caníbal = más rápido
        super().__init__(vida=25, dano=12, regeneracion=4, move_cooldown_max=0)
        self.tipo = "avatar_canibal"
        self.color = "red"


class AvatarLenador(Avatar):
    def __init__(self):
        # Leñador = rápido pero no el más rápido
        super().__init__(vida=20, dano=9, regeneracion=0, move_cooldown_max=1)
        self.tipo = "avatar_lenador"
        self.color = "sienna"


class Rafaga:
    def __init__(self, dano: int = 5):
        self.tipo = "rafaga"
        self.dano = dano


# ==========================================================
# CLASE PRINCIPAL DEL JUEGO
# ==========================================================

class Juego:
    def __init__(self, root, callback_volver_menu):
        from juego_base import aplicar_configuracion_global, DURACION_NIVEL, VELOCIDAD_NIVEL, TIEMPOS_REGENERACION
        aplicar_configuracion_global()  # Actualiza los valores globales según el nivel actual

        self.root = root
        self.root.title("Rooks vs Avatars - 4 Tipos")
        self.callback_volver_menu = callback_volver_menu

        global matriz_juego
        matriz_juego = [[[] for _ in range(COLUMNAS)] for _ in range(FILAS)]

        self.juego_terminado = False
        self.velocidad = VELOCIDAD_NIVEL
        self.tiempo_restante = DURACION_NIVEL
        self.tiempos_generacion = TIEMPOS_REGENERACION
        self._shot_tick = 0
        self.shot_interval = 3

        # ---- Sistema de monedas (placeholder) ----
        self.monedas = 500
        self.rook_seleccionado = RookArena

        # --------------------------------------------------------------
        # INTERFAZ
        # --------------------------------------------------------------
        self.frame_superior = tk.Frame(root, bg="lightgray")
        self.frame_superior.pack(fill=tk.X)

        # Label monedas
        self.label_monedas = tk.Label(
            self.frame_superior,
            text=f"💰 Monedas: {self.monedas} (no funcional)",
            font=("Arial", 12),
            bg="lightgray"
        )
        self.label_monedas.pack(side=tk.LEFT, padx=10)

        # Label tiempo
        self.label_tiempo = tk.Label(
            self.frame_superior,
            text=f"⏰ Tiempo: {self.tiempo_restante}s",
            font=("Arial", 12, "bold"),
            bg="lightgray"
        )
        self.label_tiempo.pack(side=tk.RIGHT, padx=10)

        self.crear_botones_seleccion()

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=COLUMNAS * TAM_CASILLA,
            height=FILAS * TAM_CASILLA,
            bg="lightgreen"
        )
        self.canvas.pack()

        # Dibujar cuadrícula
        for f in range(FILAS):
            for c in range(COLUMNAS):
                self.canvas.create_rectangle(
                    c * TAM_CASILLA, f * TAM_CASILLA,
                    (c + 1) * TAM_CASILLA, (f + 1) * TAM_CASILLA,
                    outline="black"
                )

        self.canvas.bind("<Button-1>", self.colocar_rook)

        # Iniciar generadores
        for tipo in ["flechador", "escudero", "canibal", "lenador"]:
            self.programar_generacion(tipo)

        self.root.after(1000, self.actualizar_tiempo)
        self.actualizar_juego()

    # --------------------------------------------------------------
    # FUNCIONES DE JUEGO
    # --------------------------------------------------------------

    def crear_botones_seleccion(self):
        frame_botones = tk.Frame(self.frame_superior, bg="lightgray")
        frame_botones.pack(side=tk.RIGHT, padx=10)
        tipos_rook = [
            ("🪨 Roca (100)", RookRoca, "gray"),
            ("🔥 Fuego (150)", RookFuego, "orange"),
            ("💧 Agua (150)", RookAgua, "cyan"),
            ("🏖️ Arena (50)", RookArena, "yellow")
        ]
        for texto, clase, color in tipos_rook:
            tk.Button(
                frame_botones,
                text=texto,
                bg=color,
                command=lambda c=clase: self.seleccionar_rook(c),
                width=12,
                font=("Arial", 9)
            ).pack(side=tk.LEFT, padx=2)

    def seleccionar_rook(self, clase_rook):
        self.rook_seleccionado = clase_rook

    def colocar_rook(self, event):
        if self.juego_terminado:
            return
        c = event.x // TAM_CASILLA
        f = event.y // TAM_CASILLA

        # No permitir colocar rook si ya hay un Avatar o un Rook en la celda
        if any(isinstance(e, (Rook, Avatar)) for e in matriz_juego[f][c]):
            # opcional: mostrar mensaje o efecto de error
            return

        rook = self.rook_seleccionado()  # Crear instancia del tipo seleccionado
        rook.set_pos(f, c)
        matriz_juego[f][c].append(rook)

    def generar_avatar(self):
        """Genera un avatar aleatorio en la última fila (abajo) en una celda libre."""
        # Intentar colocar en una columna aleatoria que esté libre de Rook/Avatar
        cols = list(range(COLUMNAS))
        random.shuffle(cols)
        for columna in cols:
            if not any(isinstance(e, (Rook, Avatar)) for e in matriz_juego[FILAS - 1][columna]):
                tipo = random.choice([AvatarFlechador, AvatarEscudero, AvatarCanibal, AvatarLenador])
                av = tipo()
                av.set_pos(FILAS - 1, columna)
                # evitar movimiento inmediato en el mismo tick
                av.move_cooldown = av.move_cooldown_max
                matriz_juego[FILAS - 1][columna].append(av)
                return
        # si no hay columna libre, no generar

    def mover_avatars(self):
        """Mueve los avatars hacia arriba y les permite atacar rooks si están frente a uno.
           No permiten moverse a una celda que ya contenga un Rook/Avatar.
           Movimiento fijo por cooldown (move_cooldown_max)."""
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Avatar):
                        # Procesar ráfagas en la casilla actual
                        rafagas_en_actual = [p for p in matriz_juego[f][c] if isinstance(p, Rafaga)]
                        if rafagas_en_actual:
                            total_dano_actual = sum(r.dano for r in rafagas_en_actual)
                            matriz_juego[f][c] = [p for p in matriz_juego[f][c] if not isinstance(p, Rafaga)]
                            e.take_damage(total_dano_actual)
                            if e.vida <= 0:
                                e.posicion = None
                                continue

                        # Si está en la primera fila, fin del juego
                        if f == 0:
                            self.game_over()
                            return

                        destino_f = f - 1

                        # Detectar rooks en actual y destino (atacar si hay)
                        rook_en_actual = [r for r in matriz_juego[f][c] if isinstance(r, Rook)]
                        rook_en_destino = [r for r in matriz_juego[destino_f][c] if isinstance(r, Rook)]

                        if rook_en_actual:
                            # si hay un rook en la misma casilla (estado indeseado), atacar y no moverse
                            objetivo = rook_en_actual[0]
                            e.attack(objetivo)
                            if objetivo.vida <= 0:
                                pass
                            continue

                        if rook_en_destino:
                            # atacar el rook en destino pero NO moverse dentro de su casilla
                            objetivo = rook_en_destino[0]
                            e.attack(objetivo)
                            continue

                        # Verificar ráfagas en la casilla destino
                        rafagas_en_destino = [p for p in matriz_juego[destino_f][c] if isinstance(p, Rafaga)]
                        if rafagas_en_destino:
                            total_dano = sum(r.dano for r in rafagas_en_destino)
                            matriz_juego[destino_f][c] = [p for p in matriz_juego[destino_f][c] if not isinstance(p, Rafaga)]
                            e.take_damage(total_dano)
                            if e.vida <= 0:
                                e.posicion = None
                                continue

                        # Si hay entidades en destino, no mover
                        if any(isinstance(x, (Rook, Avatar)) for x in matriz_juego[destino_f][c]):
                            continue

                        # Control fijo de velocidad: si move_cooldown > 0 -> decrementar y no mover
                        if getattr(e, "move_cooldown", 0) > 0:
                            e.move_cooldown -= 1
                            continue

                        # Mover avatar
                        if e in matriz_juego[f][c]:
                            matriz_juego[f][c].remove(e)
                        matriz_juego[destino_f][c].append(e)
                        e.set_pos(destino_f, c)

                        # Después de moverse, fijar cooldown (0 = se mueve cada tick)
                        e.move_cooldown = getattr(e, "move_cooldown_max", 0)

    def programar_generacion(self, tipo):
        """Programa la generación periódica de un tipo de avatar."""
        self.root.after(self.tiempos_generacion[tipo], lambda: self.generar_avatar_tipo(tipo))

    def generar_avatar_tipo(self, tipo):
        if self.juego_terminado:
            return

        # Intentar colocar en una columna aleatoria que esté libre de Rook/Avatar
        cols = list(range(COLUMNAS))
        random.shuffle(cols)
        clase = {
            "flechador": AvatarFlechador,
            "escudero": AvatarEscudero,
            "canibal": AvatarCanibal,
            "lenador": AvatarLenador
        }.get(tipo)

        if clase is not None:
            for columna in cols:
                if not any(isinstance(e, (Rook, Avatar)) for e in matriz_juego[FILAS - 1][columna]):
                    av = clase()
                    av.set_pos(FILAS - 1, columna)
                    # evitar movimiento inmediato en el mismo tick
                    av.move_cooldown = av.move_cooldown_max
                    matriz_juego[FILAS - 1][columna].append(av)
                    break

        self.programar_generacion(tipo)

    def programar_generacion(self, tipo):
        self.root.after(self.tiempos_generacion[tipo], lambda: self.generar_avatar_tipo(tipo))

    def mover_avatars(self):
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Avatar):
                        rafagas = [r for r in matriz_juego[f][c] if isinstance(r, Rafaga)]
                        if rafagas:
                            total = sum(r.dano for r in rafagas)
                            matriz_juego[f][c] = [p for p in matriz_juego[f][c] if not isinstance(p, Rafaga)]
                            e.take_damage(total)
                            if e.vida <= 0:
                                continue
                        if f == 0:
                            self.game_over()
                            return
                        destino = f - 1
                        rook_dest = [r for r in matriz_juego[destino][c] if isinstance(r, Rook)]
                        if rook_dest:
                            e.attack(rook_dest[0])
                            continue
                        matriz_juego[f][c].remove(e)
                        matriz_juego[destino][c].append(e)
                        e.set_pos(destino, c)

    def disparar(self):
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Rook):
                        e.tick()
                        if e.can_shoot() and f + 1 < FILAS:
                            if not any(isinstance(x, Rafaga) for x in matriz_juego[f + 1][c]):
                                matriz_juego[f + 1][c].append(e.shoot())

    def mover_rafagas(self):
        for f in range(FILAS - 1, -1, -1):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Rafaga):
                        matriz_juego[f][c].remove(e)
                        if f + 1 < FILAS:
                            matriz_juego[f + 1][c].append(e)

    def dibujar(self):
        self.canvas.delete("entidad")
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in matriz_juego[f][c]:
                    cx = c * TAM_CASILLA + TAM_CASILLA // 2
                    cy = f * TAM_CASILLA + TAM_CASILLA // 2
                    if isinstance(e, Rook):
                        self.canvas.create_oval(cx - 15, cy - 15, cx + 15, cy + 15, fill=e.color, tags="entidad")
                    elif isinstance(e, Avatar):
                        self.canvas.create_rectangle(cx - 15, cy - 15, cx + 15, cy + 15, fill=e.color, tags="entidad")
                    elif isinstance(e, Rafaga):
                        self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="yellow", tags="entidad")

    def actualizar_juego(self):
        if self.juego_terminado:
            return
        self.mover_avatars()
        self.mover_rafagas()
        self._shot_tick += 1
        if self._shot_tick >= self.shot_interval:
            self.disparar()
            self._shot_tick = 0
        self.dibujar()
        self.root.after(self.velocidad, self.actualizar_juego)

    def finalizar_nivel(self):
        if self.juego_terminado:
            return
        self.juego_terminado = True
        self.canvas.create_text(
            COLUMNAS * TAM_CASILLA // 2, FILAS * TAM_CASILLA // 2,
            text=f"🎉 ¡Nivel {NIVEL_ACTUAL} completado! 🎉",
            font=("Arial", 20, "bold"), fill="blue"
        )
        self.root.after(3000, self.volver_al_menu)

    def game_over(self):
        self.juego_terminado = True
        self.canvas.create_text(
            COLUMNAS * TAM_CASILLA // 2, FILAS * TAM_CASILLA // 2,
            text="💀 GAME OVER 💀",
            font=("Arial", 24, "bold"), fill="red"
        )
        self.root.after(3000, self.volver_al_menu)

    def volver_al_menu(self):
        try:
            if self.callback_volver_menu:
                self.root.destroy()
                self.callback_volver_menu()
            else:
                self.root.destroy()
        except:
            pass


# ==========================================================
# EJECUCIÓN DIRECTA (para pruebas)
# ==========================================================
if __name__ == "__main__":
    root = tk.Tk()
    Juego(root, None)
    root.mainloop()
