import tkinter as tk
from gestion_puntajes import obtener_top_nivel
import encrip_aes
from PIL import Image, ImageTk
import os

class SalonFamaNivel:
    def __init__(self, root, nivel, username_enc, callback_volver, c1, c2, c3, c4, c5, c6, c7):
        """Interfaz que muestra el top 3 de un nivel específico"""
        self.root = root
        self.nivel = nivel
        self.username_enc = username_enc
        self.callback_volver = callback_volver
        
        # Colores
        self.c1 = c1  # Color principal/fondo
        self.c2 = c2  # Color secundario
        self.c3 = c3  # Color de botones
        self.c4 = c4  # Color de texto
        self.c5 = c5  # Color de acento
        self.c6 = c6  # Color de hover
        self.c7 = c7  # Color adicional
        
        self.frame = None
        self.master_key = encrip_aes.master_key
        
        # Variables para la animación de fondo
        self.background_images = []
        self.current_frame = 0
        self.animation_speed = 200  # milisegundos entre frames
        self.is_playing = False
        self.animation_job = None
        self.background_label = None
        
        # Variables para control de intro y loop
        self.intro_frames = 4  # Primeras 4 imágenes son intro
        self.loop_start_frame = 4  # El loop empieza desde la imagen 5
        self.intro_played = False  # Si ya se reprodujo la intro
        
        # Nuevas variables para Canvas
        self.canvas = None
        self.bg_image_id = None
        self.podium_items = []  # ids de canvas para eliminar cuando se reconstruya la pantalla
        
        self.cargar_animacion_fondo()
        self.crear_interfaz()
    
    def obtener_foto_perfil(self, username_enc):
        """Obtiene la foto de perfil del usuario si existe"""
        try:
            # Convertir username encriptado a nombre de archivo seguro
            safe_username = username_enc.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            
            # Buscar archivo de foto de perfil
            profile_photos_dir = os.path.join(os.path.dirname(__file__), "profile_photos")
            photo_path = os.path.join(profile_photos_dir, f"profile_{safe_username}.jpg")
            
            if os.path.exists(photo_path):
                # Cargar y redimensionar la imagen para el podio
                img = Image.open(photo_path)
                img = img.resize((60, 60), Image.Resampling.LANCZOS)  # Tamaño apropiado para el podio
                return ImageTk.PhotoImage(img)
            else:
                return None
                
        except Exception as e:
            print(f"Error cargando foto de perfil para {username_enc}: {e}")
            return None
    
    def obtener_carpeta_imagenes(self):
        """Retorna la carpeta de imágenes según el nivel"""
        carpetas = {
            1: "flechador",   # Nivel Fácil
            2: "escudero",    # Nivel Medio
            3: "canibal"      # Nivel Difícil
        }
        return carpetas.get(self.nivel, "canibal")
    
    def cargar_animacion_fondo(self):
        """Carga las imágenes para la animación de fondo según el nivel"""
        try:
            # Obtener la carpeta correspondiente al nivel
            carpeta_nivel = self.obtener_carpeta_imagenes()
            
            # Buscar la carpeta de imágenes
            current_dir = os.path.dirname(os.path.abspath(__file__))
            images_path = os.path.join(current_dir, "images", carpeta_nivel)
            
            if not os.path.exists(images_path):
                # Intentar ruta alternativa
                images_path = os.path.join(os.getcwd(), "images", carpeta_nivel)
                if not os.path.exists(images_path):
                    return
            
            # Extensiones de imagen válidas
            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
            
            # Obtener y ordenar archivos
            files = []
            for file in os.listdir(images_path):
                if file.lower().endswith(valid_extensions):
                    files.append(file)
            
            if not files:
                return
                
            files.sort()
            
            # Cargar imágenes
            self.background_images = []
            for file in files:
                try:
                    file_path = os.path.join(images_path, file)
                    img = Image.open(file_path)
                    
                    # Obtener dimensiones de la ventana
                    self.root.update_idletasks()
                    window_width = self.root.winfo_width() or 800
                    window_height = self.root.winfo_height() or 600
                    
                    # Redimensionar imagen para cubrir toda la ventana
                    img = img.resize((window_width, window_height), Image.Resampling.LANCZOS)
                    
                    # Convertir a PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    self.background_images.append(photo)
                    
                except Exception as e:
                    print(f"Error cargando {file}: {e}")
            
            # Verificar que tenemos suficientes imágenes para intro + loop
            if len(self.background_images) >= 8:
                pass
            else:
                # Ajustar parámetros si hay menos imágenes
                total_images = len(self.background_images)
                if total_images > 4:
                    self.intro_frames = 4
                    self.loop_start_frame = 4
                else:
                    self.intro_frames = total_images // 2
                    self.loop_start_frame = self.intro_frames
            
        except Exception as e:
            print(f"Error al cargar animación de fondo: {e}")
    
    def iniciar_animacion_fondo(self):
        """Inicia la animación de fondo (actualiza la imagen dibujada en el canvas)"""
        if self.background_images and not self.is_playing and self.canvas:
            self.is_playing = True
            self.current_frame = 0
            self.intro_played = False
            # Si no existe bg_image_id (por ejemplo si se cargó tarde), crear uno
            if not self.bg_image_id:
                self.bg_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_images[0])
                self.canvas.tag_lower(self.bg_image_id)
            self._animar_frame_fondo()
    
    def detener_animacion_fondo(self):
        """Detiene la animación de fondo"""
        self.is_playing = False
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
    
    def _animar_frame_fondo(self):
        """Actualiza la imagen de fondo en el canvas respetando intro + loop"""
        if not self.is_playing or not self.background_images or not self.canvas:
            return
        try:
            # Actualizar la imagen del canvas (itemconfig con PhotoImage)
            # Asegurar que bg_image_id existe
            if not self.bg_image_id:
                self.bg_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_images[self.current_frame])
                self.canvas.tag_lower(self.bg_image_id)
            else:
                self.canvas.itemconfig(self.bg_image_id, image=self.background_images[self.current_frame])

            # Avanzar al siguiente frame
            self.current_frame += 1

            # Intro / loop logic
            if not self.intro_played and self.current_frame >= self.intro_frames:
                self.intro_played = True
                self.current_frame = self.loop_start_frame
            elif self.intro_played and self.current_frame >= len(self.background_images):
                self.current_frame = self.loop_start_frame

            # Programar siguiente frame
            if self.is_playing:
                self.animation_job = self.root.after(self.animation_speed, self._animar_frame_fondo)

        except Exception as e:
            print(f"Error en animación: {e}")
    
    def obtener_nombre_nivel(self):
        """Retorna el nombre del nivel"""
        nombres = {1: "Fácil", 2: "Medio", 3: "Difícil"}
        return nombres.get(self.nivel, "Desconocido")
    
    def crear_interfaz(self):
        """Crea la interfaz del ranking con fondo animado en un Canvas"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Detener cualquier animación anterior
        self.detener_animacion_fondo()

        # Crear Canvas como fondo (éste se dibuja primero, los widgets creados después estarán encima)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Mostrar primera imagen de inmediato si hay imágenes
        if self.background_images:
            # Crear imagen en el canvas (guardar id)
            self.bg_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_images[0])
            # enviar al fondo por si hubiera más elementos en el canvas
            self.canvas.tag_lower(self.bg_image_id)

        # BARRA SUPERIOR (HEADER) - crear encima del canvas
        top_bar = tk.Frame(self.root, bg=self.c4, height=40)
        top_bar.place(x=0, y=0, relwidth=1)

        tk.Label(
            top_bar,
            text=f"Salón de la Fama - Nivel {self.obtener_nombre_nivel()}",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6,
            relief="flat"
        ).pack(side=tk.LEFT, padx=15, pady=8)

        # Botón volver - sin borde
        btn_volver = tk.Button(
            self.root,
            text="← Volver",
            font=("Arial", 10, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.volver,
            padx=12,
            pady=8
        )
        btn_volver.place(x=30, y=55)

        # Título principal - más arriba
        titulo_container = tk.Frame(self.root, bg=self.c4, relief="flat")
        titulo_container.place(relx=0.5, y=60, anchor="n")

        label_titulo = tk.Label(
            titulo_container,
            text=f"🏆 TOP 3 - NIVEL {self.obtener_nombre_nivel().upper()} 🏆",
            font=("Arial", 24, "bold"),
            bg=self.c4,
            fg=self.c6,
            padx=20,
            pady=15,
            relief="flat"
        )
        label_titulo.pack()

        # Obtener top 3
        top3 = obtener_top_nivel(self.nivel, limit=3)

        if not top3:
            vacio_container = tk.Frame(self.root, bg=self.c4, relief="flat")
            vacio_container.place(relx=0.5, y=150, anchor="n")

            label_vacio = tk.Label(
                vacio_container,
                text="Aún no hay puntajes registrados en este nivel",
                font=("Arial", 14),
                bg=self.c4,
                fg=self.c6,
                padx=30,
                pady=20,
                relief="flat"
            )
            label_vacio.pack()
        else:
            # Dibujar en el canvas (podio)
            # Limpiar elementos previos por si acaso
            for item in getattr(self, "podium_items", []):
                try:
                    self.canvas.delete(item)
                except:
                    pass
            self.podium_items = []
            self.mostrar_ranking_podio(top3)

        # Iniciar animación
        self.root.after(100, self.iniciar_animacion_fondo)
    
    def _draw_outlined_text(self, x, y, text, font, fill="white", outline="black", anchor="center"):
        """Dibuja texto con outline en el canvas (múltiples textos en offsets) y devuelve id del texto principal y de los outlines"""
        ids = []
        # offsets para el contorno
        offsets = [(-1,0),(1,0),(0,-1),(0,1)]
        for dx, dy in offsets:
            id_outline = self.canvas.create_text(x+dx, y+dy, text=text, font=font, fill=outline, anchor=anchor)
            ids.append(id_outline)
        id_main = self.canvas.create_text(x, y, text=text, font=font, fill=fill, anchor=anchor)
        ids.append(id_main)
        return ids
    
    def mostrar_ranking_podio(self, top3):
        """Dibuja el podio y la info de jugadores directamente en el canvas (transparente respecto al fondo)"""
        emojis = ["🥇", "🥈", "🥉"]
        colores_medalla = [self.c5, "#C0C0C0", "#CD7F32"]

        window_width = self.root.winfo_width() or 800

        posiciones_podio = [
            {"x": window_width // 2 + 10, "y": 360},     # 1er lugar
            {"x": window_width // 2 - 215, "y": 400},    # 2do lugar
            {"x": window_width // 2 + 225, "y": 400},    # 3er lugar
        ]

        # Tamaños de fuente más grandes y legibles
        font_medalla = ("Arial", 24, "bold")  
        font_pos = ("Arial", 16, "bold")     
        font_nombre = ("Arial", 12, "bold")       
        font_puntaje = ("Arial", 11, "bold")    
        font_extra = ("Arial", 9)              
        font_fecha = ("Arial", 8)             

        # borrar cualquier elemento previo del podio
        for item in getattr(self, "podium_items", []):
            try:
                self.canvas.delete(item)
            except:
                pass
        self.podium_items = []
        
        # Lista para mantener referencias a las imágenes de perfil
        if not hasattr(self, 'profile_images'):
            self.profile_images = []
        self.profile_images.clear()

        for idx, (username_enc, puntaje, fecha, tempo, popularidad) in enumerate(top3):
            try:
                username_display = encrip_aes.decrypt_data(username_enc, self.master_key)
            except:
                username_display = "Usuario desconocido"

            pos = posiciones_podio[idx]
            x = pos["x"]
            y = pos["y"]
            
            # Intentar cargar foto de perfil
            profile_photo = self.obtener_foto_perfil(username_enc)
            
            # Ajustar posición vertical si hay foto de perfil
            if profile_photo:
                # Si hay foto, mover todo hacia abajo para hacer espacio
                foto_y = y - 40  # Foto arriba del podio
                content_y_offset = 20  # Mover contenido hacia abajo
                
                # Mostrar foto de perfil
                photo_id = self.canvas.create_image(x, foto_y, image=profile_photo, anchor="n")
                self.podium_items.append(photo_id)
                self.profile_images.append(profile_photo)  # Mantener referencia
                
                # Crear borde circular alrededor de la foto (opcional)
                # circle_id = self.canvas.create_oval(x-32, foto_y-32, x+32, foto_y+32, outline="white", width=3)
                # self.podium_items.append(circle_id)
            else:
                content_y_offset = 0

            # Medalla (dibujar como texto grande con outline)
            ids = self._draw_outlined_text(x, y + content_y_offset, emojis[idx], font_medalla, fill="gold", outline="black", anchor="n")
            self.podium_items.extend(ids)

            # Número de posición (abajo de la medalla)
            ids = self._draw_outlined_text(x, y + content_y_offset + 35, f"#{idx+1}", font_pos, fill="white", outline="black", anchor="n")
            self.podium_items.extend(ids)

            # Nombre (centro) - con más espaciado
            ids = self._draw_outlined_text(x, y + content_y_offset + 60, username_display, font_nombre, fill="white", outline="black", anchor="n")
            self.podium_items.extend(ids)

            # Puntaje - con más espaciado
            ids = self._draw_outlined_text(x, y + content_y_offset + 80, f"{puntaje:.1f} pts", font_puntaje, fill="yellow", outline="black", anchor="n")
            self.podium_items.extend(ids)

            # Extra (tempo y popularidad) - con más espaciado
            ids = self._draw_outlined_text(x, y + content_y_offset + 98, f"T:{tempo} P:{popularidad}", font_extra, fill="lightblue", outline="black", anchor="n")
            self.podium_items.extend(ids)

            # Fecha - con más espaciado
            ids = self._draw_outlined_text(x, y + content_y_offset + 115, fecha, font_fecha, fill="lightgray", outline="black", anchor="n")
            self.podium_items.extend(ids)

            # Si es el usuario actual, destacar con color especial
            if username_enc == self.username_enc:
                # Cambiar color del texto principal (último id de cada grupo) a dorado brillante
                highlight_color = "#FFD700"  # Dorado brillante
                # Recorrer todos los ids de este jugador y cambiar el color del texto principal
                start_idx = len(self.podium_items) - 30  # Últimos 30 elementos (6 grupos × 5 ids cada uno)
                for i in range(start_idx, len(self.podium_items), 5):
                    if i + 4 < len(self.podium_items):
                        try:
                            # Cambiar color del texto principal (último de cada grupo de 5)
                            self.canvas.itemconfig(self.podium_items[i + 4], fill=highlight_color)
                        except:
                            pass
    
    def volver(self):
        """Vuelve a la selección de nivel"""
        # Detener animación antes de volver
        self.detener_animacion_fondo()
        
        if self.callback_volver:
            self.callback_volver()
    
    def __del__(self):
        """Destructor para asegurar que se detiene la animación"""
        self.detener_animacion_fondo()