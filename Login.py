import tkinter as tk
from tkinter import ttk, messagebox
import os
from face_gui import Face_Recognition
import encrip_aes
from PersonalizaciónUI import MenuPersonalizacion
import calendar
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class LoginAvatarsRooks:
    def __init__(self, root):
        self.root = root
        self.face_window = None
        self.root.title("Avatars vs Rooks - Desktop game")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Colores del tema
        self.bg_black = "#000000"
        self.bg_dark = "#1a1a1a"
        self.dark_gray = "#535353"
        self.red_primary = "#cc0000"
        self.red_dark = "#990000"
        self.white = "#FFFFFF"
        self.gray_text = "#CCCCCC"
        
        self.root.configure(bg=self.bg_black)
        self.center_window()
        
        self.users = {}
        self.cards = {}
        self.master_key = encrip_aes.load_or_create_key()
        self.load_users()
        self.load_cards()
        
        # Variables de tema
        self.dark_mode = True
        
        # Crear ambos frames pero no mostrarlos aún
        self.login_frame = None
        self.register_frame = None
        
        self.create_login_widgets()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Para guardar la foto
        self.profile_photo_path = None
        self.profile_photo_display = None
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1024 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.root.geometry(f'1000x600+{x}+{y}')
    
    def load_users(self):
        """Carga todos los datos de usuarios"""
        try:
            datos = encrip_aes.load_users_aes()
            self.users = {}
            
            for username, user_data in datos.items():
                self.users[username] = {
                    'password_hash': user_data['password_hash'],
                    'nombre': encrip_aes.decrypt_data(user_data['nombre_enc'], self.master_key),
                    'apellidos': encrip_aes.decrypt_data(user_data['apellidos_enc'], self.master_key),
                    'nacionalidad': encrip_aes.decrypt_data(user_data['nacionalidad_enc'], self.master_key),
                    'correo': encrip_aes.decrypt_data(user_data['email_enc'], self.master_key)
                }
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            self.users = {}

    def load_cards(self):
        """Carga datos de tarjetas"""
        try:
            cartas = encrip_aes.load_cards_aes()
            self.cards = {}
            
            for username, card_data in cartas.items():
                self.cards[username] = {
                    'numero': encrip_aes.decrypt_data(card_data['numero_enc'], self.master_key),
                    'expiry': encrip_aes.decrypt_data(card_data['expiry_enc'], self.master_key),
                    'cvv': card_data['cvv_hash'],
                    'titular': encrip_aes.decrypt_data(card_data['titular_enc'], self.master_key)
                }
        except Exception as e:
            print(f"Error al cargar tarjetas: {e}")
            self.cards = {}

    def create_login_widgets(self):
        """Crea la interfaz de login siguiendo el diseño de referencia"""
        
        # Frame principal sin borde
        self.login_frame = tk.Frame(self.root, bg=self.bg_black)
        
        # BARRA SUPERIOR
        top_bar = tk.Frame(self.login_frame, bg=self.red_primary, height=40)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Título en la barra
        tk.Label(
            top_bar,
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            fg=self.white,
            bg=self.red_primary
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # ÁREA DE CONTENIDO
        content_area = tk.Frame(self.login_frame, bg=self.bg_black)
        content_area.pack(fill=tk.BOTH, expand=True)
        
        # Botones superiores izquierdos
        left_buttons_frame = tk.Frame(content_area, bg=self.bg_black)
        left_buttons_frame.place(x=20, y=20)
        
        self.create_round_button(
            left_buttons_frame,
            "Ayuda",
            lambda: messagebox.showinfo("Ayuda", "Sección de ayuda")
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_round_button(
            left_buttons_frame,
            "Créditos",
            lambda: self.show_credits()
        ).pack(side=tk.LEFT, padx=5)
        
        # Botones superiores derechos
        right_buttons_frame = tk.Frame(content_area, bg=self.bg_black)
        right_buttons_frame.place(relx=1.0, x=-20, y=20, anchor='ne')
        
        # Botón reconocimiento facial
        try:
            # Cargar la imagen para reconocimiento facial
            face_icon = tk.PhotoImage(file="./images/face_icon.png")  
            face_icon = face_icon.subsample(8, 8)

        except:
            face_icon = None

        face_btn = tk.Button(
            right_buttons_frame,
            image=face_icon,
            text="👤" if not face_icon else "",
            font=("Arial", 16),
            bg=self.red_primary,
            fg=self.white,
            width=40, 
            height=40,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.face_recognition
        )
        face_btn.pack(side=tk.LEFT, padx=5)

        if face_icon:
            face_btn.image = face_icon

        # Botón modo oscuro
        try:
            # Cargar la imagen para modo oscuro
            dark_icon = tk.PhotoImage(file="./images/moon.png")  
            dark_icon = dark_icon.subsample(4, 4)
        except:
            dark_icon = None

        dark_mode_btn = tk.Button(
            right_buttons_frame,
            image=dark_icon,
            text="🌙" if not dark_icon else "",
            font=("Arial", 16),
            bg=self.red_primary,
            fg=self.white,
            width=40,  
            height=40,  
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.set_theme("dark")
        )
        dark_mode_btn.pack(side=tk.LEFT, padx=5)

        if dark_icon:
            dark_mode_btn.image = dark_icon

        # Botón modo claro
        try:
            # Cargar la imagen para modo claro
            light_icon = tk.PhotoImage(file="./images/sun.png")  
            light_icon = light_icon.subsample(15, 15)
        except:
            light_icon = None

        light_mode_btn = tk.Button(
            right_buttons_frame,
            image=light_icon,
            text="☀️" if not light_icon else "",
            font=("Arial", 16),
            bg=self.white,
            fg=self.bg_black,
            width=40,  # Ancho en píxeles
            height=40,  # Alto en píxeles
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.set_theme("light")
        )
        light_mode_btn.pack(side=tk.LEFT, padx=5)

        if light_icon:
            light_mode_btn.image = light_icon
        
        # CONTENEDOR CENTRAL DE LOGIN
        login_container = tk.Frame(content_area, bg=self.bg_black)
        login_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        title_label = tk.Label(
            login_container,
            text="AVATARS VS ROOKS",
            font=("Arial", 30, "bold"),
            fg=self.white,
            bg=self.bg_black
        )
        title_label.pack(pady=(0, 40))
        
        # Frame del formulario
        form_frame = tk.Frame(login_container, bg=self.bg_black)
        form_frame.pack()
        
        # Campo Identificador
        tk.Label(
            form_frame,
            text="Identificador",
            font=("Arial", 11, "bold"),
            fg=self.white,
            bg=self.bg_black
        ).pack(anchor='w', pady=(0, 5))

        username_frame = tk.Frame(form_frame, bg=self.white)
        username_frame.pack(pady=(0, 20))

        self.username_entry = tk.Entry(
            username_frame, 
            font=("Arial", 12),
            bg=self.white,
            fg="#000000",
            width=44,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.username_entry.pack(side=tk.LEFT, padx=5, pady=5) 
        self.username_entry.insert(0, "Ingrese su usuario, correo o telefono")
        self.username_entry.config(fg=self.dark_gray)
        self.username_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese su usuario, correo o telefono"))
        self.username_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese su usuario, correo o telefono"))

        # Campo Contraseña
        tk.Label(
            form_frame,
            text="Contraseña",
            font=("Arial", 11, "bold"),
            fg=self.white,
            bg=self.bg_black
        ).pack(anchor='w', pady=(0, 5))
        
        password_frame = tk.Frame(form_frame, bg=self.white)
        password_frame.pack(pady=(0, 5))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            bg=self.white,
            fg="#000000",
            width=40,
            show="",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.password_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.password_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.password_entry.insert(0, "Ingrese su contraseña")
        self.password_entry.config(fg=self.dark_gray)
        self.password_entry.bind('<FocusIn>', lambda e: self.clear_placeholder_password(e, "Ingrese su contraseña"))
        self.password_entry.bind('<FocusOut>', lambda e: self.restore_placeholder_password(e, "Ingrese su contraseña"))

        
        # Botón mostrar/ocultar contraseña
        self.show_pass_btn = tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 12),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=self.toggle_password
        )
        self.show_pass_btn.pack(side=tk.RIGHT, padx=5)
        
        # ¿Olvidaste la contraseña?
        forgot_pass_btn = tk.Label(
            form_frame,
            text="¿Olvidaste la contraseña?",
            font=("Arial", 9),
            fg=self.red_primary,
            bg=self.bg_black,
            cursor="hand2"
        )
        forgot_pass_btn.pack(pady=(5, 25))
        forgot_pass_btn.bind('<Button-1>', lambda e: self.forgot_password())
        
        # Botones de acción
        buttons_frame = tk.Frame(form_frame, bg=self.bg_black)
        buttons_frame.pack(pady=(0, 15))
        
        # Botón Iniciar sesión
        login_btn = tk.Button(
            buttons_frame,
            text="Iniciar sesión",
            font=("Arial", 12, "bold"),
            bg=self.red_primary,
            fg=self.white,
            width=19,
            height=1,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.red_dark,
            command=self.login
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón Registrarse
        register_btn = tk.Button(
            buttons_frame,
            text="Registrarse",
            font=("Arial", 12, "bold"),
            bg=self.red_primary,
            fg=self.white,
            width=19,
            height=1,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.red_dark,
            command=self.show_register_message
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón de iniciar sesion con google
        try:
            # Cargar la imagen del logo de Google
            google_logo = tk.PhotoImage(file="./images/google.png")  
            google_logo = google_logo.subsample(15, 15)  # Reducido de 15 a 8
        except:
            # Si hay error cargando la imagen, usar texto como fallback
            google_logo = None

        # Crear un frame contenedor para controlar el tamaño exacto
        google_frame = tk.Frame(form_frame, bg=self.red_primary, width=410, height=35)
        google_frame.pack(pady=(0, 10))
        google_frame.pack_propagate(False)  # Esto evita que el frame se ajuste al contenido

        google_btn = tk.Button(
            google_frame,
            text=" Iniciar sesión con  ",
            image=google_logo,
            compound=tk.RIGHT,
            font=("Arial", 12, "bold"),
            bg=self.red_primary,
            fg=self.white,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.red_dark,
            command=self.google_login
        )
        google_btn.pack(fill=tk.BOTH, expand=True) 

        if google_logo:
            google_btn.image = google_logo

        # Guardar referencia de la imagen para evitar que sea eliminada por el garbage collector
        if google_logo:
            google_btn.image = google_logo

        
    def create_round_button(self, parent, text, command):
        """Crea botones redondeados para la parte superior"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            bg=self.red_primary,
            fg=self.white,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            borderwidth=2,
            highlightthickness=0,
            command=command
        )
        # Simular bordes redondeados con configuración especial
        btn.config(
            highlightbackground=self.red_primary,
            highlightcolor=self.red_primary
        )
        return btn

    #Funciones que manejan los placeholders d elos campos del login
    def clear_placeholder(self, event, placeholder):
        """Limpia el placeholder al hacer focus"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="#000000")

    def restore_placeholder(self, event, placeholder):
        """Restaura el placeholder si el campo está vacío"""
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)
            event.widget.config(fg="#666666")

    def clear_placeholder_password(self, event, placeholder):
        """Limpia el placeholder al hacer focus"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="#000000", show="•") 

    def restore_placeholder_password(self, event, placeholder):
        """Restaura el placeholder si el campo está vacío"""
        if event.widget.get() == "":
            event.widget.config(show="") 
            event.widget.insert(0, placeholder)
            event.widget.config(fg=self.dark_gray)

    def toggle_password(self):
        """Muestra u oculta la contraseña"""
        if self.password_entry.cget('show') == '•':
            self.password_entry.config(show='')
            self.show_pass_btn.config(text='👁‍🗨')
        else:
            self.password_entry.config(show='•')
            self.show_pass_btn.config(text='👁')


    def set_theme(self, mode):
        """Cambia el tema según el modo seleccionado"""
        if mode == "dark":
            messagebox.showinfo("Tema", "Modo oscuro activado")
            # Aquí puedes agregar lógica para cambiar colores
        elif mode == "light":
            messagebox.showinfo("Tema", "Modo claro activado")
            # Aquí puedes agregar lógica para cambiar colores

    def forgot_password(self):
        """Recuperación de contraseña"""
        messagebox.showinfo("Recuperar contraseña", "Se enviará un correo de recuperación")

    def change_language(self):
        """Cambia el idioma"""
        messagebox.showinfo("Idioma", "Selector de idioma")

    def show_credits(self):
        """Muestra los créditos"""
        messagebox.showinfo(
            "Créditos",
            "Avatars VS Rooks\n\n" +
            "Desarrollado por:\n" +
            "Tu equipo de desarrollo\n\n" +
            "Tecnológico de Costa Rica\n" +
            "CE 1105 - Principios de Modelado"
        )

    def google_login(self):
        """Login con Google (simulado)"""
        messagebox.showinfo("Google Login", "Funcionalidad de Google OAuth en desarrollo")

    def show_register_message(self):
        """Muestra la ventana de registro"""
        self.show_register_window()

    def login(self):
        """Valida credenciales de usuario"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or username == "Ingrese su usuario, correo o telefono":
            messagebox.showerror("Error", "Por favor ingresa tu usuario")
            return
        
        if not password:
            messagebox.showerror("Error", "Por favor ingresa tu contraseña")
            return
        
        users_aes = encrip_aes.load_users_aes()
        
        if username in users_aes:
            try:
                if encrip_aes.verify_password(users_aes[username]['password_hash'], password):
                    nombre = encrip_aes.decrypt_data(users_aes[username]['nombre_enc'], self.master_key)
                    self.login_frame.pack_forget()
                    MenuPersonalizacion(self.root, username, nombre, self.reiniciar_login)

                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {e}")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def face_recognition(self):
        """Login con reconocimiento facial"""
        try:
            temp_root = tk.Toplevel(self.root)
            temp_root.grab_set()
            temp_root.focus_set()
            Face_Recognition(temp_root).login_with_face_gui()
            temp_root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error en el login facial: {e}")

    def update_days(self, event=None):
        "Actualizar los dias segun el mes y año seleccionados"
        try:
            month_name = self.month_combo.get()
            month = self.meses.index(month_name) + 1
            year = int(self.year_combo.get())

            #Obtener numero de dias en el mes
            import calendar
            days_in_month = calendar.monthrange(year, month)[1]

            #Actualizar valores de dias
            current_day = int(self.day_combo.get())
            self.day_combo['values'] = list(range(1, days_in_month + 1))

            #Si el dia es mayor que los dias del mes, ajustarlo
            if current_day > days_in_month:
                self.day_combo.set(days_in_month)
        except:
            pass

    #Seleccionar la foto
    def selec_profile_photo(self):
        file_path = filedialog.askopenfilename(
            title= "Seleccionar foto de perfil",
            filetypes=[
            ("Archivos de imagen", "*.jpg *.jpeg *.png"),
            ("JPG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            try: 
                with Image.open(file_path) as img:

                    if img.mode in ("RGBA", "LA", "P"):

                        background = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    elif img.mode != "RGB":
                        img = img.convert("RGB")
                    img.thumbnail((150,150), Image.Resampling.LANCZOS)
                    self.profile_photo_display = ImageTk.PhotoImage(img)
                
                self.photo_btn.config(
                    image=self.profile_photo_display,
                    text=""
                )

                self.photo_btn.image = self.profile_photo_display  # Mantener referencia
            
                messagebox.showinfo("Éxito", "Foto de perfil cargada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")


    def create_register_widgets(self):
        """Crea los widgets para el registro con tema oscuro"""
        self.register_frame = tk.Frame(self.root, bg=self.bg_black)
        
        # Contenedor principal con scroll
        canvas = tk.Canvas(self.register_frame, bg=self.bg_black, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.register_frame, orient="vertical", command=canvas.yview)
        scrollbar.config(bg=self.red_primary, troughcolor=self.bg_black)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_black)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Barra superior
        top_bar = tk.Frame(scrollable_frame, bg=self.red_primary, height=40)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        tk.Label(
            top_bar,
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            fg=self.white,
            bg=self.red_primary
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # Título Registro
        tk.Label(
            scrollable_frame,
            text="Registro",
            font=("Arial", 32, "bold"),
            fg=self.white,
            bg=self.bg_black
        ).pack(pady=(30, 40))
        
        # Frame del formulario con borde
        form_container = tk.Frame(scrollable_frame, bg=self.bg_black)
        form_container.pack(padx=300)
        
        form_frame = tk.Frame(
            form_container,
            bg=self.bg_black,
            highlightbackground=self.gray_text,
            highlightthickness=1
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Padding interno
        inner_frame = tk.Frame(form_frame, bg=self.bg_black)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # INFORMACIÓN PERSONAL
        tk.Label(
            inner_frame,
            text="Información personal",
            font=("Arial", 14, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 20))

        # Nombre
        tk.Label(
            inner_frame,
            text="Nombre +",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.nombre_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT
        )
        self.nombre_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.nombre_entry.insert(0, "Ingrese su nombre")
        self.nombre_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese su nombre"))
        self.nombre_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese su nombre"))

        # Apellidos
        tk.Label(
            inner_frame,
            text="Apellidos +",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.apellidos_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT
        )
        self.apellidos_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.apellidos_entry.insert(0, "Ingrese sus apellidos")
        self.apellidos_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese sus apellidos"))
        self.apellidos_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese sus apellidos"))

        # Foto de perfil
        tk.Label(
            inner_frame,
            text="Foto de perfil",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 10))
        
        self.photo_btn = tk.Button(
            inner_frame,
            text="+\nAgregar foto",
            font=("Arial", 10),
            bg=self.white,
            fg="#666666",
            width=10,
            height=4,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.selec_profile_photo
        )
        self.photo_btn.pack(anchor="w", pady=(0, 15))

        # Fecha de nacimiento
        tk.Label(
            inner_frame,
            text="Fecha de nacimiento +",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        combo_container = tk.Frame(inner_frame, bg=self.white, relief=tk.FLAT)
        combo_container.pack(fill=tk.X, pady=(0,15), ipady=5, ipadx=5)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                        fieldbackground=self.white,
                        background=self.white,
                        foreground="#000000",
                        borderwithd=0)
        #Dia
        self.day_combo = ttk.Combobox(combo_container, width=5, state="readonly",
                                      font=("Arial", 11), style="Custom.TCombobox")
        self.day_combo ["values"] = list(range(1, 32))
        self.day_combo.set(1)
        self.day_combo.pack(side="left", padx=5)

        #Mes
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.month_combo = ttk.Combobox(combo_container, width=12, state="readonly",
                                        font=("Arial", 11), style="Custom.TCombobox")
        self.month_combo["values"] = self.meses
        self.month_combo.set("Enero")
        self.month_combo.pack(side="left", padx=5)

        #Año
        years = list(range(2025, 1925, -1))
        self.year_combo = ttk.Combobox(combo_container, width=8, state="readonly",
                               font=("Arial", 11), style='Custom.TCombobox')
        self.year_combo['values'] = years
        self.year_combo.set(2000)
        self.year_combo.pack(side="left", padx=5)

        #Actualizar
        self.month_combo.bind('<<ComboboxSelected>>', self.update_days)
        self.year_combo.bind('<<ComboboxSelected>>', self.update_days)

        # Nacionalidad
        tk.Label(
            inner_frame,
            text="Nacionalidad +",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))

        nacionalidades = [
            "Alemana",
            "Argentina",
            "Australiana",
            "Boliviana",
            "Brasileña",
            "Canadiense",
            "Chilena",
            "China",
            "Colombiana",
            "Costarricense",
            "Cubana",
            "Dominicana",
            "Ecuatoriana",
            "Española",
            "Estadounidense",
            "Filipina",
            "Finlandesa",
            "Francesa",
            "Galésa",
            "Gualtemalteca",
            "Húngara",
            "Irlandésa",
            "Inglesa",
            "Japonesa",
            "Mexicana",
            "Nicaragüense",
            "Panameña",
            "Paraguaya",
            "Peruana",
            "Puertorriqueña",
            "Salvadoreña",
            "Uruguaya",
            "Venezolana",
        ]

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombox",
                        fieldbackground=self.white,
                        background=self.white,
                        foreground="#000000",
                        arrowcolor="#000000",
                        borderwithd=0,
                        relief=tk.FLAT)
        
        self.nacionalidad_combobox = ttk.Combobox(
            inner_frame,
            values=nacionalidades,
            font=("Arial", 11),
            state="readonly",
            style="Custom.TCombobox"
        )

        self.nacionalidad_combobox.pack(fill=tk.X, pady=(0,25), ipady=5)
        self.nacionalidad_combobox.set("Seleciona tu nacionalidad")

        # CUENTA Y SEGURIDAD
        tk.Label(
            inner_frame,
            text="Cuenta y seguridad",
            font=("Arial", 14, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(10, 20))
        
        # Usuario
        tk.Label(
            inner_frame,
            text="Usuario",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.usuario_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT
        )
        self.usuario_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.usuario_entry.insert(0, "Ingrese su usuario")
        self.usuario_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese su usuario"))
        self.usuario_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese su usuario"))

        # Correo electrónico
        tk.Label(
            inner_frame,
            text="Correo electrónico",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))

        self.correo_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT
        )
        self.correo_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.correo_entry.insert(0, "Ingrese su correo electronico")
        self.correo_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese su correo electronico"))
        self.correo_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese su correo electronico"))

        # Contraseña
        tk.Label(
            inner_frame,
            text="Contraseña",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        pass_frame1 = tk.Frame(inner_frame, bg=self.white)
        pass_frame1.pack(fill=tk.X, pady=(0, 15))
        
        self.new_pass_entry = tk.Entry(
            pass_frame1,
            font=("Arial", 11),
            show="•",
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.new_pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.new_pass_entry.insert(0, "Ingrese su contraseña")
        
        show_pass1_btn = tk.Button(
            pass_frame1,
            text="👁",
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.toggle_password_field(self.new_pass_entry, show_pass1_btn)
        )
        show_pass1_btn.pack(side=tk.RIGHT, padx=5)
        
        # Confirmar contraseña
        tk.Label(
            inner_frame,
            text="Confirmar contraseña",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        pass_frame2 = tk.Frame(inner_frame, bg=self.white)
        pass_frame2.pack(fill=tk.X, pady=(0, 25))
        
        self.confirm_pass_entry = tk.Entry(
            pass_frame2,
            font=("Arial", 11),
            show="•",
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.confirm_pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.confirm_pass_entry.insert(0, "Ingrese su contraseña")
        
        show_pass2_btn = tk.Button(
            pass_frame2,
            text="👁",
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.toggle_password_field(self.confirm_pass_entry, show_pass2_btn)
        )
        show_pass2_btn.pack(side=tk.RIGHT, padx=5)

        # RECONOCIMIENTO FACIAL (Opcional)
        tk.Label(
            inner_frame,
            text="Reconocimiento facial (Opcional)",
            font=("Arial", 14, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(10, 15))
        
        self.usar_facial_var = tk.BooleanVar()
        facial_check = tk.Checkbutton(
            inner_frame,
            text="Habilitar",
            variable=self.usar_facial_var,
            font=("Arial", 10),
            bg=self.bg_black,
            fg=self.white,
            activebackground=self.bg_black,
            selectcolor=self.bg_black,
            activeforeground=self.white
        )
        facial_check.pack(anchor="w", pady=(0, 10))
        
        self.facial_button = tk.Button(
            inner_frame,
            text="Capturar rostro",
            font=("Arial", 11, "bold"),
            bg=self.red_primary,
            fg=self.white,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.open_face_gui
        )
        self.facial_button.pack(fill=tk.X, pady=(0, 25), ipady=8)
        
        # Activar/desactivar botón según checkbox
        def toggle_facial_button():
            if self.usar_facial_var.get():
                self.facial_button.config(state=tk.NORMAL)
            else:
                self.facial_button.config(state=tk.DISABLED)
        
        facial_check.config(command=toggle_facial_button)

        # INFORMACIÓN DE PAGO (Opcional)
        tk.Label(
            inner_frame,
            text="Información de pago (opcional)",
            font=("Arial", 14, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(10, 15))
        
        self.guardar_tarjeta_var = tk.BooleanVar()
        tarjeta_check = tk.Checkbutton(
            inner_frame,
            text="Habilitar",
            variable=self.guardar_tarjeta_var,
            font=("Arial", 10),
            bg=self.bg_black,
            fg=self.white,
            activebackground=self.bg_black,
            selectcolor=self.bg_black,
            activeforeground=self.white
        )
        tarjeta_check.pack(anchor="w", pady=(0, 15))
        
        # Número de tarjeta
        tk.Label(
            inner_frame,
            text="Numero de tarjeta",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.num_tarjeta_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.num_tarjeta_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.num_tarjeta_entry.insert(0, "Numero de tarjeta")
        
        # Frame para fecha y CVV
        expiry_cvv_frame = tk.Frame(inner_frame, bg=self.bg_black)
        expiry_cvv_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Fecha de expiración
        expiry_left = tk.Frame(expiry_cvv_frame, bg=self.bg_black)
        expiry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(
            expiry_left,
            text="Fecha de expiración",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.expiry_entry = tk.Entry(
            expiry_left,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.expiry_entry.pack(fill=tk.X, ipady=5)
        
        # CVV
        cvv_right = tk.Frame(expiry_cvv_frame, bg=self.bg_black)
        cvv_right.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            cvv_right,
            text="CVV",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.cvv_entry = tk.Entry(
            cvv_right,
            font=("Arial", 11),
            show="*",
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.cvv_entry.pack(fill=tk.X, ipady=5)
        
        # Nombre del titular
        tk.Label(
            inner_frame,
            text="Nombre del titular",
            font=("Arial", 10, "bold"),
            bg=self.bg_black,
            fg=self.white
        ).pack(anchor="w", pady=(0, 5))
        
        self.titular_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.white,
            fg="#000000",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.titular_entry.pack(fill=tk.X, pady=(0, 30), ipady=5)
        
        # Función para activar/desactivar campos de tarjeta
        def toggle_tarjeta_fields():
            state = tk.NORMAL if self.guardar_tarjeta_var.get() else tk.DISABLED
            self.num_tarjeta_entry.config(state=state)
            self.expiry_entry.config(state=state)
            self.cvv_entry.config(state=state)
            self.titular_entry.config(state=state)
        
        tarjeta_check.config(command=toggle_tarjeta_fields)
        
        # BOTÓN REGISTRARSE
        tk.Button(
            scrollable_frame,
            text="Registrarse",
            font=("Arial", 12, "bold"),
            bg=self.red_primary,
            fg=self.white,
            width=20,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.red_dark,
            command=self.register_user
        ).pack(pady=(30, 50), ipady=8)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    def toggle_password_field(self, entry, button):
        """Muestra u oculta la contraseña en un campo específico"""
        if entry.cget('show') == '•':
            entry.config(show='')
            button.config(text='👁‍🗨')
        else:
            entry.config(show='•')
            button.config(text='👁')

    def show_login_window(self):
        """Muestra la ventana de login y oculta la de registro"""
        if hasattr(self, 'register_frame'):
            self.register_frame.pack_forget()
        if hasattr(self, 'login_frame'):
            self.login_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_register_window(self):
        """Muestra la ventana de registro y oculta la de login"""
        if not hasattr(self, 'register_frame') or self.register_frame is None:
            self.create_register_widgets()
        if hasattr(self, 'login_frame'):
            self.login_frame.pack_forget()
        self.register_frame.pack(fill=tk.BOTH, expand=True)

    def open_face_gui(self):
        """Abre la interfaz para capturar rostro"""
        self.root.attributes('-disabled', True)
        try:
            fr = Face_Recognition(self.root, show_main_gui=False)
            fr.register_face_gui()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar rostro: {e}")
        self.root.attributes('-disabled', False)

    def register_user(self):
        """Obtiene y guarda todos los datos del usuario al registrarse"""
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        nacionalidad = self.nacionalidad_combobox.get()
        correo = self.correo_entry.get()
        username = self.usuario_entry.get()
        password = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        # Validar que no sean placeholders
        if nombre == "Ingrese su nombre" or not nombre:
            messagebox.showerror("Error", "Por favor ingresa tu nombre")
            return
        
        if apellidos == "Ingrese sus apellidos" or not apellidos:
            messagebox.showerror("Error", "Por favor ingresa tus apellidos")
            return
            
        if nacionalidad == "Ingrese su nacionalidad" or not nacionalidad:
            messagebox.showerror("Error", "Por favor ingresa tu nacionalidad")
            return
        
        if correo == "Ingrese su correo electronico" or not correo:
            messagebox.showerror("Error", "Por favor ingresa tu correo")
            return
        
        if "@" not in correo or "." not in correo:
            messagebox.showerror("Error", "Por favor ingresa un correo electrónico válido")
            return
        
        if username == "Ingrese su usuario" or not username:
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario")
            return
        
        if password == "Ingrese su contraseña" or not password:
            messagebox.showerror("Error", "Por favor ingresa una contraseña")
            return
        
        if password != confirm_pass:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        users_aes = encrip_aes.load_users_aes()
        if username in users_aes:
            messagebox.showerror("Error", "El usuario ya existe")
            return
        
        try:
            encrip_aes.register_user_aes(username, password, nombre, correo, nacionalidad, apellidos)
            self.load_users()
            
            if self.guardar_tarjeta_var.get():
                numero = self.num_tarjeta_entry.get().strip()
                expiry = self.expiry_entry.get().strip()
                cvv = self.cvv_entry.get().strip()
                titular = self.titular_entry.get().strip()
                
                if numero and numero != "Numero de tarjeta" and expiry and cvv and titular:
                    encrip_aes.register_user_card(username, cvv, numero, expiry, titular)
                    self.load_cards()
            
            messagebox.showinfo("Éxito", "¡Registro exitoso!")
            self.show_login_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {e}")

    def reiniciar_login(self):
        """Recrea la interfaz de login"""
        self.create_login_widgets()
        self.login_frame.pack(fill=tk.BOTH, expand=True)