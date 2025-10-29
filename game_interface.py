import tkinter as tk
from PIL import Image, ImageTk
from game_logic import GameLogic, FILAS, COLUMNAS, TAM_CASILLA, get_matriz_juego, reset_matriz_juego, set_nivel_actual
from Entidades import RookRoca, RookFuego, RookAgua, RookArena, crear_avatar, Rook, Avatar, Rafaga, ProyectilAvatar
from sistema_puntos import SistemaPuntos
from gestion_puntajes import agregar_puntaje
from ModificaciónDatos import mostrar_modificar_datos
import encrip_aes

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
    
    def __init__(self, root, callback_volver_menu, tempo, popularidad, username_enc, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None):
        """Inicializa la interfaz del juego."""
        self.root = root
        self.root.title("Avatars vs Rooks - Desktop game")
        self.callback_volver_menu = callback_volver_menu

        # Variables de música para sistema de puntos
        self.tempo = tempo
        self.popularidad = popularidad

        #Username encriptado para guardar puntaje
        self.username_enc = username_enc

        # Para la modificación de datos
        self.username = None
        self.master_key = encrip_aes.master_key
        
        # AGREGAR: Colores personalizados del usuario
        self.c1 = c1 if c1 else COLOR_FONDO
        self.c2 = c2 if c2 else COLOR_PANEL
        self.c3 = c3 if c3 else COLOR_VERDE_CLARO
        self.c4 = c4 if c4 else COLOR_BOTON
        self.c5 = c5 if c5 else COLOR_BOTON_HOVER
        self.c6 = c6 if c6 else COLOR_TEXTO
        self.c7 = c7 if c7 else COLOR_TEXTO

        # Configurar tamaño de ventana
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.center_window()
        
        # Cargar username desencriptado
        self.cargar_username_desencriptado()
        
        # Reiniciar la matriz del juego para el nuevo nivel
        reset_matriz_juego()
        
        # Lógica del juego
        self.game_logic = GameLogic()
        
        # Variables de estado del juego
        self.juego_terminado = False
        self.tiempo_restante = 0

        # Variable para pausar
        self.interfaz_pausada = False
        
        # Variables de generación de avatars
        self.tiempos_generacion = {}
        
        # Sistema de monedas
        self.monedas = 350
        self.rook_seleccionado = RookArena
        self.boton_seleccionado = None

        # Cargar imagenes de los rooks
        self.imagenes_rooks = {}
        self.cargar_imagenes_rooks()

        # Almacenar las imágenes de avatares
        self.imagenes_avatares = {}
        self.cargar_imagenes_avatares()

        # Cargar imágenes de ráfagas
        self.imagenes_rafagas = {}
        self.cargar_imagenes_rafagas()

        # Cargar imágenes de proyectiles de avatares
        self.imagenes_proyectiles_avatares = {}
        self.cargar_imagenes_proyectiles_avatares()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Inicializar configuración del nivel
        self.inicializar_nivel()
        
        # Iniciar bucles del juego
        self.iniciar_juego()
    
    def cargar_username_desencriptado(self):
        """Carga el username desencriptado desde el username_enc"""
        try:
            users_enc = encrip_aes.load_users_aes()
            
            # BUSCAR POR EL username_enc ACTUAL
            if self.username_enc in users_enc:
                self.username = encrip_aes.decrypt_data(self.username_enc, self.master_key)
                print(f"Username cargado correctamente: {self.username}")
            else:
                # Si no se encuentra, buscar en todos los usuarios encriptados
                # (por si cambió el username_enc)
                username_encontrado = False
                for enc_username, user_data in users_enc.items():
                    try:
                        dec_username = encrip_aes.decrypt_data(enc_username, self.master_key)
                        if dec_username == self.username:  # Comparar con username actual
                            self.username_enc = enc_username
                            username_encontrado = True
                            print(f"Username_enc actualizado: {enc_username}")
                            break
                    except Exception:
                        continue
                
                if not username_encontrado:
                    print(f"Username encriptado no encontrado: {self.username_enc}")
                    self.username = "unknown_user"
        except Exception as e:
            print(f"Error al desencriptar username: {e}")
            self.username = "unknown_user"

    def cargar_imagenes_rooks(self):
        """Carga las imágenes de las rooks desde la carpeta images/rooks"""
        
        for config in ROOK_UI_CONFIG:
            try:
                # Cargar imagen desde el path
                img = Image.open(config["imagen"])
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                self.imagenes_rooks[config["clase"]] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando imagen {config['imagen']}: {e}")
                self.imagenes_rooks[config["clase"]] = None

    def cargar_imagenes_avatares(self):
        """Carga todas las imágenes de los avatares (3 frames por tipo)"""
        from PIL import Image, ImageTk
        
        # Tipos de avatares que tienes
        tipos_avatares = ["avatar_flechador", "avatar_escudero", "avatar_canibal", "avatar_lenador"]
        
        for tipo in tipos_avatares:
            # Cargar los 3 frames de cada tipo
            for frame in [1, 2, 3]:
                key = f"{tipo}_{frame}"
                path = f"./images/avatars/{tipo}_{frame}.png"
                
                try:
                    img = Image.open(path)
                    # Redimensionar
                    img = img.resize((35, 50), Image.Resampling.LANCZOS)
                    self.imagenes_avatares[key] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error cargando {path}: {e}")
                    self.imagenes_avatares[key] = None

    def cargar_imagenes_rafagas(self):
        """Carga las imágenes de las ráfagas desde la carpeta images/proyectiles_rooks"""
        
        # Diccionario con los tipos y sus rutas de archivo
        tipos_rafagas = {
            "fuego": "./images/proyectiles_rooks/rafaga_fuego.png",
            "roca": "./images/proyectiles_rooks/rafaga_piedra.png",
            "agua": "./images/proyectiles_rooks/rafaga_agua.png",
            "arena": "./images/proyectiles_rooks/rafaga_arena.png"
        }
        
        for tipo, path in tipos_rafagas.items():
            try:
                # Cargar imagen desde el path
                img = Image.open(path)
                # Redimensionar
                img = img.resize((30, 30), Image.Resampling.LANCZOS)
                self.imagenes_rafagas[tipo] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando imagen {path}: {e}")
                self.imagenes_rafagas[tipo] = None

    def cargar_imagenes_proyectiles_avatares(self):
        """Carga las imágenes de los proyectiles de avatares desde la carpeta images/proyectiles_avatars"""
        
        # Diccionario con los tipos y sus rutas de archivo
        tipos_proyectiles = {
            "flechador": "./images/proyectiles_avatars/proyectil_flechador.png",
            "escudero": "./images/proyectiles_avatars/proyectil_escudero.png"
        }
        
        for tipo, path in tipos_proyectiles.items():
            try:
                # Cargar imagen desde el path
                img = Image.open(path)
                # Redimensionar 
                img = img.resize((40, 65), Image.Resampling.LANCZOS)  # Formato vertical para flechas
                self.imagenes_proyectiles_avatares[tipo] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando imagen {path}: {e}")
                self.imagenes_proyectiles_avatares[tipo] = None


    def center_window(self):
        "Centra la ventana en la pantalla"
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.root.geometry(f'1000x600+{x}+{y}')

    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz gráfica."""
        # Frame principal con colores personalizados
        self.frame_principal = tk.Frame(self.root, bg=self.c1)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior para título (header sin botones)
        self.crear_header()
        
        # Frame contenedor para el juego
        frame_juego = tk.Frame(self.frame_principal, bg=self.c1)
        frame_juego.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Frame izquierdo (tablero)
        frame_izquierdo = tk.Frame(frame_juego, bg=self.c1)
        frame_izquierdo.pack(side=tk.LEFT, padx=(0, 20))

        # Espaciador superior de la matriz
        tk.Frame(frame_izquierdo, bg=self.c1, height=20).pack()
        
        # Canvas principal del juego con colores personalizados
        self.canvas = tk.Canvas(
            frame_izquierdo,
            width=COLUMNAS * TAM_CASILLA,
            height=FILAS * TAM_CASILLA,
            bg=self.c3,  # Usar color personalizado
            highlightthickness=0
        )
        self.canvas.pack()

        tk.Frame(frame_izquierdo, bg=self.c1, height=20).pack()
        
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
        # BARRA SUPERIOR con colores personalizados
        frame_header = tk.Frame(self.frame_principal, bg=self.c4, height=40)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_header,
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6
        )
        label_titulo.pack(side=tk.LEFT, padx=15, pady=8)

    def crear_panel_central(self, parent):
        """Crea el panel central con los botones de rooks."""
        frame_central = tk.Frame(parent, bg=self.c1, width=280)
        frame_central.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        frame_central.pack_propagate(False)
        
        # Espaciador superior para bajar los botones
        tk.Frame(frame_central, bg=self.c1, height=20).pack()
        
        # Crear botones de selección de rooks
        self.botones_rooks = []
        for config in ROOK_UI_CONFIG:
            self.crear_boton_rook(frame_central, config)

    def crear_panel_controles(self, parent):
        """Crea el panel derecho con los controles (pausa, usuario, monedas, tiempo)"""
        frame_controles = tk.Frame(parent, bg=self.c1, width=400)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y)
        frame_controles.pack_propagate(False)
        
        # Espaciador superior
        tk.Frame(frame_controles, bg=self.c1, height=20).pack()
        
        # Frame para botones de pausa y usuario
        frame_botones_top = tk.Frame(frame_controles, bg=self.c1)
        frame_botones_top.pack(anchor="e", pady=(0, 15), padx=10)
        
        # Botón de pausa con colores personalizados
        self.btn_pausa = tk.Button(
            frame_botones_top,
            text="l l",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6,
            width=4,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.toggle_pausa
        )
        self.btn_pausa.pack(side=tk.LEFT, padx=5)
        
        # Botón de usuario con colores personalizados
        btn_usuario = tk.Button(
            frame_botones_top,
            text="👤",
            font=("Arial", 12),
            bg=self.c4,
            fg=self.c6,
            width=4,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.mostrar_modificar_datos
        )
        btn_usuario.pack(side=tk.LEFT, padx=5)
        
        # Espaciador
        tk.Frame(frame_controles, bg=self.c1, height=30).pack()
        
        # Panel de tiempo
        self.crear_panel_tiempo(frame_controles)
        
        # Espaciador
        tk.Frame(frame_controles, bg=self.c1, height=20).pack()

        # Panel de monedas
        self.crear_panel_monedas(frame_controles)

    def toggle_pausa(self):
        """Alterna entre pausar y reanudar el juego."""
        # Cambiar estado en game_logic
        esta_pausado = self.game_logic.toggle_pausa()
        
        # Actualizar estado de interfaz
        self.interfaz_pausada = esta_pausado
        
        # Actualizar texto del botón
        if esta_pausado:
            self.btn_pausa.config(text="▶")
        else:
            self.btn_pausa.config(text="l l")
            # Reanudar bucles si estaban pausados
            if not self.juego_terminado:
                self.reanudar_bucles()
    
    def reanudar_bucles(self):
        """Reanuda los bucles del juego después de una pausa."""
        if not self.juego_terminado and not self.interfaz_pausada:
            # Reanudar actualización de tiempo si no está corriendo
            self.root.after(1000, self.actualizar_tiempo)
            # Reanudar bucle de juego
            self.actualizar_juego()

    def mostrar_modificar_datos(self):
        """Muestra la interfaz de modificación de datos del usuario."""
        # Pausar el juego automáticamente
        if not self.game_logic.esta_pausado():
            self.toggle_pausa()
        
        # Crear ventana emergente para modificación de datos
        ventana_modificar = tk.Toplevel(self.root)
        ventana_modificar.title("Modificar Datos de Usuario")
        ventana_modificar.geometry("600x500")  # Ventana más pequeña
        ventana_modificar.resizable(False, False)
        
        # Centrar la ventana
        ventana_modificar.transient(self.root)
        ventana_modificar.grab_set()
        
        # Centrar en pantalla
        x = (ventana_modificar.winfo_screenwidth() // 2) - (600 // 2)
        y = (ventana_modificar.winfo_screenheight() // 2) - (500 // 2)
        ventana_modificar.geometry(f'600x500+{x}+{y}')
        
        # Función para volver (cerrar ventana)
        def callback_volver():
            ventana_modificar.destroy()
            # RECARGAR USERNAME Y USERNAME_ENC DESPUÉS DE LOS CAMBIOS
            old_username = self.username
            old_username_enc = self.username_enc
            
            # Buscar el username_enc actualizado
            try:
                users_enc = encrip_aes.load_users_aes()
                username_encontrado = False
                
                for enc_username, user_data in users_enc.items():
                    try:
                        dec_username = encrip_aes.decrypt_data(enc_username, self.master_key)
                        if dec_username == self.username:
                            self.username_enc = enc_username
                            username_encontrado = True
                            print(f"Username_enc actualizado: {enc_username}")
                            break
                    except Exception:
                        continue
                
                if not username_encontrado:
                    print(f"No se pudo encontrar username_enc para: {self.username}")
                    
            except Exception as e:
                print(f"Error actualizando username_enc: {e}")
            
            # Reanudar el juego si estaba pausado
            if self.game_logic.esta_pausado():
                self.toggle_pausa()
        
        # Mostrar interfaz de modificación con colores personalizados
        modificador = mostrar_modificar_datos(
            ventana_modificar,
            self.username,
            self.username_enc,
            callback_volver,
            self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7
        )
        
        # Función especial para actualizar datos después del guardado
        original_volver = modificador.volver
        def nuevo_volver():
            # Obtener datos actualizados antes de cerrar
            datos_actualizados = modificador.get_updated_data()
            if datos_actualizados:
                self.username = datos_actualizados['username']
                self.username_enc = datos_actualizados['username_enc']
                print(f"Datos actualizados en GameInterface: {self.username}")
            original_volver()
        
        modificador.volver = nuevo_volver


    def crear_boton_rook(self, parent, config):
        """Crea un botón estilizado para seleccionar un rook."""
        # Frame contenedor del botón
        frame_boton = tk.Frame(parent, bg=COLOR_PANEL, height=110)
        frame_boton.pack(fill=tk.X, pady=10, padx=10)
        frame_boton.pack_propagate(False)
        
        # Hacer el frame clickeable
        frame_boton.bind("<Button-1>", lambda e, cfg=config, fb=frame_boton: self.seleccionar_rook_desde_frame(cfg["clase"], fb))
        
        # Frame izquierdo 
        frame_emoji = tk.Frame(frame_boton, bg=COLOR_PANEL, width=80)
        frame_emoji.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        frame_emoji.pack_propagate(False)
        
        # Cargar y mostrar imagen
        try:
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
        
        label_emoji.bind("<Button-1>", lambda e, cfg=config, fb=frame_boton: self.seleccionar_rook_desde_frame(cfg["clase"], fb))
        
        # Frame derecho para información
        frame_info = tk.Frame(frame_boton, bg=COLOR_PANEL)
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        frame_info.bind("<Button-1>", lambda e, cfg=config, fb=frame_boton: self.seleccionar_rook_desde_frame(cfg["clase"], fb))
        
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
        label_nombre.bind("<Button-1>", lambda e, cfg=config, fb=frame_boton: self.seleccionar_rook_desde_frame(cfg["clase"], fb))
        
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
        label_costo.bind("<Button-1>", lambda e, cfg=config, fb=frame_boton: self.seleccionar_rook_desde_frame(cfg["clase"], fb))
        
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
        label_daño.bind("<Button-1>", lambda e, cfg=config, fb=frame_boton: self.seleccionar_rook_desde_frame(cfg["clase"], fb))
        
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
        if self.juego_terminado or self.interfaz_pausada:
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
        self.bucle_visual()  

    def programar_generacion(self, tipo):
        """Programa la generación de un avatar del tipo especificado."""
        if self.juego_terminado:
            return
            
        # Calcular tiempo de espera - si está pausado, esperar menos
        tiempo_espera = self.tiempos_generacion[tipo]
        if self.interfaz_pausada:
            tiempo_espera = 1000  # Revisar cada segundo si sigue pausado
            
        self.root.after(
            tiempo_espera, 
            lambda: self.generar_avatar_tipo(tipo)
        )

    def generar_avatar_tipo(self, tipo):
        """Genera un avatar del tipo especificado en una columna aleatoria."""
        if self.juego_terminado:
            return
        
        # Si está pausado, reprogramar para más tarde
        if self.interfaz_pausada:
            self.root.after(1000, lambda: self.generar_avatar_tipo(tipo))
            return
        
        import random
        
        # Buscar columnas libres (última fila sin avatars)
        columnas_libres = []
        matriz = get_matriz_juego()
        
        # Verificar SOLO la última fila (FILAS - 1)
        for c in range(COLUMNAS):
            avatars_en_ultima_fila = [e for e in matriz[FILAS - 1][c] if isinstance(e, Avatar)]
            if not avatars_en_ultima_fila:
                columnas_libres.append(c)
        
        # Si no hay columnas libres, esperar más tiempo antes del reintento
        if not columnas_libres:
            self.root.after(1000, lambda: self.programar_generacion(tipo))  # Esperar 1 segundo
            return
        
        # Seleccionar columna aleatoria de las libres
        columna = random.choice(columnas_libres)
        
        # Crear avatar SIEMPRE en la última fila
        avatar = crear_avatar(tipo)
        if avatar:
            avatar.set_pos(FILAS - 1, columna)  # Forzar última fila
            matriz[FILAS - 1][columna].append(avatar)
            self.dibujar_entidades()
        
        # Programar la siguiente generación
        self.programar_generacion(tipo)

    def actualizar_tiempo(self):
        """Actualiza el contador de tiempo."""
        if self.juego_terminado or self.interfaz_pausada:
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
        if self.juego_terminado or self.interfaz_pausada:
            return
        
        # Actualizar lógica del juego
        self.game_logic.actualizar_logica_juego(self.game_over)
        
        # Programar siguiente actualización
        self.root.after(self.velocidad, self.actualizar_juego)

    def bucle_visual(self):
        """Bucle de ANIMACIÓN y DIBUJO - 60 FPS."""
        if self.juego_terminado:
            return
        
        # Actualizar animaciones (movimiento suave)
        if not self.interfaz_pausada:
            self.actualizar_animaciones()
        
        # Dibujar estado actual
        self.dibujar_entidades()

        #Indicador de pausa
        if self.interfaz_pausada:
            self.mostrar_indicador_pausa()
        
        # Programar siguiente frame visual
        self.root.after(16, self.bucle_visual)
    
    def mostrar_indicador_pausa(self):
        """Muestra un indicador visual de que el juego está pausado."""
        # Crear un overlay semitransparente
        canvas_width = COLUMNAS * TAM_CASILLA
        canvas_height = FILAS * TAM_CASILLA
        
        # Crear rectángulo semitransparente
        self.canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill="black", stipple="gray50", tags="pausa_overlay"
        )
        
        # Texto de pausa
        self.canvas.create_text(
            canvas_width // 2, canvas_height // 2,
            text="PAUSADO",
            font=("Arial", 24, "bold"),
            fill="white",
            tags="pausa_overlay"
        )
        
        self.canvas.create_text(
            canvas_width // 2, (canvas_height // 2) + 30,
            text="Presiona ▶ para continuar",
            font=("Arial", 12),
            fill="white",
            tags="pausa_overlay"
        )

    def dibujar_entidades(self):
        """Dibuja todas las entidades del juego (rooks, avatars, ráfagas, proyectiles) en el canvas."""
        self.canvas.delete("entidad")
        self.canvas.delete("pausa_overlay")
        
        matriz = get_matriz_juego()
        
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in matriz[f][c]:

                    # Usar posición visual si está disponible
                    if hasattr(e, 'x_visual') and hasattr(e, 'y_visual'):
                        cx = e.x_visual
                        cy = e.y_visual
                    else:
                        # Fallback: calcular desde posición lógica
                        cx = c * TAM_CASILLA + TAM_CASILLA // 2
                        cy = f * TAM_CASILLA + TAM_CASILLA // 2
                    
                    if isinstance(e, Rook):

                        self.DibujarRook(cx,cy,e)
                    
                    elif isinstance(e, Avatar):

                        self.DibujarAvatar(cx,cy,e)
                    
                    elif isinstance(e, Rafaga):

                        self.DibujarRafaga(cx,cy,e)
                    
                    elif isinstance(e, ProyectilAvatar):
                        
                        self.DibujarProyectilAvatar(cx,cy,e)

    def actualizar_animaciones(self):
        """Actualiza las animaciones de todas las entidades en el tablero."""
        from game_logic import get_matriz_juego, FILAS, COLUMNAS
        
        matriz = get_matriz_juego()
        delta_ms = 16  # Aproximadamente 60 FPS (16ms por frame)
        
        # Recorrer todas las entidades en la matriz
        for f in range(FILAS):
            for c in range(COLUMNAS):
                for e in matriz[f][c]:
                    # Si la entidad tiene el método actualizar_animacion, llamarlo
                    if hasattr(e, 'actualizar_animacion_movimiento'):
                        e.actualizar_animacion_movimiento(delta_ms)
    
    def DibujarRook(self, cx, cy, e):
        """Dibuja una torre (Rook) en el canvas con su imagen o forma de respaldo."""
        # Obtener la imagen correspondiente al tipo de rook
        imagen = self.imagenes_rooks.get(type(e))
        
        if imagen:
            # Dibujar la imagen de la rook
            self.canvas.create_image(
                cx, cy, 
                image=imagen, 
                tags="entidad"
            )
        else:
            # Si no hay imagen, usar círculo
            self.canvas.create_oval(
                cx - 15, cy - 15, cx + 15, cy + 15,
                fill=e.color, tags="entidad"
            )
        
        # Mostrar vida
        if hasattr(e, 'vida'):
            self.canvas.create_text(
                cx, cy + 20, text=str(e.vida),
                font=("Arial", 8, "bold"), fill="white", tags="entidad"
            )

    def DibujarAvatar(self, cx, cy, e):
        """Dibuja un avatar animado con sus frames de animación y barra de vida."""
        # Actualizar animación del avatar
        e.actualizar_animacion()
        
        # Obtener la imagen correspondiente al tipo y frame actual
        key = f"{e.tipo}_{e.frame_actual}"
        imagen = self.imagenes_avatares.get(key)
        
        if imagen:
            # Dibujar la imagen animada del avatar
            self.canvas.create_image(
                cx, cy, 
                image=imagen, 
                tags="entidad"
            )
            
            # Mostrar vida
            self.canvas.create_text(
                cx, cy - 22, 
                text=str(e.vida),
                font=("Arial", 8, "bold"), 
                fill="white", 
                tags="entidad"
            )
        else:
            # Dibujar rectángulo si no hay imagen
            self.canvas.create_rectangle(
                cx - 15, cy - 15, cx + 15, cy + 15,
                fill=e.color, tags="entidad"
            )
            self.canvas.create_text(
                cx, cy, text=str(e.vida),
                font=("Arial", 8, "bold"), fill="white", tags="entidad"
            )

    def DibujarRafaga(self, cx, cy, e):
        """Dibuja una ráfaga (proyectil de torre) con imagen específica según su tipo."""
        # Ráfagas con imágenes personalizadas
        tipo_rafaga = getattr(e, 'tipo_rafaga', 'arena')
        
        # Intentar dibujar con imagen
        if tipo_rafaga in self.imagenes_rafagas and self.imagenes_rafagas[tipo_rafaga]:
            self.canvas.create_image(
                cx, cy,
                image=self.imagenes_rafagas[tipo_rafaga],
                tags="entidad"
            )
        else:
            # Fallback: si no hay imagen, usar colores
            colores_fallback = {
                "fuego": "orange",
                "roca": "gray",
                "agua": "cyan",
                "arena": "yellow"
            }
            color = colores_fallback.get(tipo_rafaga, "yellow")
            
            self.canvas.create_oval(
                cx - 5, cy - 5, cx + 5, cy + 5,
                fill=color, tags="entidad"
            )

    def DibujarProyectilAvatar(self, cx, cy, e):
        """Dibuja un proyectil de avatar (flecha, etc.) con imagen o forma de respaldo."""
        # Proyectiles de avatares con imágenes personalizadas
        tipo_proyectil = getattr(e, 'tipo_proyectil', 'flechador')
        
        # Intentar dibujar con imagen
        if tipo_proyectil in self.imagenes_proyectiles_avatares and self.imagenes_proyectiles_avatares[tipo_proyectil]:
            self.canvas.create_image(
                cx, cy,
                image=self.imagenes_proyectiles_avatares[tipo_proyectil],
                tags="entidad"
            )
        else:
            # Fallback: si no hay imagen, usar formas de colores
            colores_fallback = {
                "flechador": "brown",
                "escudero": "blue"
            }
            color = colores_fallback.get(tipo_proyectil, "brown")
            
            # Dibujar flecha con color
            self.canvas.create_polygon(
                cx, cy - 8,      # punta arriba
                cx - 4, cy + 8,  # base izquierda
                cx + 4, cy + 8,  # base derecha
                fill=color, outline="black", tags="entidad"
            )


            

    def game_over(self):
        """
        Se ejecuta cuando el jugador PIERDE.
        Muestra opciones: reintentar el nivel, menú principal.
        """
        # Evitar múltiples ejecuciones simultáneas
        if self.juego_terminado:
            return

        # Detener la lógica del juego
        self.juego_terminado = True
        self.game_logic.finalizar_juego()

        # Mostrar popup de resultado (perdió)
        self.mostrar_popup_resultado(gano=False)





    def finalizar_nivel(self):
        """
        Se ejecuta cuando el jugador GANA un nivel.
        Muestra una ventana con opciones: repetir, siguiente nivel (si aplica) o menú.
        """
        # Evitar ejecutar dos veces si ya terminó
        if self.juego_terminado:
            return
                
        # Detener la lógica del juego
        self.juego_terminado = True
        self.game_logic.finalizar_juego()

        # Mostrar popup de resultado (ganó)
        self.mostrar_popup_resultado(gano=True)



    def repetir_nivel(self, ventana, nivel):
        """
        Reinicia el nivel que el jugador acaba de jugar.
        """

        from game_logic import set_nivel_actual

        set_nivel_actual(nivel)  #Mantener el mismo nivel
        ventana.destroy()
        self.root.destroy()

        # Iniciar el mismo nivel directamente sin pasar por el menú
        self.callback_volver_menu(iniciar_nuevo_nivel=True)



    def next_level(self, ventana, nivel):
        """
        Avanza al siguiente nivel correctamente.
        """

        from game_logic import set_nivel_actual

        set_nivel_actual(nivel + 1)  # Aumentar nivel de manera segura
        ventana.destroy()
        self.root.destroy()

        # Lanzar el siguiente nivel inmediatamente
        self.callback_volver_menu(iniciar_nuevo_nivel=True)



    def mostrar_popup_resultado(self, gano):
        """
        Función unificada para mostrar popup de resultado (ganar/perder).
        
        Args:
            gano (bool): True si ganó, False si perdió
        """
        from game_logic import NIVEL_ACTUAL
        
        # Obtener datos del puntaje
        datos_puntaje = self.calcular_puntaje_final()
        
        if not datos_puntaje['exito']:
            print(f"Error calculando puntaje: {datos_puntaje.get('error', 'Error desconocido')}")
        
        # Configuración según resultado
        if gano:
            titulo = "Nivel completado"
            mensaje = f"🎉 ¡Nivel {datos_puntaje['nivel']} completado! 🎉"
            color_mensaje = COLOR_TEXTO
            altura = 420
        else:
            titulo = "¡Has perdido! 💀"
            mensaje = f"💀 Perdiste en el Nivel {datos_puntaje['nivel']} 💀"
            color_mensaje = "red"
            altura = 380
        
        # Crear popup
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(f"500x{altura}")
        ventana.config(bg=COLOR_PANEL)
        ventana.resizable(False, False)
        
        # Centrar ventana
        self.centrar_popup(ventana, 500, altura)
        
        # Mensaje principal
        tk.Label(
            ventana,
            text=mensaje,
            font=("Arial", 18, "bold"),
            bg=COLOR_PANEL, 
            fg=color_mensaje,
            pady=10
        ).pack()
        
        # Mostrar puntuación
        tk.Label(
            ventana,
            text=f"🏆 Puntuación Final: {datos_puntaje['puntaje']:.2f}",
            font=("Arial", 14, "bold"),
            bg=COLOR_PANEL, 
            fg="gold",
            pady=5
        ).pack()
        
        # Estadísticas
        tk.Label(
            ventana,
            text=f"⚔️ Avatars eliminados: {datos_puntaje['avatars_eliminados']}",
            font=("Arial", 12),
            bg=COLOR_PANEL, 
            fg=COLOR_TEXTO,
            pady=2
        ).pack()
        
        tk.Label(
            ventana,
            text=f"💔 Daño total: {datos_puntaje['puntos_vida_acumulados']}",
            font=("Arial", 12),
            bg=COLOR_PANEL, 
            fg=COLOR_TEXTO,
            pady=2
        ).pack()
        
        tk.Label(
            ventana,
            text=f"🎵 Tempo: {datos_puntaje['tempo']} | Popularidad: {datos_puntaje['popularidad']}",
            font=("Arial", 10),
            bg=COLOR_PANEL, 
            fg=COLOR_TEXTO,
            pady=2
        ).pack()
        
        # Botones según el resultado
        if gano:
            self.crear_botones_victoria(ventana, datos_puntaje['nivel'])
        else:
            self.crear_botones_derrota(ventana, datos_puntaje['nivel'])
    
    def centrar_popup(self, ventana, ancho, alto):
        """Centra una ventana popup respecto a la ventana principal"""
        ventana.update_idletasks()
        self.root.update_idletasks()
        
        # Obtener posición de la ventana padre
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        
        # Calcular posición central
        x = parent_x + (parent_width // 2) - (ancho // 2)
        y = parent_y + (parent_height // 2) - (alto // 2)
        
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    def crear_botones_victoria(self, ventana, nivel):
        """Crea botones para cuando el jugador gana"""
        # Botón para repetir nivel
        tk.Button(
            ventana,
            text="🔁 Repetir nivel",
            font=("Arial", 12, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            width=20,
            command=lambda: self.repetir_nivel(ventana, nivel)
        ).pack(pady=8)

        # Botón siguiente nivel SOLO si el nivel actual es menor a 3
        if nivel < 3:
            tk.Button(
                ventana,
                text="⏭ Siguiente nivel",
                font=("Arial", 12, "bold"),
                bg=COLOR_BOTON,
                fg=COLOR_TEXTO,
                width=20,
                command=lambda: self.next_level(ventana, nivel)
            ).pack(pady=8)

        # Botón menú principal
        tk.Button(
            ventana,
            text="🏠 Menú principal",
            font=("Arial", 12, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            width=20,
            command=lambda: self.volver_menu_win(ventana)
        ).pack(pady=8)
    
    def crear_botones_derrota(self, ventana, nivel):
        """Crea botones para cuando el jugador pierde"""
        # Frame para alinear botones en fila
        frame_botones = tk.Frame(ventana, bg=COLOR_PANEL)
        frame_botones.pack(pady=20)

        # Reintentar → Reinicia el MISMO nivel
        tk.Button(
            frame_botones,
            text="🔁 Reintentar",
            font=("Arial", 12, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            width=12,
            command=lambda: self.repetir_nivel(ventana, nivel)
        ).pack(side=tk.LEFT, padx=8)

        # Volver al menú → solo mostrar menú principal
        tk.Button(
            frame_botones,
            text="🏠 Menú",
            font=("Arial", 12, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            width=12,
            command=lambda: self.volver_menu_win(ventana)
        ).pack(side=tk.LEFT, padx=8)

    #Reemplazar volver_menu_win
    def volver_menu_win(self, ventana):
        # Cerrar sólo el popup y notificar al MainMenu
        ventana.destroy()
        self.callback_volver_menu()


    def calcular_puntaje_final(self):
            """Calcula el puntaje final usando el sistema de puntos y retorna los datos."""
            try:
                from game_logic import NIVEL_ACTUAL
            
                avatars_eliminados = self.game_logic.get_avatars_eliminados()
                puntos_vida_acumulados = self.game_logic.get_puntos_vida_acumulados()
                sistema = SistemaPuntos()
                puntaje = sistema.calcular_puntaje(
                    self.tempo,
                    self.popularidad,
                    avatars_eliminados,
                    puntos_vida_acumulados
                )
            
                # GUARDAR PUNTAJE
                agregar_puntaje(
                    self.username_enc,
                    NIVEL_ACTUAL,
                    puntaje,
                    self.tempo,
                    self.popularidad
                )
            
                # Retornar diccionario con todos los datos
                return {
                    'exito': True,
                    'puntaje': puntaje,
                    'tempo': self.tempo,
                    'popularidad': self.popularidad,
                    'avatars_eliminados': avatars_eliminados,
                    'puntos_vida_acumulados': puntos_vida_acumulados,
                    'nivel': NIVEL_ACTUAL
                }
            
            except Exception as e:
                # Retornar diccionario con información del error
                return {
                    'exito': False,
                    'error': str(e),
                    'puntaje': 0,
                    'tempo': self.tempo,
                    'popularidad': self.popularidad
                }