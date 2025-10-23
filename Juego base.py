import tkinter as tk
import random
import numpy as np

# Constantes del juego
FILAS = 9      # 9 filas (vertical)
COLUMNAS = 5   # 5 columnas (horizontal)
TAM_CASILLA = 70
VELOCIDAD = 1000  # ms entre actualizaciones

# Matriz del juego (9x5)
matriz_juego = [[[] for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Clases de entidades
class Entidad:
    """Clase base para todas las entidades del juego (rooks, avatars, etc.)."""
    def __init__(self, tipo: str, vida: int = 10, dano: int = 1, movil: bool = False):
        self.tipo = tipo
        self.vida = vida
        self.dano = dano
        self.posicion = None  # (fila, col) o None
        self.movil = movil

    def set_pos(self, fila, col):
        self.posicion = (fila, col)

    def take_damage(self, cantidad: int):
        self.vida -= cantidad
        if self.vida <= 0:
            # eliminarse de la matriz si está presente
            if self.posicion is not None:
                f, c = self.posicion
                if self in matriz_juego[f][c]:
                    matriz_juego[f][c].remove(self)
                self.posicion = None

    def tick(self):
        """Hook por actualización; sobrescribir en subclases si es necesario."""
        pass


class Rook(Entidad):
    """Rook base: no se desplaza, puede disparar si su cooldown está a cero."""
    def __init__(self, vida: int = 10, dano: int = 10, shot_cooldown_max: int = 0, costo: int = 0):
        super().__init__("rook", vida=vida, dano=dano, movil=False)
        self.shot_cooldown = 0
        self.shot_cooldown_max = shot_cooldown_max
        self.costo = costo  # Para el sistema de monedas (no funcional aún)
        self.color = "green"  # Color por defecto

    def can_shoot(self) -> bool:
        return self.shot_cooldown == 0

    def shoot(self):
        """Dispara: fija cooldown y devuelve una Rafaga (no la coloca)."""
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano)

    def tick(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1


#Tipo 1: Roca
class RookRoca(Rook):
    def __init__(self):
        super().__init__(vida=12, dano=4, shot_cooldown_max=0, costo=100)
        self.tipo = "rook_roca"
        self.color = "gray"


#Tipo 2: Fuego
class RookFuego(Rook):
    def __init__(self):
        super().__init__(vida=12, dano=8, shot_cooldown_max=0, costo=150)
        self.tipo = "rook_fuego"
        self.color = "orange"


#Tipo 3: Agua
class RookAgua(Rook):
    def __init__(self):
        super().__init__(vida=15, dano=10, shot_cooldown_max=0, costo=150)
        self.tipo = "rook_agua"
        self.color = "cyan"


#Tipo 4: Arena
class RookArena(Rook):
    def __init__(self):
        super().__init__(vida=8, dano=2, shot_cooldown_max=0, costo=50)
        self.tipo = "rook_arena"
        self.color = "yellow"


class Avatar(Entidad):
    """Avatar base: se desplaza (movil=True) y puede regenerarse/atacar."""
    def __init__(self, vida: int = 10, dano: int = 10, regeneracion: int = 0):
        super().__init__("avatar", vida=vida, dano=dano, movil=True)
        self.regeneracion = regeneracion

    def attack(self, objetivo):
        if hasattr(objetivo, "take_damage"):
            objetivo.take_damage(self.dano)

    def tick(self):
        if self.regeneracion and self.vida > 0:
            self.vida += self.regeneracion


class AvatarFlechador(Avatar):
    def __init__(self):
        super().__init__(vida=8, dano=2, regeneracion=2)
        self.tipo = "avatar_flechador"
        self.color = "orange"


class AvatarEscudero(Avatar):
    def __init__(self):
        super().__init__(vida=8, dano=3, regeneracion=1)
        self.tipo = "avatar_escudero"
        self.color = "blue"


class AvatarCanibal(Avatar):
    def __init__(self):
        super().__init__(vida=8, dano=12, regeneracion=4)
        self.tipo = "avatar_canibal"
        self.color = "red"


class AvatarLenador(Avatar):
    def __init__(self):
        super().__init__(vida=8, dano=9, regeneracion=0)
        self.tipo = "avatar_lenador"
        self.color = "sienna"


class Rafaga:
    def __init__(self, dano: int = 5):
        self.tipo = "rafaga"
        self.dano = dano


class Juego:
    def __init__(self, root):
        self.root = root
        self.root.title("Rooks vs Avatars - 4 Tipos")

        # ---- Sistema de monedas (no funcional aún) ----
        self.monedas = 500  # Monedas iniciales (placeholder)
        
        # ---- Tipo de rook seleccionado ----
        self.rook_seleccionado = RookArena  # Por defecto: Roca

        # Frame superior para controles
        self.frame_superior = tk.Frame(root, bg="lightgray")
        self.frame_superior.pack(fill=tk.X)

        # Label de monedas (placeholder)
        self.label_monedas = tk.Label(
            self.frame_superior, 
            text=f"💰 Monedas: {self.monedas} (no funcional)",
            font=("Arial", 12),
            bg="lightgray"
        )
        self.label_monedas.pack(side=tk.LEFT, padx=10)

        # Botones para seleccionar tipo de rook
        self.crear_botones_seleccion()
        # Canvas del juego
        self.canvas = tk.Canvas(
            root, width=COLUMNAS * TAM_CASILLA, height=FILAS * TAM_CASILLA, bg="lightgreen"
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

        # Click para colocar rooks
        self.canvas.bind("<Button-1>", self.colocar_rook)

        self.juego_terminado = False

        # Control de intervalo de disparo
        self.shot_interval = 3
        self._shot_tick = 0

        # Tiempos de generación por tipo (en milisegundos)
        self.tiempos_generacion = {
            "flechador": 2000,
            "escudero": 4000,
            "canibal": 12000,
            "lenador": 10000
        }

        # Iniciar los generadores de cada tipo
        self.programar_generacion("flechador")
        self.programar_generacion("escudero")
        self.programar_generacion("canibal")
        self.programar_generacion("lenador")

        self.actualizar_juego()

    def crear_botones_seleccion(self):
        """Crea botones para seleccionar el tipo de rook a colocar."""
        frame_botones = tk.Frame(self.frame_superior, bg="lightgray")
        frame_botones.pack(side=tk.RIGHT, padx=10)

        tipos_rook = [
            ("🪨 Roca (100)", RookRoca, "gray"),
            ("🔥 Fuego (150)", RookFuego, "orange"),
            ("💧 Agua (150)", RookAgua, "cyan"),
            ("🏖️ Arena (50)", RookArena, "yellow")
        ]

        for texto, clase, color in tipos_rook:
            btn = tk.Button(
                frame_botones,
                text=texto,
                bg=color,
                command=lambda c=clase: self.seleccionar_rook(c),
                width=12,
                font=("Arial", 9)
            )
            btn.pack(side=tk.LEFT, padx=2)

    def seleccionar_rook(self, clase_rook):
        """Selecciona el tipo de rook a colocar."""
        self.rook_seleccionado = clase_rook
        print(f"Rook seleccionado: {clase_rook.__name__}")

    def colocar_rook(self, event):
        if self.juego_terminado:
            return

        c = event.x // TAM_CASILLA
        f = event.y // TAM_CASILLA

        # Solo colocar si la celda está vacía o no hay rook
        if not any(isinstance(e, Rook) for e in matriz_juego[f][c]):
            # TODO: Cuando el sistema de monedas esté implementado:
            # - Verificar si hay suficientes monedas
            # - Restar el costo de la rook
            # - Actualizar el label de monedas
            
            rook = self.rook_seleccionado()  # Crear instancia del tipo seleccionado
            rook.set_pos(f, c)
            matriz_juego[f][c].append(rook)
            
            # Placeholder para sistema de monedas:
            # if self.monedas >= rook.costo:
            #     self.monedas -= rook.costo
            #     self.label_monedas.config(text=f"💰 Monedas: {self.monedas}")
            # else:
            #     print("No hay suficientes monedas!")

    def generar_avatar(self):
        """Genera un avatar aleatorio en la última fila (abajo)."""
        columna = random.randint(0, COLUMNAS - 1)
        tipo = random.choice([AvatarFlechador, AvatarEscudero, AvatarCanibal, AvatarLenador])
        av = tipo()
        av.set_pos(FILAS - 1, columna)
        matriz_juego[FILAS - 1][columna].append(av)

    def mover_avatars(self):
        """Mueve los avatars hacia arriba y les permite atacar rooks si están frente a uno."""
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

                        # Combate con Rook
                        rook_en_actual = [r for r in matriz_juego[f][c] if isinstance(r, Rook)]
                        rook_en_destino = [r for r in matriz_juego[destino_f][c] if isinstance(r, Rook)]

                        if rook_en_actual or rook_en_destino:
                            objetivo = rook_en_actual[0] if rook_en_actual else rook_en_destino[0]
                            vida_inicial = objetivo.vida
                            e.attack(objetivo)

                            if vida_inicial > 0 and objetivo.vida <= 0:
                                continue
                            else:
                                continue

                        # Verificar si hay ráfagas en la casilla destino
                        rafagas_en_destino = [p for p in matriz_juego[destino_f][c] if isinstance(p, Rafaga)]
                        if rafagas_en_destino:
                            total_dano = sum(r.dano for r in rafagas_en_destino)
                            matriz_juego[destino_f][c] = [p for p in matriz_juego[destino_f][c] if not isinstance(p, Rafaga)]
                            e.take_damage(total_dano)
                            if e.vida <= 0:
                                e.posicion = None
                                continue

                        # Mover avatar normalmente
                        if e in matriz_juego[f][c]:
                            matriz_juego[f][c].remove(e)
                        matriz_juego[destino_f][c].append(e)
                        e.set_pos(destino_f, c)

    def programar_generacion(self, tipo):
        """Programa la generación periódica de un tipo de avatar."""
        self.root.after(self.tiempos_generacion[tipo], lambda: self.generar_avatar_tipo(tipo))

    def generar_avatar_tipo(self, tipo):
        """Genera un avatar específico y vuelve a programar su aparición."""
        if self.juego_terminado:
            return

        columna = random.randint(0, COLUMNAS - 1)
        clase = {
            "flechador": AvatarFlechador,
            "escudero": AvatarEscudero,
            "canibal": AvatarCanibal,
            "lenador": AvatarLenador
        }.get(tipo)

        if clase is not None:
            av = clase()
            av.set_pos(FILAS - 1, columna)
            matriz_juego[FILAS - 1][columna].append(av)

        self.programar_generacion(tipo)

    def disparar(self):
        """Cada rook genera una rafaga debajo de ella si puede disparar."""
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Rook):
                        e.tick()
                        if not e.can_shoot():
                            continue
                        if f + 1 < FILAS:
                            if not any(isinstance(x, Rafaga) for x in matriz_juego[f + 1][c]):
                                r = e.shoot()
                                matriz_juego[f + 1][c].append(r)

    def mover_rafagas(self):
        """Mueve las ráfagas hacia abajo."""
        for f in range(FILAS - 1, -1, -1):
            for c in range(COLUMNAS):
                for e in list(matriz_juego[f][c]):
                    if isinstance(e, Rafaga):
                        if f == FILAS - 1:
                            matriz_juego[f][c].remove(e)
                            continue
                        matriz_juego[f][c].remove(e)
                        matriz_juego[f + 1][c].append(e)

    def dibujar(self):
        """Dibuja las entidades en el canvas."""
        self.canvas.delete("entidad")
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in matriz_juego[f][c]:
                    cx = c * TAM_CASILLA + TAM_CASILLA // 2
                    cy = f * TAM_CASILLA + TAM_CASILLA // 2
                    if isinstance(e, Rook):
                        # Usar el color específico de cada tipo de rook
                        self.canvas.create_oval(
                            cx - 15, cy - 15, cx + 15, cy + 15, 
                            fill=e.color, 
                            tags="entidad"
                        )
                    elif isinstance(e, Avatar):
                        color = getattr(e, "color", "brown")
                        self.canvas.create_rectangle(
                            cx - 15, cy - 15, cx + 15, cy + 15, 
                            fill=color, 
                            tags="entidad"
                        )
                    elif isinstance(e, Rafaga):
                        self.canvas.create_oval(
                            cx - 5, cy - 5, cx + 5, cy + 5, 
                            fill="yellow", 
                            tags="entidad"
                        )

    def game_over(self):
        """Finaliza el juego."""
        self.juego_terminado = True
        self.canvas.create_text(
            COLUMNAS * TAM_CASILLA // 2, FILAS * TAM_CASILLA // 2,
            text="💀 GAME OVER 💀",
            font=("Arial", 24, "bold"), fill="red"
        )

    def actualizar_juego(self):
        """Bucle principal del juego."""
        if self.juego_terminado:
            return
        
        self.mover_avatars()
        self.mover_rafagas()

        self._shot_tick += 1
        if self._shot_tick >= self.shot_interval:
            self.disparar()
            self._shot_tick = 0

        self.dibujar()
        self.root.after(VELOCIDAD, self.actualizar_juego)


# Ejecutar el juego
root = tk.Tk()
juego = Juego(root)
root.mainloop()