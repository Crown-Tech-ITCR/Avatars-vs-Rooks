import tkinter as tk
import random
from game_logic import GameLogic, FILAS, COLUMNAS, TAM_CASILLA, get_matriz_juego, NIVEL_ACTUAL,reset_matriz_juego
from Entidades import RookRoca, RookFuego, RookAgua, RookArena, crear_avatar, Rook, Avatar, Rafaga
from sistema_puntos import SistemaPuntos

# Configuración de la interfaz de rooks (solo información visual)
ROOK_UI_CONFIG = [
    ("🪨 Roca (100)", RookRoca, "gray"),
    ("🔥 Fuego (150)", RookFuego, "orange"),
    ("💧 Agua (150)", RookAgua, "cyan"),
    ("🏖️ Arena (50)", RookArena, "yellow")
]

class GameInterface:
    """Clase que maneja toda la interfaz gráfica del juego."""
    
    def __init__(self, root, callback_volver_menu, tempo, popularidad):
        """Inicializa la interfaz del juego."""
        self.root = root
        self.root.title(f"Rooks vs Avatars - Nivel {NIVEL_ACTUAL}")
        self.callback_volver_menu = callback_volver_menu
        
        # Variables de música para sistema de puntos
        self.tempo = tempo
        self.popularidad = popularidad
        
        # Reiniciar la matriz del juego para el nuevo nivel
        reset_matriz_juego()
        
        # Lógica del juego
        self.game_logic = GameLogic()
        
        # Variables de estado del juego
        self.juego_terminado = False
        self.tiempo_restante = 0  # Se inicializará con la configuración del nivel
        
        # Variables de generación de avatars
        self.tiempos_generacion = {}
        
        # Sistema de monedas (placeholder por ahora)
        self.monedas = 500
        self.rook_seleccionado = RookArena
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Inicializar configuración del nivel
        self.inicializar_nivel()
        
        # Iniciar bucles del juego
        self.iniciar_juego()

    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica."""
        # Frame superior con información
        self.frame_superior = tk.Frame(self.root, bg="lightgray")
        self.frame_superior.pack(fill=tk.X)

        # Label monedas (lado izquierdo)
        self.label_monedas = tk.Label(
            self.frame_superior,
            text=f"💰 Monedas: {self.monedas} (no funcional)",
            font=("Arial", 12),
            bg="lightgray"
        )
        self.label_monedas.pack(side=tk.LEFT, padx=10)
        
        # Label estadísticas (centro)
        self.label_stats = tk.Label(
            self.frame_superior,
            text=f"💀 Eliminados: 0 | ❤️ Vida: 0",
            font=("Arial", 10),
            bg="lightgray"
        )
        self.label_stats.pack(side=tk.LEFT, padx=20)

        # Label tiempo (lado derecho)
        self.label_tiempo = tk.Label(
            self.frame_superior,
            text=f"⏰ Tiempo: {self.tiempo_restante}s",
            font=("Arial", 12, "bold"),
            bg="lightgray"
        )
        self.label_tiempo.pack(side=tk.RIGHT, padx=10)

        # Crear botones de selección de rooks
        self.crear_botones_seleccion()

        # Canvas principal del juego
        self.canvas = tk.Canvas(
            self.root,
            width=COLUMNAS * TAM_CASILLA,
            height=FILAS * TAM_CASILLA,
            bg="lightgreen"
        )
        self.canvas.pack()

        # Dibujar cuadrícula del tablero
        self.dibujar_cuadricula()

        # Evento de clic para colocar rooks
        self.canvas.bind("<Button-1>", self.colocar_rook)

    def crear_botones_seleccion(self):
        """Crea los botones para seleccionar tipos de rooks."""
        frame_botones = tk.Frame(self.frame_superior, bg="lightgray")
        frame_botones.pack(side=tk.RIGHT, padx=10)
        
        # Lista de tipos de rook con sus clases y colores
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

    def dibujar_cuadricula(self):
        """Dibuja la cuadrícula del tablero."""
        for f in range(FILAS):
            for c in range(COLUMNAS):
                self.canvas.create_rectangle(
                    c * TAM_CASILLA, f * TAM_CASILLA,
                    (c + 1) * TAM_CASILLA, (f + 1) * TAM_CASILLA,
                    outline="black"
                )

    def seleccionar_rook(self, clase_rook):
        """Selecciona el tipo de rook a colocar."""
        self.rook_seleccionado = clase_rook
        print(f"Rook seleccionado: {clase_rook.__name__}")

    def colocar_rook(self, event):
        """Maneja el evento de clic para colocar un rook."""
        if self.juego_terminado:
            return
            
        # Calcular posición en la matriz
        c = event.x // TAM_CASILLA
        f = event.y // TAM_CASILLA
        
        # Verificar límites
        if f < 0 or f >= FILAS or c < 0 or c >= COLUMNAS:
            return
        
        matriz = get_matriz_juego()
        
        # Verificar que no haya ya un rook en esa posición
        if not any(isinstance(e, Rook) for e in matriz[f][c]):
            rook = self.rook_seleccionado()
            rook.set_pos(f, c)
            matriz[f][c].append(rook)

    def inicializar_nivel(self):
        """Inicializa la configuración específica del nivel actual."""
        from game_logic import get_config_nivel, NIVEL_ACTUAL
        
        config = get_config_nivel(NIVEL_ACTUAL)
        self.tiempo_restante = config["duracion"]
        self.tiempos_generacion = config["tiempos_regeneracion"]
        self.velocidad = config["velocidad"]

    def iniciar_juego(self):
        """Inicia todos los bucles y temporizadores del juego."""
        # Iniciar generadores de avatars
        for tipo in ["flechador", "escudero", "canibal", "lenador"]:
            self.programar_generacion(tipo)
        
        # Iniciar bucles principales
        self.root.after(1000, self.actualizar_tiempo)
        self.actualizar_juego()

    def programar_generacion(self, tipo):
        """Programa la generación de un avatar del tipo especificado."""
        if self.juego_terminado:
            return
            
        self.root.after(
            self.tiempos_generacion[tipo], 
            lambda: self.generar_avatar_tipo(tipo)
        )

    def generar_avatar_tipo(self, tipo):
        """Genera un avatar del tipo especificado en una columna aleatoria."""
        if self.juego_terminado:
            return
            
        # Seleccionar columna aleatoria
        columna = random.randint(0, COLUMNAS - 1)
        
        # Crear avatar
        avatar = crear_avatar(tipo)
        if avatar:
            avatar.set_pos(FILAS - 1, columna)  # Aparece en la fila inferior
            
            matriz = get_matriz_juego()
            matriz[FILAS - 1][columna].append(avatar)
        
        # Programar la siguiente generación
        self.programar_generacion(tipo)

    def actualizar_tiempo(self):
        """Actualiza el contador de tiempo."""
        if self.juego_terminado:
            return
            
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.label_tiempo.config(text=f"⏰ Tiempo: {self.tiempo_restante}s")
            self.root.after(1000, self.actualizar_tiempo)
        else:
            self.finalizar_nivel()

    def actualizar_juego(self):
        """Bucle principal de actualización del juego."""
        if self.juego_terminado:
            return
        
        # Actualizar lógica del juego
        self.game_logic.actualizar_logica_juego(self.game_over)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
        
        # Dibujar estado actual
        self.dibujar_entidades()
        
        # Programar siguiente actualización
        self.root.after(self.velocidad, self.actualizar_juego)

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del juego contando avatars eliminados."""
        # Contar avatars eliminados comparando con el estado anterior
        # (Esta es una implementación simplificada)
        self.label_stats.config(
            text=f"💀 Eliminados: 0 | ❤️ Vida: 0"
        )

    def dibujar_entidades(self):
        """Dibuja todas las entidades en el canvas."""
        # Limpiar entidades anteriores
        self.canvas.delete("entidad")
        
        matriz = get_matriz_juego()
        
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in matriz[f][c]:
                    # Calcular posición central de la celda
                    cx = c * TAM_CASILLA + TAM_CASILLA // 2
                    cy = f * TAM_CASILLA + TAM_CASILLA // 2
                    
                    if isinstance(e, Rook):
                        # Dibujar rooks como círculos
                        self.canvas.create_oval(
                            cx - 15, cy - 15, cx + 15, cy + 15,
                            fill=e.color,
                            tags="entidad"
                        )
                        # Mostrar vida si es menor que la máxima
                        if hasattr(e, 'vida') and e.vida < 15:
                            self.canvas.create_text(
                                cx, cy,
                                text=str(e.vida),
                                font=("Arial", 8, "bold"),
                                fill="white",
                                tags="entidad"
                            )
                    
                    elif isinstance(e, Avatar):
                        # Dibujar avatars como rectángulos
                        self.canvas.create_rectangle(
                            cx - 15, cy - 15, cx + 15, cy + 15,
                            fill=e.color,
                            tags="entidad"
                        )
                        # Mostrar vida
                        self.canvas.create_text(
                            cx, cy,
                            text=str(e.vida),
                            font=("Arial", 8, "bold"),
                            fill="white",
                            tags="entidad"
                        )
                    
                    elif isinstance(e, Rafaga):
                        # Dibujar rafagas como círculos pequeños amarillos
                        self.canvas.create_oval(
                            cx - 5, cy - 5, cx + 5, cy + 5,
                            fill="yellow",
                            tags="entidad"
                        )

    def game_over(self):
        """Maneja el game over cuando un avatar llega arriba."""
        if self.juego_terminado:
            return
            
        self.juego_terminado = True
        self.game_logic.finalizar_juego()
        
        # Mostrar mensaje de game over
        self.canvas.create_text(
            COLUMNAS * TAM_CASILLA // 2, 
            FILAS * TAM_CASILLA // 2,
            text="💀 GAME OVER 💀",
            font=("Arial", 24, "bold"), 
            fill="red",
            tags="mensaje"
        )
        
        # Calcular puntaje final
        self.calcular_puntaje_final()
        
        # Volver al menú después de 3 segundos
        self.root.after(3000, self.volver_al_menu)

    def finalizar_nivel(self):
        """Maneja la finalización exitosa del nivel."""
        if self.juego_terminado:
            return
            
        self.juego_terminado = True
        self.game_logic.finalizar_juego()
        
        # Mostrar mensaje de victoria
        self.canvas.create_text(
            COLUMNAS * TAM_CASILLA // 2,
            FILAS * TAM_CASILLA // 2,
            text=f"🎉 ¡Nivel {NIVEL_ACTUAL} completado! 🎉",
            font=("Arial", 20, "bold"),
            fill="blue",
            tags="mensaje"
        )
        
        # Calcular puntaje final
        self.calcular_puntaje_final()
        
        # Volver al menú después de 3 segundos
        self.root.after(3000, self.volver_al_menu)

    def calcular_puntaje_final(self):
        """Calcula el puntaje final usando el sistema de puntos."""
        try:

            avatrs_eliminados = self.game_logic.get_avatars_eliminados()
            puntos_vida_acumulados = self.game_logic.get_puntos_vida_acumulados()
            sistema = SistemaPuntos()
            puntaje = sistema.calcular_puntaje(
                self.tempo,
                self.popularidad,
                avatrs_eliminados,
                puntos_vida_acumulados
            )
            
            print(f"🏆 Puntaje final: {puntaje}")
            print(f" Tempo: {self.tempo}")
            print(f" Popularidad: {self.popularidad}")
            print(f" Avatars eliminados: {avatrs_eliminados}")
            print(f" Puntos de vida de avatars acumuldos: {puntos_vida_acumulados}")
            
        except Exception as e:
            print(f"Error calculando puntaje: {e}")

    def volver_al_menu(self):
        """Vuelve al menú principal."""
        try:
            if self.callback_volver_menu:
                self.root.destroy()
                self.callback_volver_menu()
            else:
                self.root.destroy()
        except:
            pass
