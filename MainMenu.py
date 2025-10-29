import tkinter as tk
from tkinter import messagebox
from PersonalizaciónUI import MenuPersonalizacion
from game_interface import GameInterface
from game_logic import set_nivel_actual
from SalonDeLaFama import SalonDeLaFama

class MainMenu:
    def __init__(self, root, username, nombre, tempo, popularidad, callback_login, c1, 
                 c2, c3, c4, c5, c6, c7, username_enc):
        " Menú Principal del juego Avatars vs Rooks"
        self.root = root
        self.username = username
        self.username_enc = username_enc
        self.nombre = nombre
        self.callback_login = callback_login
        self.tempo = tempo
        self.popularidad = popularidad
        
        # Colores recibidos
        self.c1 = c1  # Color principal/fondo
        self.c2 = c2  # Color secundario
        self.c3 = c3  # Color de botones
        self.c4 = c4  # Color de texto
        self.c5 = c5  # Color de acento
        self.c6 = c6  # Color de hover
        self.c7 = c7  # Color adicional

        self.cambio = not (self.c1 == "#000000" and self.c2 == "#1a1a1a" and self.c3 == "#535353" and self.c4 == "#cc0000" and self.c5 == "#990000" and self.c6 == "#FFFFFF" and self.c7 == "#CCCCCC")
        
        # Configurar ventana
        self.root.geometry("1000x600")
        self.frame = None
        self.center_window()
        self.create_interface()

    def center_window(self):
        "Centra la ventana en la pantalla"
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1000 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.root.geometry(f'1000x600+{x}+{y}')
    
    def create_interface(self):
        "Crea la interfaz del menú principal"

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
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            bg=self.c4,
            fg=self.c6
        ).pack(side=tk.LEFT, padx=15, pady=8)
            
        # Frame para botones superiores
        frame_superior = tk.Frame(self.frame, bg=self.c1, height=60)
        frame_superior.pack(fill="x", padx=30, pady=15)
        frame_superior.pack_propagate(False)
        
        # Botón Personalización de usuario (izquierda)
        btn_personalizacion = tk.Button(
            frame_superior,
            text="Personalización de usuario",
            font=("Arial", 10, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.go_to_customization,
            padx=12,
            pady=8
        )
        btn_personalizacion.pack(side="left")
        
        # Botón Salón de la fama (derecha)
        btn_salon_fama = tk.Button(
            frame_superior,
            text="Salón de la fama",
            font=("Arial", 10, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.go_to_hall_of_fame,
            padx=12,
            pady=8
        )
        btn_salon_fama.pack(side="right")
        
        # Frame central para contenido
        frame_central = tk.Frame(self.frame, bg=self.c1)
        frame_central.pack(expand=True, fill="both")
        
        # Título del juego
        label_titulo = tk.Label(
            frame_central,
            text="AVATARS VS ROOKS",
            font=("Arial", 32, "bold"),
            bg=self.c1,
            fg=self.c6
        )
        label_titulo.pack(pady=(20, 5))
        
        # Línea decorativa bajo el título
        linea = tk.Frame(frame_central, bg=self.c4, height=6)
        linea.pack(pady=(0, 30))
        linea.configure(width=450)
        
        # Frame para los botones de niveles (centrado)
        frame_botones = tk.Frame(frame_central, bg=self.c1)
        frame_botones.pack(pady=10)
        
        # Botón Nivel 1 (Fácil)
        btn_nivel1 = tk.Button(
            frame_botones,
            text="Fácil",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.start_level1,
            width=20,
            height=2
        )
        btn_nivel1.pack(pady=10)
        
        # Botón Nivel 2 (Medio)
        btn_nivel2 = tk.Button(
            frame_botones,
            text="Medio",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.start_level2,
            width=20,
            height=2
        )
        btn_nivel2.pack(pady=10)
        
        # Botón Nivel 3 (Difícil)
        btn_nivel3 = tk.Button(
            frame_botones,
            text="Difícil",
            font=("Arial", 14, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.start_level3,
            width=20,
            height=2
        )
        btn_nivel3.pack(pady=10)

        # Frame inferior para botón de cerrar sesión
        frame_inferior = tk.Frame(self.frame, bg=self.c1, height=60)
        frame_inferior.pack(side="bottom", fill="x", padx=30, pady=15)
        frame_inferior.pack_propagate(False)
        
        # Botón Cerrar sesión
        btn_cerrar_sesion = tk.Button(
            frame_inferior,
            text="Cerrar sesión",
            font=("Arial", 10, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief="flat",
            cursor="hand2",
            command=self.close_session,
            padx=12,
            pady=8
        )
        btn_cerrar_sesion.pack(side="left")
    
    def go_to_customization(self):
        "Navega a la personalización de usuario"
        MenuPersonalizacion(self.root, self.username, self.nombre, self.callback_login, self.reset_MainMenu,
                            self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7)
    
    def go_to_hall_of_fame(self):
        "Navega al salón de la fama"
        SalonDeLaFama(
            self.root,
            self.username_enc,  
            self.volver_desde_salon_fama,
            self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7
        )

    def volver_desde_salon_fama(self):
        "Vuelve del salon de la fama al menu principal"
        if self.frame:
            self.frame.destroy()
        self.create_interface()
    

    def start_level1(self):
        set_nivel_actual(1)
        self.root.withdraw()
        root_nivel1 = tk.Toplevel(self.root)
        root_nivel1.title("Avatars vs Rooks - Nivel 1 (Fácil)")
        if self.cambio:
            GameInterface(root_nivel1, 
                callback_volver_menu=lambda iniciar_nuevo_nivel=False: self.regresar_menu(root_nivel1, iniciar_nuevo_nivel),
                tempo=self.tempo, 
                popularidad=self.popularidad,
                username_enc=self.username_enc,
                c1=self.c1, c2=self.c2, c3=self.c3, c4=self.c4, c5=self.c5, c6=self.c6, c7=self.c7
                )
        else:
            GameInterface(root_nivel1, 
                callback_volver_menu=lambda iniciar_nuevo_nivel=False: self.regresar_menu(root_nivel1, iniciar_nuevo_nivel),
                tempo=self.tempo, 
                popularidad=self.popularidad,
                username_enc=self.username_enc
                )

    def start_level2(self):
        set_nivel_actual(2)
        self.root.withdraw()
        root_nivel2 = tk.Toplevel(self.root)
        root_nivel2.title("Avatars vs Rooks - Nivel 2 (Medio)")
        if self.cambio:
            GameInterface(root_nivel2, 
                callback_volver_menu=lambda iniciar_nuevo_nivel=False: self.regresar_menu(root_nivel2, iniciar_nuevo_nivel),
                tempo=self.tempo, 
                popularidad=self.popularidad,
                username_enc=self.username_enc,
                c1=self.c1, c2=self.c2, c3=self.c3, c4=self.c4, c5=self.c5, c6=self.c6, c7=self.c7
                )
        else:
            GameInterface(root_nivel2, 
                callback_volver_menu=lambda iniciar_nuevo_nivel=False: self.regresar_menu(root_nivel2, iniciar_nuevo_nivel),
                tempo=self.tempo, 
                popularidad=self.popularidad,
                username_enc=self.username_enc
                )


    def start_level3(self):
        set_nivel_actual(3)
        self.root.withdraw()
        root_nivel3 = tk.Toplevel(self.root)
        root_nivel3.title("Avatars vs Rooks - Nivel 3 (Difícil)")
        if self.cambio:
            GameInterface(root_nivel3, 
                callback_volver_menu=lambda iniciar_nuevo_nivel=False: self.regresar_menu(root_nivel3, iniciar_nuevo_nivel),
                tempo=self.tempo, 
                popularidad=self.popularidad,
                username_enc=self.username_enc,
                c1=self.c1, c2=self.c2, c3=self.c3, c4=self.c4, c5=self.c5, c6=self.c6, c7=self.c7
                )
        else:
            GameInterface(root_nivel3, 
                callback_volver_menu=lambda iniciar_nuevo_nivel=False: self.regresar_menu(root_nivel3, iniciar_nuevo_nivel),
                tempo=self.tempo, 
                popularidad=self.popularidad,
                username_enc=self.username_enc
                )



    def regresar_menu(self, ventana_juego, iniciar_nuevo_nivel=False):
        ventana_juego.destroy()
        self.root.deiconify()

        if iniciar_nuevo_nivel:
            from game_logic import NIVEL_ACTUAL

            if NIVEL_ACTUAL == 1:
                self.start_level1()
            elif NIVEL_ACTUAL == 2:
                self.start_level2()
            elif NIVEL_ACTUAL == 3:
                self.start_level3()




    def reset_MainMenu(self, username, name,tempo, popularidad, c1=None, c2=None, c3=None, 
                       c4=None, c5=None, c6=None, c7=None):
        """Reinicia y muestra el menú principal con los datos actualizados"""
        # Actualizar colores si se proporcionan nuevos valores

        self.tempo = tempo
        self.popularidad = popularidad

        if c1 is not None:
            self.c1 = c1
        if c2 is not None:
            self.c2 = c2
        if c3 is not None:
            self.c3 = c3
        if c4 is not None:
            self.c4 = c4
        if c5 is not None:
            self.c5 = c5
        if c6 is not None:
            self.c6 = c6
        if c7 is not None:
            self.c7 = c7
        
        if self.frame:
            self.frame.destroy()
        
        self.create_interface()

    def close_session(self):
        """Callback para volver a login"""
        self.callback_login(self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7)
