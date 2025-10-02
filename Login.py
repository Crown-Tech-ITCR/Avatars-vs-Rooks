import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import os
import time
from face_gui import Face_Recognition
from encriptación import Encriptacion

class LoginAvatarsRooks:
    def __init__(self, root):
        self.root = root
        self.face_window = None
        self.root.title("Log in")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F5F5")
        self.center_window()
        self.primary_color = "#6C6C6C"     # Gris medio oscuro 
        self.secondary_color = "#E0E0E0"   # Gris claro
        self.accent_color = "#4A4A4A"      # Gris oscuro
        self.text_color = "#2C2C2C"        # Texto gris oscuro
        self.users = {}
        self.cards = {}
        self.encriptador = Encriptacion()
        self.load_users()
        self.load_cards()
        self.create_login_widgets()
        self.create_register_widgets()
        self.show_login_window()
        

    def load_users(self):
        """Carga todos los datos de usuarios desde users.txt"""
        if os.path.exists("users.txt"):
            try:
                with open("users.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if "|" in line:
                            parts = line.strip().split("|")
                            if len(parts) >= 6:
                                username = self.encriptador.desencriptar(parts[0])
                                self.users[username] = {
                                    'password': self.encriptador.desencriptar(parts[1]),
                                    'nombre': self.encriptador.desencriptar(parts[2]),
                                    'apellidos': self.encriptador.desencriptar(parts[3]),
                                    'nacionalidad': self.encriptador.desencriptar(parts[4]),
                                    'correo': self.encriptador.desencriptar(parts[5])
                                }
            except Exception as e:
                print(f"Error al cargar usuarios: {e}")
                self.users = {}
        print(self.users)

    def save_users(self):
        """Guarda todos los datos de usuarios en users.txt"""
        try:
            with open("users.txt", "w", encoding="utf-8") as f:
                for username, data in self.users.items():
                    username = self.encriptador.encriptar(username)
                    data['password'] = self.encriptador.encriptar(data['password'])
                    data['nombre'] = self.encriptador.encriptar(data['nombre'])
                    data['apellidos'] = self.encriptador.encriptar(data['apellidos'])
                    data['nacionalidad'] = self.encriptador.encriptar(data['nacionalidad'])
                    data['correo'] = self.encriptador.encriptar(data['correo'])
                    f.write(f"{username}|{data['password']}|{data['nombre']}|{data['apellidos']}|{data['nacionalidad']}|{data['correo']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar usuarios: {e}")

    def load_cards(self):
        """Carga datos de tarjetas desde cards.txt"""
        if os.path.exists("cards.txt"):
            try:
                with open("cards.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if "|" in line:
                            parts = line.strip().split("|")
                            if len(parts) >= 5:
                                username = self.encriptador.desencriptar(parts[0])
                                self.cards[username] = {
                                    'numero': self.encriptador.desencriptar(parts[1]),
                                    'expiry': self.encriptador.desencriptar(parts[2]),
                                    'cvv': self.encriptador.desencriptar(parts[3]),
                                    'titular': self.encriptador.desencriptar(parts[4])
                                }
            except Exception as e:
                print(f"Error al cargar tarjetas: {e}")
                self.cards = {} 

    def save_cards(self):
        """Guarda datos de tarjetas en cards.txt"""
        try:
            with open("cards.txt", "w", encoding="utf-8") as f:
                for username, card_data in self.cards.items():
                    username = self.encriptador.encriptar(username)
                    card_data['numero'] = self.encriptador.encriptar(card_data['numero'])
                    card_data['expiry'] = self.encriptador.encriptar(card_data['expiry'])
                    card_data['cvv'] = self.encriptador.encriptar(card_data['cvv'])
                    card_data['titular'] = self.encriptador.encriptar(card_data['titular'])
                    f.write(f"{username}|{card_data['numero']}|{card_data['expiry']}|{card_data['cvv']}|{card_data['titular']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar tarjetas: {e}")


    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (700 // 2)
        self.root.geometry(f'600x700+{x}+{y}')
    
    def create_login_widgets(self):
        """Crea los widgets para el login"""
        self.login_frame = tk.Frame(self.root, bg="#F5F5F5")
        
        logo_label = tk.Label(
            self.login_frame, 
            text="Avatars VS Rooks", 
            font=("Arial", 28, "bold"), 
            fg="#2C2C2C",
            bg="#F5F5F5"
        )
        logo_label.pack(pady=(10, 30))
        
        form_frame = tk.Frame(self.login_frame, bg=self.secondary_color, padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            form_frame, 
            text="Usuario", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            form_frame, 
            text="Contraseña", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            show="•", 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(
            form_frame, 
            text="Iniciar sesión", 
            font=("Arial", 12, "bold"), 
            bg=self.primary_color, 
            fg="white", 
            activebackground=self.accent_color, 
            activeforeground="white", 
            relief=tk.FLAT, 
            command=self.login
        ).pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(
            form_frame, 
            text="Reconocimiento facial", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color, 
            activebackground=self.secondary_color, 
            activeforeground=self.text_color, 
            relief=tk.RAISED, 
            highlightbackground="#B0B0B0", 
            highlightthickness=2, 
            command=self.face_recognition
        ).pack(fill=tk.X)
        
        # Separador
        tk.Frame(self.login_frame, height=1, bg="#B0B0B0").pack(fill=tk.X, pady=10)
        
        tk.Button(
            self.login_frame, 
            text="Crear cuenta nueva", 
            font=("Arial", 12), 
            bg="#4A4A4A", 
            fg="white", 
            activebackground="#2C2C2C", 
            activeforeground="white", 
            relief=tk.FLAT, 
            command=self.show_register_window
        ).pack(fill=tk.X, pady=(5, 15))

    def create_register_widgets(self):
        """Crea los widgets para el registro"""

        self.register_frame = tk.Frame(self.root, bg="#F5F5F5")
        
        # Contenedor principal con scroll
        canvas = tk.Canvas(self.register_frame, bg="#F5F5F5", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.register_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F5F5F5")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        #Titulo Registro
        tk.Label(
            scrollable_frame, 
            text="Registro", 
            font=("Arial", 24, "bold"), 
            fg=self.accent_color, 
            bg="#F5F5F5"
        ).pack(pady=(10, 30))
        
        form_frame = tk.Frame(scrollable_frame, bg=self.secondary_color, padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20), padx=60)

        # INFORMACIÓN PERSONAL
        tk.Label(
            form_frame, 
            text="INFORMACIÓN PERSONAL", 
            font=("Arial", 12, "bold"), 
            bg=self.secondary_color, 
            fg=self.accent_color
        ).pack(anchor="w", pady=(0, 15))

        #Nombre
        tk.Label(
            form_frame, 
            text="Nombre *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.nombre_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.nombre_entry.pack(fill=tk.X, pady=(0, 15))

        #Apellidos
        tk.Label(
            form_frame, 
            text="Apellidos *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.apellidos_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.apellidos_entry.pack(fill=tk.X, pady=(0, 15))
        
        #Fecha de nacimiento
        tk.Label(
            form_frame, 
            text="Fecha de nacimiento *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        # Frame para la fecha
        fecha_frame = tk.Frame(form_frame, bg=self.secondary_color)
        fecha_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Día
        self.dia_entry = tk.Entry(
            fecha_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            width=5
        )
        self.dia_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.dia_entry.insert(0, "DD")
        
        tk.Label(fecha_frame, text="/", font=("Arial", 12), bg=self.secondary_color, fg=self.text_color).pack(side=tk.LEFT)
        
        # Mes
        self.mes_entry = tk.Entry(
            fecha_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            width=5
        )
        self.mes_entry.pack(side=tk.LEFT, padx=5)
        self.mes_entry.insert(0, "MM")
        
        tk.Label(fecha_frame, text="/", font=("Arial", 12), bg=self.secondary_color, fg=self.text_color).pack(side=tk.LEFT)
        
        # Año
        self.año_entry = tk.Entry(
            fecha_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            width=8
        )
        self.año_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.año_entry.insert(0, "AAAA")
        
        #Nacionalidad
        tk.Label(
            form_frame, 
            text="Nacionalidad *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))

        self.nacionalidad_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.nacionalidad_entry.pack(fill=tk.X, pady=(0, 15))


        # CUENTA Y SEGURIDAD
        tk.Label(
            form_frame, 
            text="CUENTA Y SEGURIDAD", 
            font=("Arial", 12, "bold"), 
            bg=self.secondary_color, 
            fg=self.accent_color
        ).pack(anchor="w", pady=(20, 15))
        
        #Usuario
        tk.Label(
            form_frame, 
            text="Nombre de usuario *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.usuario_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.usuario_entry.pack(fill=tk.X, pady=(0, 15))

        #Correo electrónico
        tk.Label(
            form_frame, 
            text="Correo electrónico *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))

        self.correo_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.correo_entry.pack(fill=tk.X, pady=(0, 15))

        #Contraseña
        tk.Label(
            form_frame, 
            text="Contraseña *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.new_pass_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            show="•", 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.new_pass_entry.pack(fill=tk.X, pady=(0, 15))
        
        #Confirmar contraseña
        tk.Label(
            form_frame, 
            text="Confirmar contraseña *", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.confirm_pass_entry = tk.Entry(
            form_frame, 
            font=("Arial", 12), 
            show="•", 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT
        )
        self.confirm_pass_entry.pack(fill=tk.X, pady=(0, 20))

        # RECONOCIMIENTO FACIAL (Opcional)
        tk.Label(
            form_frame, 
            text="RECONOCIMIENTO FACIAL (Opcional)", 
            font=("Arial", 12, "bold"), 
            bg=self.secondary_color, 
            fg=self.accent_color
        ).pack(anchor="w", pady=(10, 15))
        
        self.usar_facial_var = tk.BooleanVar()
        facial_check = tk.Checkbutton(
            form_frame,
            text="Habilitar reconocimiento facial para iniciar sesión",
            variable=self.usar_facial_var,
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            activebackground=self.secondary_color,
            selectcolor="#FFFFFF"
        )
        facial_check.pack(anchor="w", pady=(0, 10))
        
        self.facial_button = tk.Button(
            form_frame,
            text="📷 Capturar rostro",
            font=("Arial", 11),
            bg="#4A90E2",
            fg="white",
            activebackground="#357ABD",
            activeforeground="white",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.facial_button.pack(fill=tk.X, pady=(0, 20))
        
        # Activar/desactivar botón según checkbox
        def toggle_facial_button():
            if self.usar_facial_var.get():
                self.facial_button.config(state=tk.NORMAL)
            else:
                self.facial_button.config(state=tk.DISABLED)
        
        facial_check.config(command=toggle_facial_button)

        # INFORMACIÓN DE PAGO (Opcional)
        tk.Label(
            form_frame, 
            text="INFORMACIÓN DE PAGO (Opcional)", 
            font=("Arial", 12, "bold"), 
            bg=self.secondary_color, 
            fg=self.accent_color
        ).pack(anchor="w", pady=(10, 15))
        
        self.guardar_tarjeta_var = tk.BooleanVar()
        tarjeta_check = tk.Checkbutton(
            form_frame,
            text="Guardar datos de tarjeta para pagos rápidos",
            variable=self.guardar_tarjeta_var,
            font=("Arial", 10),
            bg=self.secondary_color,
            fg=self.text_color,
            activebackground=self.secondary_color,
            selectcolor="#FFFFFF"
        )
        tarjeta_check.pack(anchor="w", pady=(0, 10))
        
        # Frame para datos de tarjeta
        self.tarjeta_frame = tk.Frame(form_frame, bg=self.secondary_color)
        self.tarjeta_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Número de tarjeta
        tk.Label(
            self.tarjeta_frame, 
            text="Número de tarjeta", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.num_tarjeta_entry = tk.Entry(
            self.tarjeta_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.num_tarjeta_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para fecha y CVV
        expiry_cvv_frame = tk.Frame(self.tarjeta_frame, bg=self.secondary_color)
        expiry_cvv_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Fecha de expiración
        expiry_left = tk.Frame(expiry_cvv_frame, bg=self.secondary_color)
        expiry_left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(
            expiry_left, 
            text="Fecha expiración (MM/AA)", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.expiry_entry = tk.Entry(
            expiry_left, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.expiry_entry.pack(fill=tk.X)
        
        # CVV
        cvv_right = tk.Frame(expiry_cvv_frame, bg=self.secondary_color)
        cvv_right.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(
            cvv_right, 
            text="CVV", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.cvv_entry = tk.Entry(
            cvv_right, 
            font=("Arial", 12), 
            show="*",
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.cvv_entry.pack(fill=tk.X)
        
        # Nombre del titular
        tk.Label(
            self.tarjeta_frame, 
            text="Nombre del titular", 
            font=("Arial", 10), 
            bg=self.secondary_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.titular_entry = tk.Entry(
            self.tarjeta_frame, 
            font=("Arial", 12), 
            bg="#FFFFFF", 
            fg="#2C2C2C",
            insertbackground="#2C2C2C",
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.titular_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Función para activar/desactivar campos de tarjeta
        def toggle_tarjeta_fields():
            state = tk.NORMAL if self.guardar_tarjeta_var.get() else tk.DISABLED
            self.num_tarjeta_entry.config(state=state)
            self.expiry_entry.config(state=state)
            self.cvv_entry.config(state=state)
            self.titular_entry.config(state=state)
        
        tarjeta_check.config(command=toggle_tarjeta_fields)
        
        # BOTONES
        tk.Button(
            form_frame, 
            text="Registrarse", 
            font=("Arial", 12, "bold"), 
            bg=self.primary_color, 
            fg="white", 
            activebackground=self.accent_color, 
            activeforeground="white", 
            relief=tk.FLAT, 
            command=self.register_user
        ).pack(fill=tk.X, pady=(20, 15))
        
        tk.Button(
            scrollable_frame, 
            text="Volver al login", 
            font=("Arial", 10), 
            bg="#F5F5F5", 
            fg=self.text_color, 
            activebackground="#F5F5F5", 
            activeforeground=self.text_color, 
            relief=tk.RAISED, 
            highlightbackground="#B0B0B0", 
            highlightthickness=2, 
            command=self.show_login_window
        ).pack(pady=(20, 20))
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Vincular eventos de scroll
        canvas.bind_all("<MouseWheel>", on_mousewheel)  # Windows/Mac
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux
        
    def show_login_window(self):
        """Muestra la ventana de login y oculta la de registro"""
        self.register_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def show_register_window(self):
        """Muestra la ventana de registro y oculta la de login"""
        self.login_frame.pack_forget()
        self.register_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def login(self):
        """Valida credenciales de usuario y abre el menú principal."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña")
            return
        
        if username in self.users and self.users[username]['password'] == password:
            nombre = self.users[username]['nombre']
            messagebox.showinfo("Bienvenido", f"¡Bienvenido {nombre}!")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            
    def register_user(self):
        """Obtiene y guarda todos los datos del usuario al registrarse"""
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        nacionalidad = self.nacionalidad_entry.get()
        correo = self.correo_entry.get()
        username = self.usuario_entry.get()
        password = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        # Validar campos obligatorios
        if not nombre or not apellidos or not nacionalidad or not correo or not username or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos obligatorios (*)")
            return
        
        if "@" not in correo or "." not in correo:
            messagebox.showerror("Error", "Por favor ingresa un correo electrónico válido")
            return
        
        if password != confirm_pass:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if username in self.users:
            messagebox.showerror("Error", "El usuario ya existe")
            return
        
        # Guardar datos de usuario
        self.users[username] = {
            'password': password,
            'nombre': nombre,
            'apellidos': apellidos,
            'nacionalidad': nacionalidad,
            'correo': correo
        }
        self.save_users()
        
        # Guardar tarjeta si se habilitó
        if self.guardar_tarjeta_var.get():
            numero = self.num_tarjeta_entry.get()
            expiry = self.expiry_entry.get()
            cvv = self.cvv_entry.get()
            titular = self.titular_entry.get()
            
            if numero and expiry and cvv and titular:
                self.cards[username] = {
                    'numero': numero,
                    'expiry': expiry,
                    'cvv': cvv,
                    'titular': titular
                }
                self.save_cards()
        
        messagebox.showinfo("Éxito", "¡Registro exitoso!")
        self.show_login_window()
 
    def face_recognition(self):
        """Abre el sistema de reconocimiento facial"""
        try:
            self.root.destroy()
            root = tk.Tk()
            app = Face_Recognition(root)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir reconocimiento facial: {e}")

    def create_new_login(self):
        """Crea una nueva ventana de login después del logout"""
        root = tk.Tk()
        app = LoginAvatarsRooks(root)
        root.mainloop()