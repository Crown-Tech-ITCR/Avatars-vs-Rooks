import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from MusicaSpotify import SpotifyManager
from colores import ColorPicker

class MenuPersonalizacion:
    def __init__(self, root, username, nombre, callback_login, callback_menu, c1, c2, c3, c4, c5, c6, c7):
        self.root = root
        self.username = username
        self.nombre = nombre
        self.callback_login = callback_login
        self.callback_menu = callback_menu
        self.resultados = []
        self.spotify_manager = SpotifyManager()

        self.tempo_seleccionado = 120 
        self.popularidad_seleccionada = 20 
        
        # Colores recibidos
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5
        self.c6 = c6
        self.c7 = c7
        
        # Limpiar ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Personalización de Usuario")
        self.root.configure(bg=self.c1)

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea toda la interfaz de personalización con diseño mejorado"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.c1)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ========== BARRA SUPERIOR ==========
        top_bar = tk.Frame(main_frame, bg=self.c4, height=50)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Título en la barra superior
        tk.Label(
            top_bar,
            text=f"Personalización - {self.nombre}",
            font=("Arial", 14, "bold"),
            fg=self.c6,
            bg=self.c4
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Botón volver en la barra superior
        self.btn_volver_top = tk.Button(
            top_bar,
            text="← Volver",
            font=("Arial", 11, "bold"),
            bg="#000000",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5,
            command=self.volver
        )
        self.btn_volver_top.pack(side=tk.RIGHT, padx=20, pady=10)

        # ========== ÁREA DE CONTENIDO CON SCROLL ==========
        # Canvas con scrollbar
        canvas = tk.Canvas(main_frame, bg=self.c1, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.c1)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=980)
        canvas.configure(yscrollcommand=scrollbar.set)

        # ========== TÍTULO PRINCIPAL ==========
        tk.Label(
            scrollable_frame,
            text="Personaliza tu Experiencia",
            font=("Arial", 26, "bold"),
            bg=self.c1,
            fg=self.c6
        ).pack(pady=(30, 10))
        
        tk.Label(
            scrollable_frame,
            text="Configura tu perfil para una experiencia única",
            font=("Arial", 12),
            bg=self.c1,
            fg=self.c7
        ).pack(pady=(0, 30))

        # ========== SECCIÓN DE COLORES ==========
        # Frame contenedor con bordes
        section_colores = tk.Frame(scrollable_frame, bg=self.c2, relief=tk.FLAT, bd=2)
        section_colores.pack(pady=20, padx=100, fill=tk.X)
        
        # Encabezado de sección
        header_colores = tk.Frame(section_colores, bg=self.c4, height=50)
        header_colores.pack(fill=tk.X)
        header_colores.pack_propagate(False)
        
        tk.Label(
            header_colores,
            text="Selección de Color",
            font=("Arial", 16, "bold"),
            bg=self.c4,
            fg=self.c6
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Contenido de colores
        content_colores = tk.Frame(section_colores, bg=self.c2)
        content_colores.pack(pady=20, padx=20)
        
        tk.Label(
            content_colores,
            text="Elige tu color favorito para personalizar la interfaz",
            font=("Arial", 11),
            bg=self.c2,
            fg=self.c7
        ).pack(pady=(0, 15))
        
        # Frame para el color picker
        picker_frame = tk.Frame(content_colores, bg=self.c3, relief=tk.SOLID, bd=1)
        picker_frame.pack(pady=10)
        
        # ColorPicker
        self.color_picker = ColorPicker(picker_frame, width=300, height=200, bar_width=30)
        self.color_picker.pack(padx=10, pady=10)
        
        # Label del color seleccionado con estilo
        color_display_frame = tk.Frame(content_colores, bg=self.c2)
        color_display_frame.pack(pady=15)
        
        tk.Label(
            color_display_frame,
            text="Color actual:",
            font=("Arial", 11, "bold"),
            bg=self.c2,
            fg=self.c6
        ).pack(side=tk.LEFT, padx=5)
        
        self.label_color_seleccionado = tk.Label(
            color_display_frame,
            text="#ffffff",
            font=("Arial", 11, "bold"),
            bg=self.c2,
            fg=self.c4
        )
        self.label_color_seleccionado.pack(side=tk.LEFT, padx=5)
        
        # Botón aplicar color
        btn_aplicar_color = tk.Button(
            content_colores,
            text="Aplicar Color",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=8,
            command=self.aplicar_color
        )
        btn_aplicar_color.pack(pady=10)

        # ========== SECCIÓN DE MÚSICA ==========
        section_musica = tk.Frame(scrollable_frame, bg=self.c2, relief=tk.FLAT, bd=2)
        section_musica.pack(pady=20, padx=100, fill=tk.X)
        
        # Encabezado de música
        header_musica = tk.Frame(section_musica, bg=self.c4, height=50)
        header_musica.pack(fill=tk.X)
        header_musica.pack_propagate(False)
        
        tk.Label(
            header_musica,
            text="🎵 Música Favorita",
            font=("Arial", 16, "bold"),
            bg=self.c4,
            fg=self.c6
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Contenido de música
        content_musica = tk.Frame(section_musica, bg=self.c2)
        content_musica.pack(pady=20, padx=20)
        
        tk.Label(
            content_musica,
            text="Busca y selecciona tu canción favorita",
            font=("Arial", 11),
            bg=self.c2,
            fg=self.c7
        ).pack(pady=(0, 15))
        
        # ========== PREVIEW DE CANCIÓN ==========
        preview_container = tk.Frame(content_musica, bg=self.c3, relief=tk.SOLID, bd=1)
        preview_container.pack(pady=15)
        
        # Frame para imagen con borde
        image_border = tk.Frame(preview_container, bg=self.c3)
        image_border.pack(pady=15, padx=15)
        
        frame_imagen = tk.Frame(image_border, width=220, height=220, bg=self.c3,
                                relief=tk.SOLID, bd=2)
        frame_imagen.pack()
        frame_imagen.pack_propagate(False)
        
        self.label_imagen = tk.Label(frame_imagen, bg=self.c3, text="🎵\n\nSin canción\nseleccionada",
                                     font=("Arial", 12), fg=self.c7)
        self.label_imagen.place(x=0, y=0, width=220, height=220)
        
        # Info de la canción
        info_container = tk.Frame(preview_container, bg=self.c3)
        info_container.pack(pady=(0, 15), padx=15)
        
        self.label_titulo = tk.Label(
            info_container,
            text="Título de la canción",
            font=("Arial", 13, "bold"),
            bg=self.c3,
            fg=self.c6
        )
        self.label_titulo.pack(pady=(5, 2))
        
        self.label_artista = tk.Label(
            info_container,
            text="Artista",
            font=("Arial", 11),
            bg=self.c3,
            fg=self.c7
        )
        self.label_artista.pack(pady=(2, 5))

        # ========== CONTROLES DE REPRODUCCIÓN ==========
        controls_frame = tk.Frame(content_musica, bg=self.c2)
        controls_frame.pack(pady=15)

        # Botón Pausar/Reanudar
        self.btn_pausar = tk.Button(
            controls_frame,
            text="⏸ Pausar",
            font=("Arial", 11, "bold"),
            bg=self.c4,
            fg=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=6,
            command=self.toggle_pausa
        )
        self.btn_pausar.pack(side=tk.LEFT, padx=5)

        # Variable para saber si está pausado
        self.musica_pausada = False

        # ========== BÚSQUEDA ==========
        search_frame = tk.Frame(content_musica, bg=self.c2)
        search_frame.pack(pady=15)
        
        tk.Label(
            search_frame,
            text="Buscar canción:",
            font=("Arial", 11, "bold"),
            bg=self.c2,
            fg=self.c6
        ).pack(pady=(0, 8))
        
        # Frame para el campo de búsqueda
        entry_frame = tk.Frame(search_frame, bg=self.c6)
        entry_frame.pack(pady=5)
        
        self.entry_busqueda = tk.Entry(
            entry_frame,
            font=("Arial", 12),
            width=35,
            relief=tk.FLAT,
            bg=self.c6,
            fg=self.c1,
            borderwidth=0
        )
        self.entry_busqueda.pack(padx=10, pady=8)
        
        # Botón buscar
        btn_buscar = tk.Button(
            search_frame,
            text="Buscar",
            font=("Arial", 11, "bold"),
            bg=self.c4,
            fg=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            padx=25,
            pady=6,
            command=self.mostrar_resultados
        )
        btn_buscar.pack(pady=10)
        
        # Frame para resultados
        self.frame_resultados = tk.Frame(content_musica, bg=self.c2)
        self.frame_resultados.pack(pady=10)

        # ========== BOTÓN CONTINUAR ==========
        footer_frame = tk.Frame(scrollable_frame, bg=self.c1)
        footer_frame.pack(pady=40)
        
        btn_continuar = tk.Button(
            footer_frame,
            text="Continuar al Juego →",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            padx=40,
            pady=12,
            command=self.continuar_juego
        )
        btn_continuar.pack()
        
        # ========== EMPAQUETAR CANVAS ==========
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    def mostrar_resultados(self):
        """Muestra los resultados de las canciones"""
        query = self.entry_busqueda.get().strip()
        if not query:
            messagebox.showinfo("Error", "Ingresa el nombre de una canción")
            return

        # Deshabilitar botón y cambiar texto
        btn_buscar = None
        for widget in self.entry_busqueda.master.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == "Buscar":
                btn_buscar = widget
                break
        
        if btn_buscar:
            btn_buscar.config(text="Buscando...", state=tk.DISABLED, bg=self.c3)
        
        # Cambiar cursor a espera
        self.root.config(cursor="wait")
        self.root.update()
        
        try:
            # Búsqueda
            self.resultados = self.spotify_manager.buscar_canciones(query, limit=3)

            if not self.resultados:
                messagebox.showinfo("Error", "No se encontraron canciones")
                return

            # Limpiar botones anteriores
            for widget in self.frame_resultados.winfo_children():
                widget.destroy()
            
            # Título de resultados
            tk.Label(
                self.frame_resultados,
                text="Resultados:",
                font=("Arial", 11, "bold"),
                bg=self.c2,
                fg=self.c6
            ).pack(pady=(10, 5))

            # Crear botones para cada resultado
            for i, track in enumerate(self.resultados):
                nombre = track["name"]
                artista = track["artists"][0]["name"]
                
                btn = tk.Button(
                    self.frame_resultados,
                    text=f"♪  {nombre} - {artista}",
                    font=("Arial", 10),
                    bg=self.c3,
                    fg=self.c6,
                    relief=tk.FLAT,
                    cursor="hand2",
                    anchor="w",
                    padx=15,
                    pady=8,
                    width=45,
                    command=lambda i=i: self.seleccionar_cancion(i)
                )
                btn.pack(pady=3)
        
        finally:
            # Restaurar cursor y botón
            self.root.config(cursor="")
            if btn_buscar:
                btn_buscar.config(text="Buscar", state=tk.NORMAL, bg=self.c4)


    def seleccionar_cancion(self, index):
        """Selecciona la cancion a reproducir"""
        # Cambiar cursor a espera
        self.root.config(cursor="wait")
        self.root.update()
        
        try:
            track = self.resultados[index]
            track_info = self.spotify_manager.info_cancion(track)

            # Mostrar imagen del álbum
            img = track_info["imagen"].copy()
            img = img.resize((220, 220), Image.Resampling.LANCZOS)
            img_album = ImageTk.PhotoImage(img)
            self.label_imagen.config(image=img_album, text="", compound='center')
            self.label_imagen.image = img_album

            # Mostrar título de la canción y artista
            self.label_titulo.config(text=track_info['nombre'])
            self.label_artista.config(text=track_info['artista'])

            #Guardar variables importantes para sistema de puntos (tempo y popularidad)
            track_uri = track_info["uri"]
            tempo = self.spotify_manager.obtener_tempo(track_uri)
            popularidad = self.spotify_manager.obtener_popularidad(track_uri)
            
            # Guardar datos en una variable
            self.tempo_seleccionado = tempo if tempo is not None else 120
            self.popularidad_seleccionada = popularidad if popularidad is not None else 20 

            # Reproducir canción
            if not self.spotify_manager.reproducir_cancion(track_info["uri"]):
                messagebox.showwarning("Atención", "No hay dispositivo Spotify Premium activo")
        
        finally:
            # Restaurar cursor
            self.root.config(cursor="")
            
    def volver_login(self):
        """Vuelve específicamente al login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        # Llamar callback de login si existe
        if self.callback_login:
            self.callback_login(self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7)
    
    def volver_mainmenu(self):
        """Vuelve específicamente al main menu"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        # Llamar callback de main menu si existe
        if self.callback_menu:
            self.callback_menu(self.username, self.nombre, self.tempo_seleccionado,
                self.popularidad_seleccionada, self.c1, 
                self.c2, self.c3, self.c4, self.c5,
                self.c6, self.c7)
    
    def volver(self):
        """ Por defecto va al login"""
        self.volver_login()
    
    def continuar_juego(self):
        """Continúa al menú principal del juego"""
        # Usar el callback de main menu para ir al menú principal
        if self.callback_menu:
            self.volver_mainmenu()

    def aplicar_color(self):
        """Aplica el color seleccionado y actualiza el label"""
        try:
            # Verificar que el color picker existe y tiene un color válido
            if not hasattr(self, 'color_picker'):
                messagebox.showerror("Error", "No se ha inicializado el selector de colores")
                return
            
            # Obtener el color seleccionado
            color_seleccionado = getattr(self.color_picker, 'selected_color', None)
            
            # Validar que el color es válido
            if not color_seleccionado or color_seleccionado in [None, "", "#FFFFFFFF"]:
                # Usar color por defecto si no hay selección
                color_seleccionado = "#cc0000"  # Rojo por defecto
                messagebox.showinfo("Color por defecto", "No se había seleccionado ningún color.\nSe aplicará el color rojo por defecto.")
            
            # Validar formato hexadecimal
            if not color_seleccionado.startswith('#') or len(color_seleccionado) not in [7, 9]:
                color_seleccionado = "#cc0000"
                messagebox.showwarning("Color inválido", "El color seleccionado no es válido.\nSe aplicará el color rojo por defecto.")
            
            # Actualizar el label
            self.label_color_seleccionado.config(text=color_seleccionado)

            # Guardar los colores antiguos para realizar comparaciones
            colores_antiguos = {
                'c1': self.c1,
                'c2': self.c2,
                'c3': self.c3,
                'c4': self.c4,
                'c5': self.c5,
                'c6': self.c6,
                'c7': self.c7
            }
            
            # Generar paleta monocromática
            try:
                # Verificar que el color picker tiene los valores HSV necesarios
                hue = getattr(self.color_picker, 'hue', 0.0)
                saturation = getattr(self.color_picker, 'saturation', 1.0)
                
                # Validar valores HSV
                if not (0.0 <= hue <= 1.0):
                    hue = 0.0
                if not (0.0 <= saturation <= 1.0):
                    saturation = 1.0
                
                paleta = self.color_picker.generate_monochromatic_palette(hue, saturation, 7)
                
                # Validar que la paleta tiene suficientes colores
                if len(paleta) < 7:
                    raise ValueError("La paleta generada no tiene suficientes colores")
                    
            except Exception as e:
                print(f"Error generando paleta: {e}")
                # Paleta por defecto en caso de error
                paleta = [
                    "#000000",  # c1 - negro
                    "#1a1a1a",  # c2 - gris muy oscuro
                    "#535353",  # c3 - gris medio
                    color_seleccionado,  # c4 - color seleccionado
                    "#990000",  # c5 - versión oscura del color
                    "#FFFFFF",  # c6 - blanco
                    "#CCCCCC"   # c7 - gris claro
                ]

            # Asignar nuevos colores
            self.c1 = paleta[0]
            self.c2 = paleta[1]
            self.c3 = paleta[2]
            self.c4 = color_seleccionado
            self.c5 = paleta[4]
            self.c6 = paleta[5]
            self.c7 = paleta[6]

            # Actualizar la interfaz
            self.actualizar_colores_ui(colores_antiguos)

            messagebox.showinfo("Color aplicado", f"Has seleccionado el color: {color_seleccionado}")
            print(f"Color seleccionado por {self.username}: {color_seleccionado}")
            
        except Exception as e:
            print(f"Error en aplicar_color: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al aplicar el color: {str(e)}")

    def actualizar_colores_ui(self, colores_antiguos):
        """Actualiza los colores de toda la interfaz en tiempo real"""
        # Actualizar el root
        self.root.configure(bg=self.c1)
        
        # Función recursiva para actualizar todos los widgets
        def actualizar_widget(widget):

            # En caso de ser el boton de volver no actualizar (boton estandar)
            if hasattr(self, 'btn_volver_top') and widget == self.btn_volver_top:
                return  
            
            widget_type = widget.winfo_class()
            
            try:
                # Frames
                if widget_type == 'Frame':
                    current_bg = widget.cget('bg')
                    
                    # Mapear colores antiguos a nuevos
                    if current_bg == colores_antiguos['c1']:
                        widget.configure(bg=self.c1)
                    elif current_bg == colores_antiguos['c2']:
                        widget.configure(bg=self.c2)
                    elif current_bg == colores_antiguos['c3']:
                        widget.configure(bg=self.c3)
                    elif current_bg == colores_antiguos['c4']:
                        widget.configure(bg=self.c4)
                    elif current_bg == colores_antiguos['c5']:
                        widget.configure(bg=self.c5)
                    elif current_bg == colores_antiguos['c6']:
                        widget.configure(bg=self.c6)
                
                # Labels
                elif widget_type == 'Label':
                    current_bg = widget.cget('bg')
                    current_fg = widget.cget('fg')
                    
                    # Actualizar background
                    if current_bg == colores_antiguos['c1']:
                        widget.configure(bg=self.c1)
                    elif current_bg == colores_antiguos['c2']:
                        widget.configure(bg=self.c2)
                    elif current_bg == colores_antiguos['c3']:
                        widget.configure(bg=self.c3)
                    elif current_bg == colores_antiguos['c4']:
                        widget.configure(bg=self.c4)
                    elif current_bg == colores_antiguos['c6']:
                        widget.configure(bg=self.c6)
                    
                    # Actualizar foreground
                    if current_fg == colores_antiguos['c1']:
                        widget.configure(fg=self.c1)
                    elif current_fg == colores_antiguos['c4']:
                        widget.configure(fg=self.c4)
                    elif current_fg == colores_antiguos['c6']:
                        widget.configure(fg=self.c6)
                    elif current_fg == colores_antiguos['c7']:
                        widget.configure(fg=self.c7)
                
                # Buttons
                elif widget_type == 'Button':
                    current_bg = widget.cget('bg')
                    current_fg = widget.cget('fg')
                    
                    # Actualizar background
                    if current_bg == colores_antiguos['c3']:
                        widget.configure(bg=self.c3)
                    elif current_bg == colores_antiguos['c4']:
                        widget.configure(bg=self.c4)
                    elif current_bg == colores_antiguos['c5']:
                        widget.configure(bg=self.c5)
                    elif current_bg == colores_antiguos['c6']:
                        widget.configure(bg=self.c6)
                    
                    # Actualizar foreground
                    if current_fg == colores_antiguos['c1']:
                        widget.configure(fg=self.c1)
                    elif current_fg == colores_antiguos['c6']:
                        widget.configure(fg=self.c6)
                
                # Entry
                elif widget_type == 'Entry':
                    current_bg = widget.cget('bg')
                    current_fg = widget.cget('fg')
                    
                    if current_bg == colores_antiguos['c6']:
                        widget.configure(bg=self.c6)
                    if current_fg == colores_antiguos['c1']:
                        widget.configure(fg=self.c1)
                
                # Canvas
                elif widget_type == 'Canvas':
                    current_bg = widget.cget('bg')
                    if current_bg == colores_antiguos['c1']:
                        widget.configure(bg=self.c1)
                    
            except tk.TclError:
                pass  # Ignorar widgets que no tienen estas propiedades
            
            # Recursión para los hijos
            for child in widget.winfo_children():
                actualizar_widget(child)
        
        # Iniciar desde el root
        for widget in self.root.winfo_children():
            actualizar_widget(widget)
        
        # Forzar actualización visual
        self.root.update_idletasks()

    def toggle_pausa(self):
        """Alterna entre pausar y reanudar la música"""
        if self.musica_pausada:
            # Reanudar
            self.spotify_manager.reanudar_musica()
            self.btn_pausar.config(text="⏸ Pausar")
            self.musica_pausada = False
        else:
            # Pausar
            self.spotify_manager.pausar_musica()
            self.btn_pausar.config(text="▶ Reanudar")
            self.musica_pausada = True

    def cerrar_ventana(self):
        """Maneja el cierre de la ventana, deteniendo la música primero"""
        try:
            self.spotify_manager.detener_musica()
        except:
            pass  # Ignorar errores al detener música
        
        self.root.destroy()  # Cierra la aplicación

    def reset_PersonalizacionMenu(self, c1=None, c2=None, c3=None, c4=None, c5=None, c6=None, c7=None):
        """Resetea y vuelve a mostrar el menú de personalización con colores actualizados"""
        # Actualizar colores si se proporcionan
        if c1: self.c1 = c1
        if c2: self.c2 = c2
        if c3: self.c3 = c3
        if c4: self.c4 = c4
        if c5: self.c5 = c5
        if c6: self.c6 = c6
        if c7: self.c7 = c7
        
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recrear la interfaz con los nuevos colores
        self.crear_interfaz()