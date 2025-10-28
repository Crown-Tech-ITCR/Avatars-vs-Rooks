import tkinter as tk
from gestion_puntajes import obtener_top_nivel
import encrip_aes

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
        self.crear_interfaz()
    
    def obtener_nombre_nivel(self):
        """Retorna el nombre del nivel"""
        nombres = {1: "Fácil", 2: "Medio", 3: "Difícil"}
        return nombres.get(self.nivel, "Desconocido")
    
    def crear_interfaz(self):
        """Crea la interfaz del ranking"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        self.frame = tk.Frame(self.root, bg=self.c1)
        self.frame.pack(fill="both", expand=True)
        
        # BARRA SUPERIOR (HEADER)
        top_bar = tk.Frame(self.frame, bg=self.c4, height=40)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Título en la barra
        tk.Label(
            top_bar,
            text=f"Salón de la Fama - Nivel {self.obtener_nombre_nivel()}",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # Botón volver
        frame_superior = tk.Frame(self.frame, bg=self.c1, height=60)
        frame_superior.pack(fill="x", padx=30, pady=15)
        frame_superior.pack_propagate(False)
        
        btn_volver = tk.Button(
            frame_superior,
            text="← Volver",
            font=("Arial", 10, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.volver,
            padx=12,
            pady=8
        )
        btn_volver.pack(side="left")
        
        # Frame central para contenido
        frame_central = tk.Frame(self.frame, bg=self.c1)
        frame_central.pack(expand=True, fill="both", padx=40)
        
        # Título
        label_titulo = tk.Label(
            frame_central,
            text=f"🏆 TOP 3 - NIVEL {self.obtener_nombre_nivel().upper()} 🏆",
            font=("Arial", 26, "bold"),
            bg=self.c1,
            fg=self.c6
        )
        label_titulo.pack(pady=(10, 20))
        
        # Obtener top 3
        top3 = obtener_top_nivel(self.nivel, limit=3)
        
        if not top3:
            # No hay puntajes registrados
            label_vacio = tk.Label(
                frame_central,
                text="Aún no hay puntajes registrados en este nivel",
                font=("Arial", 14),
                bg=self.c1,
                fg=self.c6
            )
            label_vacio.pack(pady=50)
        else:
            # Mostrar top 3
            self.mostrar_ranking(frame_central, top3)
    
    def mostrar_ranking(self, parent, top3):
        """Muestra el ranking de jugadores"""
        emojis = ["🥇", "🥈", "🥉"]
        
        for idx, (username_enc, puntaje, fecha, tempo, popularidad) in enumerate(top3):
            # Desencriptar username para mostrar
            try:
                username_display = encrip_aes.decrypt_data(username_enc, self.master_key)
            except:
                username_display = "Usuario desconocido"
            
            # Frame para cada posición
            frame_pos = tk.Frame(parent, bg=self.c4, relief="solid", bd=2)
            frame_pos.pack(fill="x", pady=10, padx=20)
            
            # Frame interno con padding
            frame_interno = tk.Frame(frame_pos, bg=self.c4)
            frame_interno.pack(fill="x", padx=15, pady=12)
            
            # Emoji de medalla + Posición
            label_medalla = tk.Label(
                frame_interno,
                text=f"{emojis[idx]} #{idx + 1}",
                font=("Arial", 20, "bold"),
                bg=self.c4,
                fg=self.c6
            )
            label_medalla.pack(side="left", padx=(0, 15))
            
            # Frame para info del jugador
            frame_info = tk.Frame(frame_interno, bg=self.c4)
            frame_info.pack(side="left", fill="x", expand=True)
            
            # Nombre del jugador
            label_nombre = tk.Label(
                frame_info,
                text=username_display,
                font=("Arial", 16, "bold"),
                bg=self.c4,
                fg=self.c6,
                anchor="w"
            )
            label_nombre.pack(fill="x")
            
            # Puntaje
            label_puntaje = tk.Label(
                frame_info,
                text=f"Puntaje: {puntaje:.2f} puntos",
                font=("Arial", 12),
                bg=self.c4,
                fg=self.c6,
                anchor="w"
            )
            label_puntaje.pack(fill="x")
            
            # Info adicional (tempo, popularidad, fecha)
            label_extra = tk.Label(
                frame_info,
                text=f"Tempo: {tempo} | Popularidad: {popularidad} | {fecha}",
                font=("Arial", 9),
                bg=self.c4,
                fg=self.c6,
                anchor="w"
            )
            label_extra.pack(fill="x")
            
            # Destacar si es el usuario actual
            if username_enc == self.username_enc:
                frame_pos.config(bg=self.c5, highlightbackground=self.c5, highlightthickness=3)
                frame_interno.config(bg=self.c5)
                for widget in [label_medalla, label_nombre, label_puntaje, label_extra, frame_info]:
                    widget.config(bg=self.c5)
    
    def volver(self):
        """Vuelve a la selección de nivel"""
        if self.callback_volver:
            self.callback_volver()