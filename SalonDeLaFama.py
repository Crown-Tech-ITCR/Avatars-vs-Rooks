import tkinter as tk
from SalonFamaNivel import SalonFamaNivel

class SalonDeLaFama:
    def __init__(self, root, username_enc, callback_volver, c1, c2, c3, c4, c5, c6, c7):
        """Interfaz de selección de nivel del Salón de la Fama"""
        self.root = root
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
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de selección de nivel"""
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
            text="Salón de la Fama",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # Botón volver (izquierda arriba)
        frame_superior = tk.Frame(self.frame, bg=self.c1, height=60)
        frame_superior.pack(fill="x", padx=30, pady=15)
        frame_superior.pack_propagate(False)
        
        btn_volver = tk.Button(
            frame_superior,
            text="← Volver al menú",
            font=("Arial", 10, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.volver_menu,
            padx=12,
            pady=8
        )
        btn_volver.pack(side="left")
        
        # Frame central para contenido
        frame_central = tk.Frame(self.frame, bg=self.c1)
        frame_central.pack(expand=True, fill="both")
        
        # Título
        label_titulo = tk.Label(
            frame_central,
            text="SALÓN DE LA FAMA",
            font=("Arial", 32, "bold"),
            bg=self.c1,
            fg=self.c6
        )
        label_titulo.pack(pady=(20, 5))
        
        # Subtítulo
        label_subtitulo = tk.Label(
            frame_central,
            text="Selecciona un nivel para ver el top 3",
            font=("Arial", 14),
            bg=self.c1,
            fg=self.c6
        )
        label_subtitulo.pack(pady=(0, 10))
        
        # Línea decorativa
        linea = tk.Frame(frame_central, bg=self.c4, height=6)
        linea.pack(pady=(0, 30))
        linea.configure(width=450)
        
        # Frame para los botones de niveles
        frame_botones = tk.Frame(frame_central, bg=self.c1)
        frame_botones.pack(pady=10)
        
        # Botón Nivel 1 (Fácil)
        btn_facil = tk.Button(
            frame_botones,
            text="🏆 Fácil",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=lambda: self.ver_nivel(1),
            width=20,
            height=2
        )
        btn_facil.pack(pady=10)
        
        # Botón Nivel 2 (Medio)
        btn_medio = tk.Button(
            frame_botones,
            text="🏆 Medio",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=lambda: self.ver_nivel(2),
            width=20,
            height=2
        )
        btn_medio.pack(pady=10)
        
        # Botón Nivel 3 (Difícil)
        btn_dificil = tk.Button(
            frame_botones,
            text="🏆 Difícil",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=lambda: self.ver_nivel(3),
            width=20,
            height=2
        )
        btn_dificil.pack(pady=10)
    
    def ver_nivel(self, nivel):
        """Navega a la vista del ranking de un nivel específico"""
        SalonFamaNivel(
            self.root,
            nivel,
            self.username_enc,
            self.volver_seleccion,
            self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7
        )
    
    def volver_seleccion(self):
        """Vuelve a la pantalla de selección de nivel"""
        self.crear_interfaz()
    
    def volver_menu(self):
        """Vuelve al menú principal"""
        if self.callback_volver:
            self.callback_volver()