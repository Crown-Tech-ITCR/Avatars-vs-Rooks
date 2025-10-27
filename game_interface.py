import tkinter as tk
from game_logic import GameLogic, FILAS, COLUMNAS, TAM_CASILLA, get_matriz_juego, NIVEL_ACTUAL, reset_matriz_juego
from Entidades import RookRoca, RookFuego, RookAgua, RookArena, crear_avatar, Rook, Avatar, Rafaga, ProyectilAvatar
from sistema_puntos import SistemaPuntos

# Configuración de colores
COLOR_FONDO = "black" 
COLOR_PANEL = "#2f4c2f"
COLOR_VERDE_CLARO = "#4a7856"
COLOR_VERDE_OSCURO = "#2f4c2f"
COLOR_CASILLA_1 = "#6c6e66"
COLOR_CASILLA_2 = "#2f4c2f"
COLOR_TEXTO = "white"
COLOR_BOTON = "#2f4c2f"
COLOR_BOTON_HOVER = "#2b663b"
COLOR_HEADER = "#2f4c2f" 

# Configuración de la interfaz de rooks
ROOK_UI_CONFIG = [
    {
        "nombre": "Rook de fuego",
        "emoji": "🔥",
        "imagen": "./images/rooks/rook_fuego.png",
        "costo": 150,
        "daño": 8,
        "clase": RookFuego,
        "color": "orange"
    },
    {
        "nombre": "Rook de roca",
        "emoji": "🪨",
        "imagen": "./images/rooks/rook_roca.png",
        "costo": 100,
        "daño": 4,
        "clase": RookRoca,
        "color": "gray"
    },
    {
        "nombre": "Rook de agua",
        "emoji": "💧",
        "imagen": "./images/rooks/rook_agua.png",
        "costo": 150,
        "daño": 10,
        "clase": RookAgua,
        "color": "cyan"
    },
    {
        "nombre": "Rook de arena",
        "emoji": "🏖️",
        "imagen": "./images/rooks/rook_arena.png",
        "costo": 50,
        "daño": 2,
        "clase": RookArena,
        "color": "yellow"
    }
]

class GameInterface:
    """Clase que maneja toda la interfaz gráfica del juego."""
    
    def __init__(self, root, callback_volver_menu, tempo, popularidad):
        """Inicializa la interfaz del juego."""
        self.root = root
        self.root.title("Avatars vs Rooks - Desktop game")
        self.callback_volver_menu = callback_volver_menu
        
        # Configurar tamaño de ventana
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Variables de música para sistema de puntos
        self.tempo = tempo
        self.popularidad = popularidad
        
        # Reiniciar la matriz del juego para el nuevo nivel
        reset_matriz_juego()
        
        # Lógica del juego
        self.game_logic = GameLogic()
        
        # Variables de estado del juego
        self.juego_terminado = False
        self.tiempo_restante = 0
        
        # Variables de generación de avatars
        self.tiempos_generacion = {}
        
        # Sistema de monedas
        self.monedas = 350
        self.rook_seleccionado = RookArena
        self.boton_seleccionado = None
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Inicializar configuración del nivel
        self.inicializar_nivel()
        
        # Iniciar bucles del juego
        self.iniciar_juego()

    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica."""
        # Frame principal con fondo oscuro
        self.frame_principal = tk.Frame(self.root, bg=COLOR_FONDO)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior para título (header sin botones)
        self.crear_header()
        
        # Frame contenedor para el juego
        frame_juego = tk.Frame(self.frame_principal, bg=COLOR_FONDO)
        frame_juego.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Frame izquierdo (tablero)
        frame_izquierdo = tk.Frame(frame_juego, bg=COLOR_FONDO)
        frame_izquierdo.pack(side=tk.LEFT, padx=(0, 20))

        # Espaciador superior de la matriz
        tk.Frame(frame_izquierdo, bg=COLOR_FONDO, height=20).pack()
        
        # Canvas principal del juego
        self.canvas = tk.Canvas(
            frame_izquierdo,
            width=COLUMNAS * TAM_CASILLA,
            height=FILAS * TAM_CASILLA,
            bg=COLOR_VERDE_CLARO,
            highlightthickness=0
        )
        self.canvas.pack()

        tk.Frame(frame_izquierdo, bg=COLOR_FONDO, height=20).pack()
        
        # Dibujar cuadrícula del tablero
        self.dibujar_cuadricula()
        
        # Evento de clic para colocar rooks
        self.canvas.bind("<Button-1>", self.colocar_rook)
        
        # Frame central (panel de rooks)
        self.crear_panel_central(frame_juego)
        
        # Frame derecho (panel de controles: pausa, usuario, monedas, tiempo)
        self.crear_panel_controles(frame_juego)

    def crear_header(self):
        """Crea el header con solo el título"""
        # BARRA SUPERIOR 
        frame_header = tk.Frame(self.frame_principal, bg=COLOR_HEADER, height=40)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_header,
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            bg=COLOR_HEADER,
            fg=COLOR_TEXTO
        )
        label_titulo.pack(side=tk.LEFT, padx=15, pady=8)

    def crear_panel_central(self, parent):
        """Crea el panel central con los botones de rooks."""
        frame_central = tk.Frame(parent, bg=COLOR_FONDO, width=280)
        frame_central.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        frame_central.pack_propagate(False)
        
        # Espaciador superior para bajar los botones
        tk.Frame(frame_central, bg=COLOR_FONDO, height=20).pack()
        
        # Crear botones de selección de rooks
        self.botones_rooks = []
        for config in ROOK_UI_CONFIG:
            self.crear_boton_rook(frame_central, config)

    def crear_panel_controles(self, parent):
        """Crea el panel derecho con los controles (pausa, usuario, monedas, tiempo)"""
        frame_controles = tk.Frame(parent, bg=COLOR_FONDO, width=400)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y)
        frame_controles.pack_propagate(False)
        
        # Espaciador superior
        tk.Frame(frame_controles, bg=COLOR_FONDO, height=20).pack()
        
        # Frame para botones de pausa y usuario
        frame_botones_top = tk.Frame(frame_controles, bg=COLOR_FONDO)
        frame_botones_top.pack(anchor="e", pady=(0, 15), padx=10)
        
        # Botón de pausa
        btn_pausa = tk.Button(
            frame_botones_top,
            text="l l",
            font=("Arial", 12, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            width=4,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        btn_pausa.pack(side=tk.LEFT, padx=5)
        
        # Botón de usuario
        btn_usuario = tk.Button(
            frame_botones_top,
            text="👤",
            font=("Arial", 12),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            width=4,
            height=2,
            relief="flat",
            cursor="hand2"
        )
        btn_usuario.pack(side=tk.LEFT, padx=5)
        
        # Espaciador
        tk.Frame(frame_controles, bg=COLOR_FONDO, height=30).pack()
        
        # Panel de tiempo
        self.crear_panel_tiempo(frame_controles)
        
        # Espaciador
        tk.Frame(frame_controles, bg=COLOR_FONDO, height=20).pack()

        # Panel de monedas
        self.crear_panel_monedas(frame_controles)

    def crear_boton_rook(self, parent, config):
        """Crea un botón estilizado para seleccionar un rook."""
        # Frame contenedor del botón
        frame_boton = tk.Frame(parent, bg=COLOR_PANEL, height=110)
        frame_boton.pack(fill=tk.X, pady=10, padx=10)
        frame_boton.pack_propagate(False)
        
        # Hacer el frame clickeable
        frame_boton.bind("<Button-1>", lambda e: self.seleccionar_rook_desde_frame(config["clase"], frame_boton))
        
        # Frame izquierdo 
        frame_emoji = tk.Frame(frame_boton, bg=COLOR_PANEL, width=80)
        frame_emoji.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        frame_emoji.pack_propagate(False)
        
        # Cargar y mostrar imagen
        try:
            from PIL import Image, ImageTk
            # Cargar imagen desde la ruta en config
            imagen = Image.open(config["imagen"]) 
            imagen = imagen.resize((90, 90)) 
            imagen_tk = ImageTk.PhotoImage(imagen)
            
            label_emoji = tk.Label(
                frame_emoji,
                image=imagen_tk,
                bg=COLOR_PANEL
            )
            label_emoji.image = imagen_tk 
            label_emoji.pack(expand=True)
        except:
            # Si falla, usar el emoji como fallback
            label_emoji = tk.Label(
                frame_emoji,
                text=config["emoji"],
                font=("Arial", 40),
                bg=COLOR_PANEL
            )
            label_emoji.pack(expand=True)
        
        label_emoji.bind("<Button-1>", lambda e: self.seleccionar_rook_desde_frame(config["clase"], frame_boton))
        
        # Frame derecho para información
        frame_info = tk.Frame(frame_boton, bg=COLOR_PANEL)
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        frame_info.bind("<Button-1>", lambda e: self.seleccionar_rook_desde_frame(config["clase"], frame_boton))
        
        # Nombre del rook
        label_nombre = tk.Label(
            frame_info,
            text=config["nombre"],
            font=("Arial", 12, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            anchor="w"
        )
        label_nombre.pack(fill=tk.X, pady=(8, 2))
        label_nombre.bind("<Button-1>", lambda e: self.seleccionar_rook_desde_frame(config["clase"], frame_boton))
        
        # Costo
        label_costo = tk.Label(
            frame_info,
            text=f"Costo: {config['costo']}",
            font=("Arial", 10),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            anchor="w"
        )
        label_costo.pack(fill=tk.X, pady=2)
        label_costo.bind("<Button-1>", lambda e: self.seleccionar_rook_desde_frame(config["clase"], frame_boton))
        
        # Daño
        label_daño = tk.Label(
            frame_info,
            text=f"Daño: {config['daño']}",
            font=("Arial", 10),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            anchor="w"
        )
        label_daño.pack(fill=tk.X, pady=2)
        label_daño.bind("<Button-1>", lambda e: self.seleccionar_rook_desde_frame(config["clase"], frame_boton))
        
        # Guardar referencia al frame para poder resaltarlo
        self.botones_rooks.append(frame_boton)
        
        # Efecto hover
        def on_enter(e):
            if frame_boton != self.boton_seleccionado:
                frame_boton.config(bg=COLOR_BOTON_HOVER)
                frame_emoji.config(bg=COLOR_BOTON_HOVER)
                frame_info.config(bg=COLOR_BOTON_HOVER)
                for widget in frame_info.winfo_children():
                    widget.config(bg=COLOR_BOTON_HOVER)
                label_emoji.config(bg=COLOR_BOTON_HOVER)
        
        def on_leave(e):
            if frame_boton != self.boton_seleccionado:
                frame_boton.config(bg=COLOR_PANEL)
                frame_emoji.config(bg=COLOR_PANEL)
                frame_info.config(bg=COLOR_PANEL)
                for widget in frame_info.winfo_children():
                    widget.config(bg=COLOR_PANEL)
                label_emoji.config(bg=COLOR_PANEL)
        
        frame_boton.bind("<Enter>", on_enter)
        frame_boton.bind("<Leave>", on_leave)
        frame_emoji.bind("<Enter>", on_enter)
        frame_emoji.bind("<Leave>", on_leave)
        frame_info.bind("<Enter>", on_enter)
        frame_info.bind("<Leave>", on_leave)
        label_emoji.bind("<Enter>", on_enter)
        label_emoji.bind("<Leave>", on_leave)
        for widget in frame_info.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def seleccionar_rook_desde_frame(self, clase_rook, frame_boton):
        """Selecciona un rook desde el frame del botón."""
        self.seleccionar_rook(clase_rook)
        
        # Quitar selección anterior
        if self.boton_seleccionado:
            self.boton_seleccionado.config(bg=COLOR_PANEL)
            for widget in self.boton_seleccionado.winfo_children():
                widget.config(bg=COLOR_PANEL)
                if isinstance(widget, tk.Frame):
                    for subwidget in widget.winfo_children():
                        subwidget.config(bg=COLOR_PANEL)
        
        # Marcar nuevo botón seleccionado
        self.boton_seleccionado = frame_boton
        frame_boton.config(bg=COLOR_BOTON)
        for widget in frame_boton.winfo_children():
            widget.config(bg=COLOR_BOTON)
            if isinstance(widget, tk.Frame):
                for subwidget in widget.winfo_children():
                    subwidget.config(bg=COLOR_BOTON)

    def crear_panel_monedas(self, parent):
        """Crea el panel de monedas."""
        frame_monedas = tk.Frame(parent, bg=COLOR_BOTON, height=60, width=180) 
        frame_monedas.pack(side=tk.BOTTOM, anchor="e", pady=5, padx=10) 
        frame_monedas.pack_propagate(False)
        
        # Emoji de moneda
        label_icono = tk.Label(
            frame_monedas,
            text="🪙",
            font=("Arial", 28),
            bg=COLOR_BOTON
        )
        label_icono.pack(side=tk.LEFT, padx=(10, 5), pady=(0, 8))
        
        # Cantidad de monedas 
        self.label_monedas = tk.Label(
            frame_monedas,
            text=str(self.monedas),
            font=("Arial", 20, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO
        )
        self.label_monedas.pack(side=tk.LEFT, padx=(5, 10), pady=8)

    def crear_panel_tiempo(self, parent):
        """Crea el panel de tiempo."""
        frame_tiempo = tk.Frame(parent, bg=COLOR_PANEL, height=60, width=180)  
        frame_tiempo.pack(side=tk.BOTTOM, anchor="e", pady=11, padx=10)  
        frame_tiempo.pack_propagate(False)
        
        # Label "Tiempo"
        label_texto = tk.Label(
            frame_tiempo,
            text="Tiempo",
            font=("Arial", 11, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        )
        label_texto.pack(side=tk.LEFT, padx=(10, 5), pady=8)  

        # Tiempo restante
        self.label_tiempo = tk.Label(
            frame_tiempo,
            text="0:00",
            font=("Arial", 20, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        )
        self.label_tiempo.pack(side=tk.LEFT, padx=(5, 10), pady=8)

    def dibujar_cuadricula(self):
        """Dibuja la cuadrícula del tablero con patrón de ajedrez."""
        for f in range(FILAS):
            for c in range(COLUMNAS):
                # Alternar colores como un tablero de ajedrez
                color = COLOR_CASILLA_1 if (f + c) % 2 == 0 else COLOR_CASILLA_2
                
                self.canvas.create_rectangle(
                    c * TAM_CASILLA, f * TAM_CASILLA,
                    (c + 1) * TAM_CASILLA, (f + 1) * TAM_CASILLA,
                    fill=color,
                    outline=""
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
        
        entidades_en_casilla = matriz[f][c]
        
        # Verificar si hay rooks o avatars en la casilla
        hay_rook = any(isinstance(e, Rook) for e in entidades_en_casilla)
        hay_avatar = any(isinstance(e, Avatar) for e in entidades_en_casilla)
        
        if hay_rook or hay_avatar:
            return
        
        # Crear y colocar el rook
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
        
        import random
        
        # Buscar columnas libres (última fila sin avatars)
        columnas_libres = []
        matriz = get_matriz_juego()
        
        for c in range(COLUMNAS):
            # Verificar si la última fila de esta columna NO tiene avatars
            avatars_en_ultima_fila = [e for e in matriz[FILAS - 1][c] if isinstance(e, Avatar)]
            if not avatars_en_ultima_fila:
                columnas_libres.append(c)
        
        # Si no hay columnas libres, no generar avatar
        if not columnas_libres:
            # Programar reintento en poco tiempo
            self.root.after(500, lambda: self.programar_generacion(tipo))
            return
        
        # Seleccionar columna aleatoria de las libres
        columna = random.choice(columnas_libres)
        
        # Crear avatar
        avatar = crear_avatar(tipo)
        if avatar:
            avatar.set_pos(FILAS - 1, columna)  # Aparece en la fila inferior
            matriz[FILAS - 1][columna].append(avatar)
        
        # Programar la siguiente generación
        self.programar_generacion(tipo)

    def actualizar_tiempo(self):
        """Actualiza el contador de tiempo."""
        if self.juego_terminado:
            return
            
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            self.label_tiempo.config(text=f"{minutos}:{segundos:02d}")
            self.root.after(1000, self.actualizar_tiempo)
        else:
            self.finalizar_nivel()

    def actualizar_juego(self):
        """Bucle principal de actualización del juego."""
        if self.juego_terminado:
            return
        
        # Actualizar lógica del juego
        self.game_logic.actualizar_logica_juego(self.game_over)
        
        # Dibujar estado actual
        self.dibujar_entidades()
        
        # Programar siguiente actualización
        self.root.after(self.velocidad, self.actualizar_juego)

    def dibujar_entidades(self):
        """Dibuja todas las entidades en el canvas."""
        self.canvas.delete("entidad")
        
        matriz = get_matriz_juego()
        
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in matriz[f][c]:
                    cx = c * TAM_CASILLA + TAM_CASILLA // 2
                    cy = f * TAM_CASILLA + TAM_CASILLA // 2
                    
                    if isinstance(e, Rook):
                        # Dibujar rooks como círculos
                        self.canvas.create_oval(
                            cx - 15, cy - 15, cx + 15, cy + 15,
                            fill=e.color, tags="entidad"
                        )
                        if hasattr(e, 'vida') and e.vida < 15:
                            self.canvas.create_text(
                                cx, cy, text=str(e.vida),
                                font=("Arial", 8, "bold"), fill="white", tags="entidad"
                            )
                    
                    elif isinstance(e, Avatar):
                        # Dibujar avatars como rectángulos
                        self.canvas.create_rectangle(
                            cx - 15, cy - 15, cx + 15, cy + 15,
                            fill=e.color, tags="entidad"
                        )
                        self.canvas.create_text(
                            cx, cy, text=str(e.vida),
                            font=("Arial", 8, "bold"), fill="white", tags="entidad"
                        )
                    
                    elif isinstance(e, Rafaga):
                        # Ráfagas de rooks (amarillas, hacia abajo)
                        self.canvas.create_oval(
                            cx - 5, cy - 5, cx + 5, cy + 5,
                            fill="yellow", tags="entidad"
                        )
                    
                    elif isinstance(e, ProyectilAvatar):
                        # Proyectiles de avatars (verdes, hacia arriba)
                        self.canvas.create_oval(
                            cx - 4, cy - 4, cx + 4, cy + 4,
                            fill="green", tags="entidad"
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
            print(f" Puntos de vida de avatars acumulados: {puntos_vida_acumulados}")
            
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