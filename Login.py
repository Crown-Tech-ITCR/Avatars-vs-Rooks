import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Toplevel, Button
import os
from face_gui import Face_Recognition
import encrip_aes
from PersonalizaciónUI import MenuPersonalizacion
import calendar
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from password_recovery import PasswordRecovery
from Traducciones import t, set_language
from PIL import Image, ImageTk
from Modos import apply_dark_mode, apply_light_mode


class LoginAvatarsRooks:
    def __init__(self, root):
        self.root = root
        self.face_window = None
        self.root.title("Avatars vs Rooks - Desktop game")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Colores del tema
        self.c1 = "#000000"
        self.c2 = "#1a1a1a"
        self.c3 = "#535353"
        self.c4 = "#cc0000"
        self.c5 = "#990000"
        self.c6 = "#FFFFFF"
        self.c7 = "#CCCCCC"

        self.colors = [self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7]
        self.bg_black = self.c1

        self.root.configure(bg=self.colors[0])
        self.center_window()
        
        self.users = {}
        self.cards = {}
        self.master_key = encrip_aes.load_or_create_key()
        self.password_recovery = PasswordRecovery(self.master_key)
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
        """Crea la interfaz de login"""
        
        # Frame principal sin borde
        self.login_frame = tk.Frame(self.root, bg=self.colors[0])
        
        # BARRA SUPERIOR
        top_bar = tk.Frame(self.login_frame, bg=self.colors[3], height=40)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Título en la barra
        tk.Label(
            top_bar,
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            fg=self.colors[5],
            bg=self.colors[3]
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # ÁREA DE CONTENIDO
        content_area = tk.Frame(self.login_frame, bg=self.colors[0])
        content_area.pack(fill=tk.BOTH, expand=True)
        
        # Botones superiores izquierdos
        left_buttons_frame = tk.Frame(content_area, bg=self.colors[0])
        left_buttons_frame.place(x=20, y=20)
        
        self.help_btn = self.create_round_button(
            left_buttons_frame,
            t("help_button"),
            self.show_help
        )
        self.help_btn.pack(side=tk.LEFT, padx=5)

        self.credits_btn = self.create_round_button(
            left_buttons_frame,
            t("credits_button"),
            lambda: self.show_credits()
        )
        self.credits_btn.pack(side=tk.LEFT, padx=5)
        
        # Botones superiores derechos
        right_buttons_frame = tk.Frame(content_area, bg=self.colors[0])
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
            bg=self.colors[3],
            fg=self.colors[5],
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
            bg=self.colors[3],
            fg=self.colors[5],
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
            bg=self.colors[5],
            fg=self.colors[0],
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
        login_container = tk.Frame(content_area, bg=self.colors[0])
        login_container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        self.title_label = tk.Label(
            login_container,
            text=t("login_title"),
            font=("Arial", 30, "bold"),
            fg=self.colors[5],
            bg=self.colors[0]
        )
        self.title_label.pack(pady=(0, 40))
        
        # Frame del formulario
        form_frame = tk.Frame(login_container, bg=self.colors[0])
        form_frame.pack()
        
        # Campo Identificador
        self.username_label = tk.Label(
            form_frame,
            text=t("username"),
            font=("Arial", 11, "bold"),
            fg=self.colors[5],
            bg=self.colors[0]
        )
        self.username_label.pack(anchor='w', pady=(0, 5))

        username_frame = tk.Frame(form_frame, bg=self.colors[5])
        username_frame.pack(pady=(0, 20))

        self.username_entry = tk.Entry(
            username_frame, 
            font=("Arial", 12),
            bg=self.colors[5],
            fg=self.colors[0],
            width=44,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.username_entry.pack(side=tk.LEFT, padx=5, pady=5) 
        self.username_entry.insert(0, t("username_placeholder"))
        self.username_entry.config(fg=self.colors[1])
        self.username_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, t("username_placeholder")))
        self.username_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, t("username_placeholder")))

        # Campo Contraseña
        self.password_label = tk.Label(
            form_frame,
            text=t("password"),
            font=("Arial", 11, "bold"),
            fg=self.colors[5],
            bg=self.colors[0]
        )
        self.password_label.pack(anchor='w', pady=(0, 5))

        password_frame = tk.Frame(form_frame, bg=self.colors[5])
        password_frame.pack(pady=(0, 5))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            bg=self.colors[5],
            fg=self.colors[0],
            width=40,
            show="",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.password_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.password_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.password_entry.insert(0, t("password_placeholder"))
        self.password_entry.config(fg=self.colors[1])
        self.password_entry.bind('<FocusIn>', lambda e: self.clear_placeholder_password(e, t("password_placeholder")))
        self.password_entry.bind('<FocusOut>', lambda e: self.restore_placeholder_password(e, t("password_placeholder")))

        # Botón mostrar/ocultar contraseña
        self.show_pass_btn = tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 12),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=self.toggle_password
        )
        self.show_pass_btn.pack(side=tk.RIGHT, padx=5)
        
        # ¿Olvidaste la contraseña?
        self.forgot_pass_btn = tk.Label(
            form_frame,
            text=t("forgot_password"),
            font=("Arial", 9),
            fg=self.colors[3],
            bg=self.colors[0],
            cursor="hand2"
        )
        self.forgot_pass_btn.pack(pady=(5, 25))
        self.forgot_pass_btn.bind('<Button-1>', lambda e: self.forgot_password())
        
        # Botones de acción
        buttons_frame = tk.Frame(form_frame, bg=self.colors[0])
        buttons_frame.pack(pady=(0, 15))
        
        # Botón Iniciar sesión
        self.login_btn = tk.Button(
            buttons_frame,
            text=t("login_button"),
            font=("Arial", 12, "bold"),
            bg=self.colors[3],
            fg=self.colors[5],
            width=19,
            height=1,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors[4],
            command=self.login
        )
        self.login_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón Registrarse
        self.register_btn = tk.Button(
            buttons_frame,
            text=t("register_button"),
            font=("Arial", 12, "bold"),
            bg=self.colors[3],
            fg=self.colors[5],
            width=19,
            height=1,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors[4],
            command=self.show_register_message
        )
        self.register_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón de iniciar sesion con google
        try:
            # Cargar la imagen del logo de Google
            google_logo = tk.PhotoImage(file="./images/google.png")  
            google_logo = google_logo.subsample(15, 15)  # Reducido de 15 a 8
        except:
            # Si hay error cargando la imagen, usar texto como fallback
            google_logo = None

        
        google_frame = tk.Frame(form_frame, bg=self.colors[3], width=410, height=35)
        google_frame.pack(pady=(0, 10))
        google_frame.pack_propagate(False)  # Esto evita que el frame se ajuste al contenido

        self.google_btn = tk.Button(
            google_frame,
            text=t("google_login"),
            image=google_logo,
            compound=tk.RIGHT,
            font=("Arial", 12, "bold"),
            bg=self.colors[3],
            fg=self.colors[5],
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors[4],
            command=self.google_login
        )
        self.google_btn.pack(fill=tk.BOTH, expand=True) 

        if google_logo:
            self.google_btn.image = google_logo

        # Guardar referencia de la imagen para evitar que sea eliminada por el garbage collector
        if google_logo:
            self.google_btn.image = google_logo
        #Boton de banderas
        bottom_right_frame = tk.Frame(self.login_frame, bg=self.bg_black)
        bottom_right_frame.place(relx=1.0, rely=1.0, anchor='se')
        self.add_language_selector(bottom_right_frame)

        
    def create_round_button(self, parent, text, command):
        """Crea botones redondeados para la parte superior"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 10, "bold"),
            bg=self.colors[3],
            fg=self.colors[5],
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
            highlightbackground=self.colors[3],
            highlightcolor=self.colors[3]
        )
        return btn

    #Funciones que manejan los placeholders d elos campos del login
    def clear_placeholder(self, event, placeholder):
        """Limpia el placeholder al hacer focus"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg=self.colors[0])

    def restore_placeholder(self, event, placeholder):
        """Restaura el placeholder si el campo está vacío"""
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)
            event.widget.config(fg=self.colors[2])

    def clear_placeholder_password(self, event, placeholder_text):
        """Limpia el placeholder de los campos de contraseña"""
        entry = event.widget
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(show="•", fg=self.c1) 

    def restore_placeholder_password(self, event, placeholder_text):
        """Restaura el placeholder si el campo está vacío"""
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(show="", fg=self.c3) 

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
            apply_dark_mode(self)
        elif mode == "light":
            apply_light_mode(self)

         

    def forgot_password(self):
        """Recuperación de contraseña"""
        messagebox.showinfo("Recuperar contraseña", "Se enviará un correo de recuperación")

    def change_language(self):
        """Cambia el idioma"""
        messagebox.showinfo("Idioma", "Selector de idioma")

    def show_credits(self):
        ventana_creditos = Toplevel()
        ventana_creditos.title(t("credits_title"))
        ventana_creditos.geometry("850x650")
        ventana_creditos.config(bg=self.colors[0])

        # --- Título ---
        titulo = Label(
            ventana_creditos,
            text=t("credits_title"),
            font=("Arial Black", 16),
            fg=self.colors[6],
            bg=self.colors[0]
        )
        titulo.pack(pady=20)

        # --- Frame principal---
        frame_equipo = Frame(ventana_creditos, bg=self.colors[0])
        frame_equipo.pack(expand=True)

        # --- Lista de integrantes ---
        integrantes = [
            {"nombre": "Alanna Mendoza", "rol": t("credits_leader"), "descripcion": t("credits_leader"), "foto": "./images/Alanna.png"},
            {"nombre": "Fabricio Coto", "rol": t("credits_admin"), "descripcion": t("credits_member"), "foto": "./images/Fabricio.png"},
            {"nombre": "Ariel Rodriguez", "rol": t("credits_ux"), "descripcion": t("credits_member"), "foto": "./images/Ariel.png"},
            {"nombre": "Mauricio Lopez", "rol": t("credits_tester"), "descripcion": t("credits_member"), "foto": "./images/Mau.png"},
        ]

        # --- Cargar imágenes---
        columnas = 2
        for i, miembro in enumerate(integrantes):
            fila = i // columnas
            columna = i % columnas

            # Marco individual
            card = Frame(frame_equipo, bg=self.colors[1], bd=2, relief="ridge", padx=10, pady=10, width=320, height=300)
            card.grid(row=fila, column=columna, padx=25, pady=25, sticky="nsew")

            # Imagen
            try:
                imagen = Image.open(miembro["foto"]).resize((100, 100))
                imagen = ImageTk.PhotoImage(imagen)
                img_label = Label(card, image=imagen, bg=self.colors[1])
                img_label.image = imagen
                img_label.pack(pady=5)
            except:
                Label(card, text="[Foto]", fg=self.colors[6], bg=self.colors[1]).pack(pady=5)

            # Nombre
            Label(card, text=miembro["nombre"], font=("Arial", 12, "bold"), fg=self.colors[6], bg=self.colors[1]).pack(pady=2)
            # Rol
            Label(card, text=miembro["rol"], font=("Arial", 10, "italic"), fg=self.colors[3], bg=self.colors[1]).pack()
            # Descripción
            Label(card, text=miembro["descripcion"], font=("Arial", 9), fg=self.colors[6], bg=self.colors[1], wraplength=200, justify="center").pack(pady=5)

        # --- Botón para cerrar ---
        boton_cerrar = Button(
            ventana_creditos,
            text=t("credits_back"),
            font=("Arial Black", 11),
            bg=self.colors[4],
            fg=self.colors[6],
            activebackground=self.colors[3],
            activeforeground=self.colors[6],
            command=ventana_creditos.destroy
        )
        boton_cerrar.pack(pady=10)
    
    
    def show_help(self):
        ventana_ayuda = Toplevel()
        ventana_ayuda.title(t("help_title"))
        ventana_ayuda.geometry("700x500")
        ventana_ayuda.config(bg=self.colors[0])

        # --- Título ---
        titulo = Label(
            ventana_ayuda,
            text=t("help_title"),
            font=("Arial Black", 16),
            fg=self.colors[6],
            bg=self.colors[0]
        )
        titulo.pack(pady=20)

        # --- Contenedor principal ---
        frame_texto = Frame(ventana_ayuda, bg=self.colors[0])
        frame_texto.pack(padx=40, pady=10, fill="both", expand=True)

        # --- Secciones de ayuda ---
        secciones = [
            {"titulo": t("help_section_login"), "texto": t("help_section_login_text")},
            {"titulo": t("help_section_register"), "texto": t("help_section_register_text")},
            {"titulo": t("help_section_forgot"), "texto": t("help_section_forgot_text")},
        ]

        # --- Mostrar texto en pantalla ---
        for sec in secciones:
            Label(
                frame_texto,
                text=sec["titulo"],
                font=("Arial Black", 12),
                fg=self.colors[3],
                bg=self.colors[0],
                anchor="w",
                justify="left"
            ).pack(anchor="w", pady=(10, 0))
            Label(
                frame_texto,
                text=sec["texto"],
                font=("Arial", 10),
                fg=self.colors[6],
                bg=self.colors[0],
                wraplength=600,
                justify="left"
            ).pack(anchor="w", pady=(0, 10))

        # --- Botón Volver ---
        boton_cerrar = Button(
            ventana_ayuda,
            text=t("help_back"),
            font=("Arial Black", 11),
            bg=self.colors[4],
            fg=self.colors[6],
            activebackground=self.colors[3],
            activeforeground=self.colors[6],
            command=ventana_ayuda.destroy
        )
        boton_cerrar.pack(pady=10)


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

        if not username or username == t("username_placeholder"):
            messagebox.showerror(t("user_error"))
            return
        
        if not password:
            messagebox.showerror(t("password_error"))
            return
        
        users_aes = encrip_aes.load_users_aes()
        
        if username in users_aes:
            try:
                if encrip_aes.verify_password(users_aes[username]['password_hash'], password):
                    nombre = encrip_aes.decrypt_data(users_aes[username]['nombre_enc'], self.master_key)
                    primerIngreso = users_aes[username]['primerIngreso']
                    if primerIngreso:
                        self.login_frame.pack_forget()
                        users_aes[username]['primerIngreso'] = False
                        encrip_aes.save_users_aes(users_aes)
                        MenuPersonalizacion(self.root, username, nombre, self.reiniciar_login, 
                        self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7)
                    else:
                        messagebox.showinfo(t("user_ver"))

                else:
                    messagebox.showerror(t("error_uc"))
            except Exception as e:
                messagebox.showerror(t("error_credentials").format(error=e))
        else:
            messagebox.showerror(t("error_uc"))

    def face_recognition(self):
        """Login con reconocimiento facial"""
        try:
            temp_root = tk.Toplevel(self.root)
            temp_root.grab_set()
            temp_root.focus_set()
            Face_Recognition(temp_root).login_with_face_gui()
            temp_root.destroy()
        except Exception as e:
            messagebox.showerror(t("error_facial").format(error=e))

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
            title= t("photo_perfil"),
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
            
                messagebox.showinfo(t("succes_photo"))
            except Exception as e:
                messagebox.showerror(t("error_photo").format(error=e))
    
    def forgot_password(self):
        self.login_frame.pack_forget()

        recovery_frame = tk.Frame(self.root, bg=self.bg_black)
        recovery_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            recovery_frame, 
            text=t("recover_password"),
            font=("Arial", 24, "bold"),
            fg=self.c4,
            bg=self.bg_black
        )
        title_label.pack(pady=30)

        form_frame = tk.Frame(recovery_frame, bg="#FF0000", width=400, height=300)
        form_frame.pack(pady=20, padx=50)
        form_frame.pack_propagate(False)

        #Paso 1 Ingresar Usuario
        tk.Label(
            form_frame,
            text=t("enter_username"),
            font=("Arial", 12),
            fg=self.c6,
            bg=self.bg_black
        ).pack(pady=(20, 10))
    
        username_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            bg=self.c2,
            fg=self.c6,
            insertbackground=self.c6,
            relief=tk.FLAT,
            width=30
        )
        username_entry.pack(pady=10, ipady=8)
    
        def verify_user():
            username = username_entry.get().strip()

            if not username:
                messagebox.showerror(t("error_username"))
                return
            #Verificar si el usuario existe
            users = encrip_aes.load_users_aes()
            if username not in users:
                messagebox.showerror(t("error_usernot_found"))
                return
            
            if not self.password_recovery.user_has_security_question(username):
                messagebox.showerror(
                    t("error_usernot_question")
                )
                return
            question = self.password_recovery.get_security_question(username)

            if question:
                self.show_security_question(username,question)
            else:
                messagebox.showerror(t("error_recovery_question"))

        #Boton Continuar
        continue_btn = tk.Button(
            form_frame,
            text=t("continue"),
            font=("Arial", 11, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            command=verify_user
        )
        continue_btn.pack(pady=20, ipady=10, ipadx=40)
    
        # Botón volver
        back_btn = tk.Label(
            form_frame,
            text=t("return_login"),
            font=("Arial", 10),
            fg=self.c3,
            bg=self.c1,
            cursor="hand2"
        )
        back_btn.pack(pady=(10, 20))
        back_btn.bind('<Button-1>', lambda e: self.reiniciar_login())

    def show_security_question(self, username, question):
        """Muestra la pregunta de seguridad para verificar"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
    
        # Frame principal
        recovery_frame = tk.Frame(self.root, bg=self.bg_black)
        recovery_frame.pack(fill=tk.BOTH, expand=True)
    
        # Título
        tk.Label(
            recovery_frame,
            text=t("question_security"),
            font=("Arial", 24, "bold"),
            fg=self.c4,
            bg=self.bg_black
        ).pack(pady=30)
    
        # Frame del formulario
        form_frame = tk.Frame(recovery_frame, bg=self.c1)
        form_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)

        print("Form frame creado")
        print(f"widht: {form_frame.winfo_reqwidth()}")
        print(f"Height: {form_frame.winfo_reqheight()}")

    
        # Mostrar pregunta
        tk.Label(
            form_frame,
            text=question,
            font=("Arial", 12, "bold"),
            fg=self.c6,
            bg=self.c1,
            wraplength=400
        ).pack(pady=(20, 10))
    
        # Entry para respuesta
        tk.Label(
            form_frame,
            text=t("answer"),
            font=("Arial", 11),
            fg=self.c3,
            bg=self.c1
        ).pack(pady=(10, 5))
    
        answer_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            bg=self.c2,
            fg=self.c6,
            insertbackground=self.c6,
            relief=tk.FLAT,
            width=30
        )
        answer_entry.pack(pady=10, ipady=8)
    
        def verify_answer():
            answer = answer_entry.get().strip()
        
            if not answer:
                messagebox.showerror(t("enter_answer"))
                return
        
            # Verificar respuesta
            if self.password_recovery.verify_security_answer(username, answer):
                self.show_reset_password(username)
            else:
                messagebox.showerror(t("answer_incorrect"))
                answer_entry.delete(0, tk.END)
    
        # Botón verificar
        verify_btn = tk.Button(
            form_frame,
            text=t("verify"),
            font=("Arial", 11, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            command=verify_answer
        )
        verify_btn.pack(pady=20, ipady=10, ipadx=40)
    
        # Botón cancelar
        cancel_btn = tk.Label(
            form_frame,
            text=t("cancel"),
            font=("Arial", 10),
            fg=self.c3,
            bg=self.c1,
            cursor="hand2"
        )
        cancel_btn.pack(pady=(10, 20))
        cancel_btn.bind('<Button-1>', lambda e: self.reiniciar_login())
    
    def show_reset_password(self, username):
        """Muestra el formulario para restablecer contraseña"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
    
        # Frame principal
        recovery_frame = tk.Frame(self.root, bg=self.bg_black)
        recovery_frame.pack(fill=tk.BOTH, expand=True)
    
        # Título
        tk.Label(
            recovery_frame,
            text=t("reset_password"),
            font=("Arial", 24, "bold"),
            fg=self.c4,
            bg=self.bg_black
        ).pack(pady=30)
    
        # Frame del formulario
        form_frame = tk.Frame(recovery_frame, bg=self.c1)  # Cambiar bg="#FF0000" por bg=self.c1
        form_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
    
        # Nueva contraseña
        tk.Label(
            form_frame,
            text=t("new_password"),
            font=("Arial", 11),
            fg=self.c6,
            bg="#FF0000"
        ).pack(pady=(20, 5), anchor="w", padx=20)
    
        new_password_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            bg=self.c2,
            fg=self.c6,
            insertbackground=self.c6,
            relief=tk.FLAT,
            show="*",
            width=30
        )
        new_password_entry.pack(pady=5, ipady=8, padx=20)
    
        # Confirmar contraseña
        tk.Label(
            form_frame,
            text=t("confirm_password"),
            font=("Arial", 11),
            fg=self.c6,
            bg="#FF0000"
        ).pack(pady=(15, 5), anchor="w", padx=20)
    
        confirm_password_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            bg=self.c2,
            fg=self.c6,
            insertbackground=self.c6,
            relief=tk.FLAT,
            show="*",
            width=30
        )
        confirm_password_entry.pack(pady=5, ipady=8, padx=20)
    
        def reset_password():
            new_pass = new_password_entry.get()
            confirm_pass = confirm_password_entry.get()
        
            if not all([new_pass, confirm_pass]):
                messagebox.showerror(t("error_enter_all"))
                return
        
            if new_pass != confirm_pass:
                messagebox.showerror(t("paswords_notmatch"))
                return
        
            if len(new_pass) < 4:  # Ajusta según tus requisitos
                messagebox.showerror(t("min_caracters"))
                return
        
            # Restablecer contraseña
            if self.password_recovery.reset_password(username, new_pass):
                messagebox.showinfo(
                t("successful_change")
                )
                self.reiniciar_login()
            else:
                messagebox.showerror(t("error_change"))
    
        # Botón restablecer
        reset_btn = tk.Button(
            form_frame,
            text=t("restore"),
            font=("Arial", 11, "bold"),
            bg=self.c4,
            fg=self.c6,
            activebackground=self.c5,
            activeforeground=self.c6,
            relief=tk.FLAT,
            cursor="hand2",
            command=reset_password
        )
        reset_btn.pack(pady=20, ipady=10, ipadx=40)
    
        # Botón cancelar
        cancel_btn = tk.Label(
            form_frame,
            text=t("cancel"),
            font=("Arial", 10),
            fg=self.c3,
            bg="#FF0000",
            cursor="hand2"
        )
        cancel_btn.pack(pady=(10, 20))
        cancel_btn.bind('<Button-1>', lambda e: self.reiniciar_login())


    def create_register_widgets(self):
        """Crea los widgets para el registro con tema oscuro"""
        self.register_frame = tk.Frame(self.root, bg=self.colors[0])  # ✅ Correcto
        
        # Contenedor principal con scroll
        canvas = tk.Canvas(self.register_frame, bg=self.colors[0], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.register_frame, orient="vertical", command=canvas.yview)
        scrollbar.config(bg=self.colors[3], troughcolor=self.colors[0])
        scrollable_frame = tk.Frame(canvas, bg=self.colors[0])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Barra superior
        top_bar = tk.Frame(scrollable_frame, bg=self.colors[3], height=40)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        tk.Label(
            top_bar,
            text="Avatars vs Rooks - Desktop game",
            font=("Arial", 12, "bold"),
            fg=self.colors[5],
            bg=self.colors[3]
        ).pack(side=tk.LEFT, padx=15, pady=8)
        
        # Título Registro
        tk.Label(
            scrollable_frame,
            text=t("register_title"),
            font=("Arial", 32, "bold"),
            fg=self.colors[5],
            bg=self.colors[0]
        ).pack(pady=(30, 40))
        
        # Frame del formulario con borde
        form_container = tk.Frame(scrollable_frame, bg=self.colors[0])
        form_container.pack(padx=300)
        
        form_frame = tk.Frame(
            form_container,
            bg=self.colors[0],
            highlightbackground=self.colors[6],
            highlightthickness=1
        )
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Padding interno
        inner_frame = tk.Frame(form_frame, bg=self.colors[0])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # INFORMACIÓN PERSONAL
        tk.Label(
            inner_frame,
            text=t("personal_information"),
            font=("Arial", 14, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 20))

        # Nombre
        tk.Label(
            inner_frame,
            text=t("username2"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.nombre_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT
        )
        self.nombre_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.nombre_entry.insert(0, t("username3"))
        self.nombre_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese su nombre"))
        self.nombre_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese su nombre"))

        # Apellidos
        tk.Label(
            inner_frame,
            text=t("lats_name"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.apellidos_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT
        )
        self.apellidos_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.apellidos_entry.insert(0, t("insert_sumernames"))
        self.apellidos_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, t("insert_sumernames")))
        self.apellidos_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, t("insert_sumernames")))

        tk.Label(
            form_frame,
            text=t("question_security"),
            font=("Arial", 10),
            fg=self.colors[6],  # Era: self.c6
            bg=self.colors[0]   # Era: self.c1
        ).pack(pady=(10,5), anchor="w", padx=20)

        self.security_question_combobox = ttk.Combobox(
            form_frame,
            values=PasswordRecovery.SECURITY_QUESTIONS,
            state="readonly",
            font=("Arial", 10),
            width=35
        )
        self.security_question_combobox.pack(pady=5, padx=20)
        self.security_question_combobox.current(0)

        tk.Label(
            form_frame,
            text=t("answer_security"),
            font=("Arial", 10),
            fg=self.colors[6],    # Era: self.c6
            bg=self.colors[0]   # Era: self.c1
        ).pack(pady=(10, 5), anchor="w", padx=20)
    
    # Entry para respuesta
        self.security_answer_entry = tk.Entry(
            form_frame,
            font=("Arial", 10),
            bg=self.colors[2],    # Era: self.c2
            fg=self.colors[6],    # Era: self.c6
            insertbackground=self.colors[6],  # Era: self.c6
            relief=tk.FLAT,
            width=30
        )
        self.security_answer_entry.pack(pady=5, padx=20, ipady=5)
        

        # Foto de perfil
        tk.Label(
            inner_frame,
            text=t("photo_perfil"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 10))
        
        self.photo_btn = tk.Button(
            inner_frame,
            text=t("add_photo"),
            font=("Arial", 10),
            bg=self.colors[5],
            fg=self.colors[2],
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
            text=t("date_birthday"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        combo_container = tk.Frame(inner_frame, bg=self.colors[5], relief=tk.FLAT)
        combo_container.pack(fill=tk.X, pady=(0,15), ipady=5, ipadx=5)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                        fieldbackground=self.colors[5],
                        background=self.colors[5],
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
            text=t("nationality"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
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
                        fieldbackground=self.colors[5],
                        background=self.colors[5],
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
        self.nacionalidad_combobox.set(t("selec_nationality"))

        # CUENTA Y SEGURIDAD
        tk.Label(
            inner_frame,
            text=t("account_security"),
            font=("Arial", 14, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(10, 20))
        
        # Usuario
        tk.Label(
            inner_frame,
            text=t("username"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.usuario_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT
        )
        self.usuario_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.usuario_entry.insert(0, t("insert_username"))
        self.usuario_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, t("insert_username")))
        self.usuario_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, t("insert_username")))
        self.usuario_entry.bind('<KeyRelease>', self.validar_usuario_tiempo_real)

        # Frame para mostrar requisitos de usuario
        requirements_user_frame = tk.Frame(inner_frame, bg=self.c1)
        requirements_user_frame.pack(fill=tk.X, pady=(5, 15))

        # Lista de requisitos con sus checks
        self.req_user_length = tk.Label(
            requirements_user_frame,
            text=t("restriccion1"),
            font=("Arial", 9),
            bg=self.c1,
            fg=self.c7,
            anchor="w"
        )
        self.req_user_length.pack(anchor="w", pady=2)

        self.req_user_alphanumeric = tk.Label(
            requirements_user_frame,
            text=t("restriccion2"),
            font=("Arial", 9),
            bg=self.c1,
            fg=self.c7,
            anchor="w"
        )
        self.req_user_alphanumeric.pack(anchor="w", pady=2)

        # Correo electrónico
        tk.Label(
            inner_frame,
            text=t("email"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))

        self.correo_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT
        )
        self.correo_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.correo_entry.insert(0, t("insert_email"))
        self.correo_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, t("insert_email")))
        self.correo_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, t("insert_email")))

        # Contraseña
        tk.Label(
            inner_frame,
            text=t("password"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        pass_frame1 = tk.Frame(inner_frame, bg=self.colors[5])
        pass_frame1.pack(fill=tk.X, pady=(0, 15))
        
        # Frame para mostrar requisitos de contraseña
        requirements_frame = tk.Frame(inner_frame, bg=self.colors[0])
        requirements_frame.pack(fill=tk.X, pady=(5, 15))

        # Lista de requisitos con sus checks
        self.req_length = tk.Label(
            requirements_frame,
            text=t("restriccion3"),
            font=("Arial", 9),
            bg=self.c1,
            fg=self.c7,  # Color gris
            anchor="w"
        )
        self.req_length.pack(anchor="w", pady=2)

        self.req_alphanumeric = tk.Label(
            requirements_frame,
            text=t("restriccion4"),
            font=("Arial", 9),
            bg=self.c1,
            fg=self.c7,
            anchor="w"
        )
        self.req_alphanumeric.pack(anchor="w", pady=2)

        self.new_pass_entry = tk.Entry(
            pass_frame1,
            font=("Arial", 11),
            show="",
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            borderwidth=0
        )
        
        self.req_no_spaces = tk.Label(
            requirements_frame,
            text=t("restriccion5"),
            font=("Arial", 9),
            bg=self.c1,
            fg=self.c7,
            anchor="w"
        )
        self.req_no_spaces.pack(anchor="w", pady=2)

        self.new_pass_entry = tk.Entry(
            pass_frame1,
            font=("Arial", 11),
            show="",
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            borderwidth=0
        )

        self.new_pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        # Vincular validación en tiempo real
        self.new_pass_entry.bind('<KeyRelease>', self.validar_contrasena_tiempo_real)
        self.new_pass_entry.bind('<FocusIn>', lambda e: self.clear_placeholder_password(e, t("password_placeholder")))
        self.new_pass_entry.bind('<FocusOut>', lambda e: self.restore_placeholder_password(e, t("password_placeholder")))
        self.new_pass_entry.insert(0, t("password_placeholder"))

        show_pass1_btn = tk.Button(
            pass_frame1,
            text="👁",
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.toggle_password_field(self.new_pass_entry, show_pass1_btn)
        )
        show_pass1_btn.pack(side=tk.RIGHT, padx=5)
        
        # Confirmar contraseña
        tk.Label(
            inner_frame,
            text=t("confirm_password"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        pass_frame2 = tk.Frame(inner_frame, bg=self.colors[5])
        pass_frame2.pack(fill=tk.X, pady=(0, 25))
        
        self.confirm_pass_entry = tk.Entry(
            pass_frame2,
            font=("Arial", 11),
            show="",
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            borderwidth=0
        )
        self.confirm_pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.confirm_pass_entry.insert(0, t("password_placeholder"))

        self.confirm_pass_entry.bind('<FocusIn>', lambda e: self.clear_placeholder_password(e, t("password_placeholder")))
        self.confirm_pass_entry.bind('<FocusOut>', lambda e: self.restore_placeholder_password(e, t("password_placeholder")))

        show_pass2_btn = tk.Button(
            pass_frame2,
            text="👁",
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            borderwidth=0,
            cursor="hand2",
            command=lambda: self.toggle_password_field(self.confirm_pass_entry, show_pass2_btn)
        )
        show_pass2_btn.pack(side=tk.RIGHT, padx=5)

        # RECONOCIMIENTO FACIAL (Opcional)
        tk.Label(
            inner_frame,
            text=t("facial_identification"),
            font=("Arial", 14, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(10, 15))
        
        self.usar_facial_var = tk.BooleanVar()
        facial_check = tk.Checkbutton(
            inner_frame,
            text=t("enable_facial"),
            variable=self.usar_facial_var,
            font=("Arial", 10),
            bg=self.colors[0],
            fg=self.colors[5],
            activebackground=self.colors[0],
            selectcolor=self.colors[0],
            activeforeground=self.colors[5]
        )
        facial_check.pack(anchor="w", pady=(0, 10))
        
        self.facial_button = tk.Button(
            inner_frame,
            text=t("capture_face"),
            font=("Arial", 11, "bold"),
            bg=self.colors[3],
            fg=self.colors[5],
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
            text=t("pay_information"),
            font=("Arial", 14, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(10, 15))
        
        self.guardar_tarjeta_var = tk.BooleanVar()
        tarjeta_check = tk.Checkbutton(
            inner_frame,
            text=t("enable_facial"),
            variable=self.guardar_tarjeta_var,
            font=("Arial", 10),
            bg=self.colors[0],
            fg=self.colors[5],
            activebackground=self.colors[0],
            selectcolor=self.colors[0],
            activeforeground=self.colors[5]
        )
        tarjeta_check.pack(anchor="w", pady=(0, 15))
        
        # Número de tarjeta
        tk.Label(
            inner_frame,
            text=t("card_number"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.num_tarjeta_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.num_tarjeta_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        self.num_tarjeta_entry.insert(0, t("card_number"))
        
        # Frame para fecha y CVV
        expiry_cvv_frame = tk.Frame(inner_frame, bg=self.colors[0])
        expiry_cvv_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Fecha de expiración
        expiry_left = tk.Frame(expiry_cvv_frame, bg=self.colors[0])
        expiry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(
            expiry_left,
            text=t("expiry_date"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.expiry_entry = tk.Entry(
            expiry_left,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.expiry_entry.pack(fill=tk.X, ipady=5)
        
        # CVV
        cvv_right = tk.Frame(expiry_cvv_frame, bg=self.colors[0])
        cvv_right.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            cvv_right,
            text="CVV",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.cvv_entry = tk.Entry(
            cvv_right,
            font=("Arial", 11),
            show="*",
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.cvv_entry.pack(fill=tk.X, ipady=5)
        
        # Nombre del titular
        tk.Label(
            inner_frame,
            text=t("name_holder"),
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(anchor="w", pady=(0, 5))
        
        self.titular_entry = tk.Entry(
            inner_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
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
            text=t("register_button"),
            font=("Arial", 12, "bold"),
            bg=self.colors[3],
            fg=self.colors[5],
            width=20,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors[4],
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

    def add_language_selector(self, parent):
        self.flags = {
            "es": ImageTk.PhotoImage(Image.open("./images/bandera_españa.png").resize((60, 31))),
            "en": ImageTk.PhotoImage(Image.open("./images/bandera_ru.png").resize((60, 31))),
            "hu": ImageTk.PhotoImage(Image.open("./images/bandera_hungria.png").resize((60, 31))),
        }
        self.current_flag = "es"
        self.flag_btn = tk.Button(
            parent,
            image=self.flags[self.current_flag],
            relief=tk.FLAT,
            bg=self.bg_black,
            command=self.show_language_menu,
            cursor="hand2"
        )
        self.flag_btn.pack(side=tk.LEFT, padx=10, pady=10)

    def show_language_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(
            label="Español", image=self.flags["es"], compound="left",
            command=lambda: self.change_language("es")
        )
        menu.add_command(
            label="English", image=self.flags["en"], compound="left",
            command=lambda: self.change_language("en")
        )
        menu.add_command(
            label="Magyar", image=self.flags["hu"], compound="left",
            command=lambda: self.change_language("hu")
        )
        x = self.flag_btn.winfo_rootx()
        y = self.flag_btn.winfo_rooty() + self.flag_btn.winfo_height()
        menu.tk_popup(x, y)

    def change_language(self, lang_code):
        set_language(lang_code)
        self.current_flag = lang_code
        self.flag_btn.config(image=self.flags[lang_code])
        self.refresh_texts()

    def refresh_texts(self):
        # Actualiza los textos de los labels y botones principales del login
        self.title_label.config(text=t("login_title"))
        self.username_label.config(text=t("username"))
        self.password_label.config(text=t("password"))
        self.forgot_pass_btn.config(text=t("forgot_password"))
        self.login_btn.config(text=t("login_button"))
        self.register_btn.config(text=t("register_button"))
        self.google_btn.config(text=t("google_login"))
        self.help_btn.config(text=t("help_button"))
        self.credits_btn.config(text=t("credits_button"))

        # Actualiza el placeholder del usuario si está vacío o es el placeholder anterior
        if self.username_entry.get() == "" or self.username_entry.get() in [
            t("username_placeholder"),
            "Ingrese su usuario, correo o teléfono",
            "Enter your username, email or phone",
            "Adja meg felhasználónevét, e-mailjét vagy telefonszámát"
        ]:
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, t("username_placeholder"))
            self.username_entry.config(fg=self.colors[1])

        # Actualiza el placeholder de la contraseña si está vacío o es el placeholder anterior
        if self.password_entry.get() == "" or self.password_entry.get() in [
            t("password_placeholder"),
            "Ingrese su contraseña",
            "Enter your password",
            "Adja meg jelszavát"
        ]:
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, t("password_placeholder"))
            self.password_entry.config(fg=self.colors[1])
            self.password_entry.config(show="")  # Asegura que el placeholder no oculte el texto

    def show_login_window(self):
        """Muestra la ventana de login y oculta la de registro"""
        # IMPORTANTE: Recrear la interfaz de login con los colores actualizados
        if hasattr(self, 'login_frame') and self.login_frame:
            self.login_frame.destroy()
        
        # Recrear la interfaz de login con los nuevos colores
        self.create_login_widgets()
        
        if hasattr(self, 'register_frame') and self.register_frame:
            try:
                self.register_frame.pack_forget()
            except:
                pass
        
        self.login_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_register_window(self):
        """Muestra la ventana de registro y oculta la de login"""
        # IMPORTANTE: Recrear la interfaz de registro con los colores actualizados
        if hasattr(self, 'register_frame') and self.register_frame:
            self.register_frame.destroy()
        
        # Recrear la interfaz de registro con los nuevos colores
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
            messagebox.showerror(t("error_register_facial").format(error=e))
        self.root.attributes('-disabled', False)



    def register_user(self):
        """Obtiene y guarda todos los datos del usuario al registrarse"""
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        nacionalidad = self.nacionalidad_combobox.get()
        correo = self.correo_entry.get()
        username = self.usuario_entry.get()

        if not self.validar_usuario_final(username):
            return  # No continuar si el usuario no es válid
    
        password = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if not self.validar_contrasena_final(password):
            messagebox.showerror(t("error_restr_password"))
        
        # Verificar que las contraseñas coincidan
        if password != confirm_pass:
            messagebox.showerror(t("paswords_notmatch"))
            return
    
        security_question = self.security_question_combobox.get()
        security_answer = self.security_answer_entry.get()


        # Validar que no sean placeholders
        if nombre == t("username3") or not nombre:
            messagebox.showerror(t("error_name"))
            return
        
        if apellidos == t("insert_sumernames") or not apellidos:
            messagebox.showerror(t("error_sumername"))
            return
        
        if not security_answer.strip():
            messagebox.showerror(t("error_questionsecury"))
            return
        
            
        if nacionalidad == t("enter_nationality") or not nacionalidad:
            messagebox.showerror(t("error_nationality"))
            return
        
        if correo == t("insert_email") or not correo:
            messagebox.showerror(t("error_email"))
            return
        
        if "@" not in correo or "." not in correo:
            messagebox.showerror(t("error_email2"))
            return
        
        if username == t("insert_username") or not username:
            messagebox.showerror(t("user_error"))
            return
        
        if password == t("password_placeholder") or not password:
            messagebox.showerror(t("error_password3"))
            return
        
        if password != confirm_pass:
            messagebox.showerror(t("paswords_notmatch"))
            return
        
        users_aes = encrip_aes.load_users_aes()
        if username in users_aes:
            messagebox.showerror(t("user_exist"))
            return
        
        try:
            encrip_aes.register_user_aes(username, password, nombre, correo, nacionalidad, apellidos)
            self.load_users()

            success, message = self.password_recovery.add_security_question(
                username,
                security_question,
                security_answer
            )
            if not success:
                messagebox.showerror(t("error_guardar_pregunta"))
                return
            
            
            if self.guardar_tarjeta_var.get():
                numero = self.num_tarjeta_entry.get().strip()
                expiry = self.expiry_entry.get().strip()
                cvv = self.cvv_entry.get().strip()
                titular = self.titular_entry.get().strip()
                
                if numero and numero != t("card_number") and expiry and cvv and titular:
                    encrip_aes.register_user_card(username, cvv, numero, expiry, titular)
                    self.load_cards()
            
            messagebox.showinfo(t("register_succselfol"))
            self.show_login_window()
            
        except Exception as e:
            messagebox.showerror("error_register_usuario")

    def reiniciar_login(self, c1, c2, c3, c4, c5, c6, c7):
        """Recrea la interfaz de login"""
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5
        self.c6 = c6
        self.c7 = c7
        self.colors = [c1, c2, c3, c4, c5, c6, c7]

        # Limpiar la ventana completamente
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Actualizar fondo de la ventana principal con self.colors[0]
        self.root.configure(bg=c1)

        self.create_login_widgets()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    #Estas funciones verifican que el usuario o la contrasena sean validos

    def validar_contrasena_tiempo_real(self, event=None):
        """Valida la contraseña en tiempo real y actualiza los checks visuales"""
        password = self.new_pass_entry.get()
        
        # Si es el placeholder, no validar
        if password == t("password_placeholder") or password == "":
            self.req_length.config(text="❌" + t("restriccion3"), fg=self.c7)  # ← Cambiar
            self.req_alphanumeric.config(text="❌" + t("restriccion4"), fg=self.c7)  # ← Cambiar
            self.req_no_spaces.config(text="❌" + t("restriccion5"), fg=self.c7)  # ← Cambiar
            return
        
        # Validar longitud (8-23 caracteres)
        if 8 <= len(password) <= 23:
            self.req_length.config(text="✅" + t("restriccion3"), fg="#00CC00")
        else:
            self.req_length.config(text="❌" + t("restriccion3"), fg=self.c4)

        # Validar solo alfanumérico (letras y números, sin caracteres especiales)
        if password.isalnum():
            self.req_alphanumeric.config(text="✅" + t("restriccion4"), fg="#00CC00")
            self.req_no_spaces.config(text="✅" + t("restriccion5"), fg="#00CC00")
        else:
            self.req_alphanumeric.config(text="❌" + t("restriccion4"), fg=self.c4)
            if ' ' in password:
                self.req_no_spaces.config(text="❌" + t("restriccion5"), fg=self.c4)
            else:
                self.req_no_spaces.config(text="❌" + t("restriccion5"), fg=self.c4)

    def validar_contrasena_final(self, password):
        """Valida la contraseña antes de registrar y muestra mensajes de error"""
        
        # Verificar longitud
        if len(password) < 8 or len(password) > 23:
            messagebox.showerror(
                t("pasword_invalid"),
                t("condicion_pasword")
            )
            return False
        
        # Verificar solo alfanumérico (sin caracteres especiales ni espacios)
        if not password.isalnum():
            messagebox.showerror(
                t("pasword_invalid"),
                t("condicion_pasword2")
            )
            return False
        
        return True
    
    def validar_usuario_tiempo_real(self, event=None):
        """Valida el usuario en tiempo real y actualiza los checks visuales"""
        username = self.usuario_entry.get()
        
        # Si es el placeholder o está vacío, resetear
        if username == t("insert_username") or username == "":
            self.req_user_length.config(text="❌"+ t("restriccion1") , fg=self.c7)
            self.req_user_alphanumeric.config(text="❌"+ t("restriccion2"), fg=self.c7)
            return
        
        # Validar longitud (4-256 caracteres)
        if 4 <= len(username) <= 256:
            self.req_user_length.config(text="✅ Entre 4 y 256 caracteres", fg="#00CC00")
        else:
            self.req_user_length.config(text="❌ Entre 4 y 256 caracteres", fg=self.c4)
        
        # Validar solo alfanumérico (letras y números, sin caracteres especiales ni espacios)
        if username.isalnum():
            self.req_user_alphanumeric.config(text="✅" + t("restriccion2"), fg="#00CC00")
        else:
            self.req_user_alphanumeric.config(text="❌" + t("restriccion2"), fg=self.c4)


    def validar_usuario_final(self, username):
        """Valida el usuario antes de registrar y muestra mensajes de error"""
        
        # Verificar longitud
        if len(username) < 4 or len(username) > 256:
            messagebox.showerror(
                t("user_invalid"),
                t("condicion_user1")
            )
            return False
        
        # Verificar solo alfanumérico (sin caracteres especiales ni espacios)
        if not username.isalnum():
            messagebox.showerror(
                t("user_invalid"),
                t("condicion_user2")
            )
            return False
        
        # Verificar que no exista
        if username in self.users:
            messagebox.showerror(
                t("user_ind"),
                t("user_ocupado")
            )
            return False
        
        return True