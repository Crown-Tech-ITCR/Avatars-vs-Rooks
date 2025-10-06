import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from MusicaSpotify import SpotifyManager

class MenuPersonalizacion:
    def __init__(self, root, username, nombre, callback_volver):
        self.root = root
        self.username = username
        self.nombre = nombre
        self.callback_volver = callback_volver
        self.resultados = []
        self.spotify_manager = SpotifyManager()
        
        # Limpiar ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Personalización de Usuario")
        self.root.configure(bg="#F5F5F5")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea toda la interfaz de personalización con layout vertical"""

        # Crear canvas con scrollbar
        canvas = tk.Canvas(self.root, bg="#F5F5F5", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F5F5F5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)

        # TÍTULO PRINCIPAL
        label_titulo_principal = tk.Label(scrollable_frame, text="Personalización de usuario", 
                                        font=("Arial", 24, "bold"), bg="#F5F5F5")
        label_titulo_principal.pack(pady=(40, 20))

        # SUBTÍTULO
        label_subtitulo = tk.Label(scrollable_frame, text="Elige tu canción favorita", 
                                font=("Arial", 16), bg="#F5F5F5")
        label_subtitulo.pack(pady=(0, 45))

        #============= SECCIÓN DE PREVIEW =============

        # Frame contenedor para preview
        preview_container = tk.Frame(scrollable_frame, bg="#F5F5F5")
        preview_container.pack(pady=20)

        # Frame con fondo gris para la imagen
        frame_imagen = tk.Frame(preview_container, width=250, height=250, bg="#D3D3D3",
                                borderwidth=0, highlightthickness=0)
        frame_imagen.pack(pady=(0, 20))
        frame_imagen.pack_propagate(False)

        # Label para la imagen dentro del frame
        self.label_imagen = tk.Label(frame_imagen, bg="#D3D3D3", borderwidth=0, highlightthickness=0)
        self.label_imagen.place(x=0, y=0, width=250, height=250)

        # Titulo de la cancion
        self.label_titulo = tk.Label(preview_container, text="Canción", 
                                font=("Arial", 14, "bold"), bg="#F5F5F5")
        self.label_titulo.pack(pady=(10, 5))

        # Titulo del artista
        self.label_artista = tk.Label(preview_container, text="Artista", 
                                font=("Arial", 12), bg="#F5F5F5", fg="#666666")
        self.label_artista.pack()

        # ============= SECCIÓN DE BÚSQUEDA =============

        # Frame de búsqueda
        frame_busqueda = tk.Frame(scrollable_frame, bg="#F5F5F5")
        frame_busqueda.pack(pady=10)

        self.entry_busqueda = tk.Entry(frame_busqueda, font=("Arial", 12), width=20)
        self.entry_busqueda.pack(pady=5)

        btn_buscar = tk.Button(frame_busqueda, text="Buscar Canciones", 
                            font=("Arial", 12), command=self.mostrar_resultados)
        btn_buscar.pack(pady=5)

        # Frame para resultados
        self.frame_resultados = tk.Frame(scrollable_frame, bg="#F5F5F5")
        self.frame_resultados.pack(pady=20)


        # ============= BOTONES =============

        frame_botones = tk.Frame(scrollable_frame, bg="#F5F5F5")
        frame_botones.pack(pady=(60, 50))
        
        btn_volver = tk.Button(frame_botones, text="Volver", 
                            font=("Arial", 12), 
                            command=self.volver_login)
        btn_volver.pack(side="left", padx=10)
        
        btn_continuar = tk.Button(frame_botones, text="Continuar al juego", 
                                font=("Arial", 12, "bold"),
                                command=self.continuar_juego)
        btn_continuar.pack(side="left", padx=10)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Habilitar scroll con rueda del mouse
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

        self.resultados = self.spotify_manager.buscar_canciones(query, limit=3)

        if not self.resultados:
            messagebox.showinfo("Error", "No se encontraron canciones")
            return

        # Limpiar botones anteriores
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        # Crear botones para cada resultado
        for i, track in enumerate(self.resultados):
            nombre = track["name"]
            artista = track["artists"][0]["name"]
            btn = tk.Button(self.frame_resultados, text=f"{nombre} - {artista}", 
                            font=("Arial", 10), width=40, anchor="w", 
                            command=lambda i=i: self.seleccionar_cancion(i))
            btn.pack(pady=5)

    def seleccionar_cancion(self, index):
        """Selecciona la cancion a reproducir"""
        track = self.resultados[index]
        track_info = self.spotify_manager.info_cancion(track)

        # Mostrar imagen del álbum
        img = track_info["imagen"].copy()
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        img_album = ImageTk.PhotoImage(img)
        self.label_imagen.config(image=img_album, compound='center')
        self.label_imagen.image = img_album

        # Mostrar título de la canción y artista
        self.label_titulo.config(text=track_info['nombre'])
        self.label_artista.config(text=track_info['artista'])

        # Reproducir canción
        if not self.spotify_manager.reproducir_cancion(track_info["uri"]):
            messagebox.showwarning("Atención", "No hay dispositivo Spotify Premium activo")
    
    def volver_login(self):
        """Vuelve al login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        # Llamar callback
        self.callback_volver()
    
    def continuar_juego(self):
        """Continúa al menú principal del juego"""
        messagebox.showinfo("Próximamente", "Aquí se abrirá el menú principal del juego")
       