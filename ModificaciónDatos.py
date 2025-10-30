import tkinter as tk
from tkinter import ttk, messagebox
import encrip_aes
from Traducciones import t

class ModificarDatosUsuario:
    def __init__(self, root, username, username_enc, callback_volver, c1, c2, c3, c4, c5, c6, c7):
        self.root = root
        self.username = username
        self.username_enc = username_enc
        self.callback_volver = callback_volver
        
        # Colores del tema
        self.colors = [c1, c2, c3, c4, c5, c6, c7]
        self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7 = c1, c2, c3, c4, c5, c6, c7
        
        # Variables para validación
        self.master_key = encrip_aes.master_key
        
        # Cargar datos actuales del usuario
        self.cargar_datos_usuario()
        
        # Crear interfaz
        self.create_widgets()
    
    def cargar_datos_usuario(self):
        """Carga los datos actuales del usuario desde el archivo encriptado"""
        try:
            users_enc = encrip_aes.load_users_aes()
            print(f"Intentando cargar datos para username_enc: {self.username_enc}")
            
            # Primero intentar con el username_enc proporcionado
            user_data = users_enc.get(self.username_enc, None)
            
            # Si no se encuentra, buscar por username desencriptado
            if user_data is None:
                print(f"No encontrado con username_enc, buscando por username: {self.username}")
                for enc_username, data in users_enc.items():
                    try:
                        dec_username = encrip_aes.decrypt_data(enc_username, self.master_key)
                        if dec_username == self.username:
                            print(f"Usuario encontrado con nuevo username_enc: {enc_username}")
                            self.username_enc = enc_username  # Actualizar la referencia
                            user_data = data
                            break
                    except Exception as e:
                        print(f"Error desencriptando username {enc_username}: {e}")
                        continue
            
            # Si aún no se encuentra, crear datos vacíos
            if user_data is None:
                print(f"Usuario no encontrado, creando datos vacíos")
                self.datos_actuales = {
                    'username': self.username,
                    'nombre': '',
                    'apellidos': '',
                    'email': '',
                    'nacionalidad': '',
                    'telefono': ''
                }
                return
            
            # Desencriptar datos con validación
            self.datos_actuales = {
                'username': self.username,  # Username ya desencriptado
                'nombre': self.safe_decrypt(user_data.get('nombre_enc', ''), 'nombre'),
                'apellidos': self.safe_decrypt(user_data.get('apellidos_enc', ''), 'apellidos'),
                'email': self.safe_decrypt(user_data.get('email_enc', ''), 'email'),
                'nacionalidad': self.safe_decrypt(user_data.get('nacionalidad_enc', ''), 'nacionalidad'),
                'telefono': self.safe_decrypt(user_data.get('telefono_enc', ''), 'telefono') if 'telefono_enc' in user_data else ''
            }
            
            print(f"Datos cargados exitosamente para: {self.username}")
                
        except Exception as e:
            print(f"Error al cargar datos del usuario: {e}")
            self.datos_actuales = {
                'username': self.username,
                'nombre': '',
                'apellidos': '',
                'email': '',
                'nacionalidad': '',
                'telefono': ''
            }

    def safe_decrypt(self, encrypted_data, field_name):
        """Desencripta datos de forma segura con manejo de errores"""
        try:
            if not encrypted_data:
                return ''
            return encrip_aes.decrypt_data(encrypted_data, self.master_key)
        except Exception as e:
            print(f"Error desencriptando campo '{field_name}': {e}")
            return ''

    def create_widgets(self):
        """Crea la interfaz de modificación de datos"""
        self.modify_frame = tk.Frame(self.root, bg=self.colors[0])
        
        # CONFIGURAR VENTANA PRINCIPAL PRIMERO
        self.root.geometry("600x700")  # Ventana más compacta
        self.root.resizable(False, False)
        self.root.minsize(600, 700)
        self.root.maxsize(600, 700)
        
        # Contenedor principal SIN scroll - más simple
        main_container = tk.Frame(self.modify_frame, bg=self.colors[0])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Barra superior
        top_bar = tk.Frame(main_container, bg=self.colors[3], height=40)
        top_bar.pack(fill=tk.X, pady=(0, 20))
        
        # Botón volver
        back_btn = tk.Button(
            top_bar,
            text="← Volver",
            font=("Arial", 10),
            bg=self.colors[3],
            fg=self.colors[5],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.volver
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Título centrado
        title_label = tk.Label(
            main_container,
            text="Modificar Datos de Usuario",
            font=("Arial", 20, "bold"),
            bg=self.colors[0],
            fg=self.colors[4]
        )
        title_label.pack(pady=(0, 30))
        
        # CONTENEDOR CENTRADO PARA FORMULARIO
        form_container = tk.Frame(main_container, bg=self.colors[0])
        form_container.pack(expand=True)
        
        # INFORMACIÓN PERSONAL
        personal_section = tk.Frame(form_container, bg=self.colors[0])
        personal_section.pack(pady=(0, 20))
        
        tk.Label(
            personal_section,
            text="Información Personal",
            font=("Arial", 14, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack(pady=(0, 15))
        
        # Username (nueva fila)
        username_frame = tk.Frame(personal_section, bg=self.colors[0])
        username_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(
            username_frame,
            text="Nombre de usuario",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack()
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            justify='center'
        )
        self.username_entry.pack(fill=tk.X, ipady=5, pady=5)
        self.username_entry.insert(0, self.datos_actuales.get('username', ''))
        
        # Fila 1: Nombre y Apellidos
        row1 = tk.Frame(personal_section, bg=self.colors[0])
        row1.pack(pady=10, fill=tk.X)
        
        # Nombre (izquierda)
        name_frame = tk.Frame(row1, bg=self.colors[0])
        name_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        tk.Label(
            name_frame,
            text="Nombre",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack()
        
        self.nombre_entry = tk.Entry(
            name_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            justify='center'
        )
        self.nombre_entry.pack(fill=tk.X, ipady=5, pady=5)
        self.nombre_entry.insert(0, self.datos_actuales.get('nombre', ''))
        
        # Apellidos (derecha)
        lastname_frame = tk.Frame(row1, bg=self.colors[0])
        lastname_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0))
        
        tk.Label(
            lastname_frame,
            text="Apellidos",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack()
        
        self.apellidos_entry = tk.Entry(
            lastname_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            justify='center'
        )
        self.apellidos_entry.pack(fill=tk.X, ipady=5, pady=5)
        self.apellidos_entry.insert(0, self.datos_actuales.get('apellidos', ''))
        
        # Fila 2: Email y Teléfono
        row2 = tk.Frame(personal_section, bg=self.colors[0])
        row2.pack(pady=15, fill=tk.X)
        
        # Email (izquierda)
        email_frame = tk.Frame(row2, bg=self.colors[0])
        email_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        tk.Label(
            email_frame,
            text="Email",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack()
        
        self.correo_entry = tk.Entry(
            email_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            justify='center'
        )
        self.correo_entry.pack(fill=tk.X, ipady=5, pady=5)
        self.correo_entry.insert(0, self.datos_actuales.get('email', ''))
        
        # Teléfono (derecha)
        phone_frame = tk.Frame(row2, bg=self.colors[0])
        phone_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0))
        
        tk.Label(
            phone_frame,
            text="Teléfono",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack()
        
        self.telefono_entry = tk.Entry(
            phone_frame,
            font=("Arial", 11),
            bg=self.colors[5],
            fg=self.colors[0],
            relief=tk.FLAT,
            justify='center'
        )
        self.telefono_entry.pack(fill=tk.X, ipady=5, pady=5)
        self.telefono_entry.insert(0, self.datos_actuales.get('telefono', ''))
        
        # Nacionalidad (fila completa)
        nationality_frame = tk.Frame(personal_section, bg=self.colors[0])
        nationality_frame.pack(pady=15, fill=tk.X)
        
        tk.Label(
            nationality_frame,
            text="Nacionalidad",
            font=("Arial", 10, "bold"),
            bg=self.colors[0],
            fg=self.colors[5]
        ).pack()
        
        nacionalidades = [
            "Alemana", "Argentina", "Australiana", "Boliviana", "Brasileña",
            "Canadiense", "Chilena", "China", "Colombiana", "Costarricense",
            "Cubana", "Dominicana", "Ecuatoriana", "Española", "Estadounidense",
            "Filipina", "Finlandesa", "Francesa", "Galésa", "Gualtemalteca",
            "Húngara", "Irlandésa", "Inglesa", "Japonesa", "Mexicana",
            "Nicaragüense", "Panameña", "Paraguaya", "Peruana", "Puertorriqueña",
            "Salvadoreña", "Uruguaya", "Venezolana"
        ]
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
                        fieldbackground=self.colors[5],
                        background=self.colors[5],
                        foreground="#000000",
                        arrowcolor="#000000",
                        borderwithd=0,
                        relief=tk.FLAT)
        
        self.nacionalidad_combobox = ttk.Combobox(
            nationality_frame,
            values=nacionalidades,
            font=("Arial", 11),
            state="readonly",
            style="Custom.TCombobox",
            justify='center'
        )
        self.nacionalidad_combobox.pack(fill=tk.X, ipady=5, pady=5)
        
        # Establecer nacionalidad actual
        nacionalidad_actual = self.datos_actuales.get('nacionalidad', '')
        if nacionalidad_actual in nacionalidades:
            self.nacionalidad_combobox.set(nacionalidad_actual)
        else:
            self.nacionalidad_combobox.set("Selecciona tu nacionalidad")
        
        # BOTÓN GUARDAR CAMBIOS - JUSTO DEBAJO DE NACIONALIDAD
        guardar_frame = tk.Frame(personal_section, bg=self.colors[0])
        guardar_frame.pack(pady=(15, 0))
        
        self.btn_guardar = tk.Button(
            guardar_frame,
            text="💾 GUARDAR CAMBIOS",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",  # Verde para guardar
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.guardar_cambios
        )
        self.btn_guardar.pack(pady=10)
        
        # Mostrar frame
        self.modify_frame.pack(fill=tk.BOTH, expand=True)

    def validar_datos(self):
        """Valida todos los datos antes de guardar"""
        username = self.username_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        apellidos = self.apellidos_entry.get().strip()
        correo = self.correo_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        nacionalidad = self.nacionalidad_combobox.get()
        
        # Validaciones básicas
        if not username:
            messagebox.showerror("Error", "Error, por favor ingresa tu nombre de usuario")
            return False
        
        if not nombre:
            messagebox.showerror("Error", "Error, por favor ingresa tu nombre")
            return False
        
        if not apellidos:
            messagebox.showerror("Error", "Error, por favor ingresa tus apellidos")
            return False
        
        if not correo:
            messagebox.showerror("Error", "Error, por favor ingresa tu correo electrónico")
            return False
        
        if not telefono:
            messagebox.showerror("Error", "Error, por favor ingresa tu teléfono")
            return False
        
        if nacionalidad == "Selecciona tu nacionalidad" or not nacionalidad:
            messagebox.showerror("Error", "Error, por favor ingresa tu nacionalidad")
            return False
        
        # Validar formato de correo
        if "@" not in correo or "." not in correo:
            messagebox.showerror("Error", "Correo electrónico no válido.")
            return False
        
        # Validar dominio permitido
        correo = correo.lower()
        dominios_permitidos = ["@gmail.com", "@hotmail.com", "@outlook.com", "@outlook.es"]
        if not any(correo.endswith(dominio) for dominio in dominios_permitidos):
            messagebox.showerror(
                "Error",
                "Solo se permiten correos de Gmail, Hotmail u Outlook."
            )
            return False
        
        # Validar formato de teléfono
        telefono_limpio = telefono.replace("-", "").replace(" ", "")
        if not telefono_limpio.isdigit() or len(telefono_limpio) != 8:
            messagebox.showerror("Error", "Error, el telefono no es valido")
            return False
        
        # Validar username
        if len(username) < 4 or len(username) > 256:
            messagebox.showerror("Error", "El nombre de usuario debe tener entre 4 y 256 caracteres")
            return False
        
        if not username.isalnum():
            messagebox.showerror("Error", "El nombre de usuario solo puede contener letras y números")
            return False
        
        # Verificar que el username no esté en uso por otro usuario (solo si cambió)
        if username != self.datos_actuales.get('username', ''):
            users_enc = encrip_aes.load_users_aes()
            for enc_username, user_data in users_enc.items():
                if enc_username != self.username_enc:  # No comparar con el usuario actual
                    try:
                        existing_username = encrip_aes.decrypt_data(enc_username, self.master_key)
                        if username.lower() == existing_username.lower():
                            messagebox.showerror("Error", "Este nombre de usuario ya está en uso")
                            return False
                    except Exception:
                        continue
        
        return True

    def guardar_cambios(self):
        """Guarda todos los cambios realizados"""
        if not self.validar_datos():
            return
        
        try:
            # Obtener datos actualizados
            new_username = self.username_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            apellidos = self.apellidos_entry.get().strip()
            correo = self.correo_entry.get().strip().lower()
            telefono = self.telefono_entry.get().strip()
            nacionalidad = self.nacionalidad_combobox.get()
            
            # Cargar datos actuales
            users_enc = encrip_aes.load_users_aes()
            user_data = users_enc[self.username_enc]
            
            # Variables para seguimiento de cambios
            username_cambio = False
            old_username_enc = None
            
            # Si el username cambió, necesitamos crear una nueva entrada y borrar la antigua
            if new_username != self.datos_actuales.get('username', ''):
                # GUARDAR LA REFERENCIA ANTERIOR ANTES DE CAMBIARLA
                old_username_enc = self.username_enc
                
                # Encriptar nuevo username
                new_username_enc = encrip_aes.encrypt_data(new_username, self.master_key)
                
                # Copiar todos los datos del usuario con el nuevo username encriptado
                users_enc[new_username_enc] = user_data.copy()
                
                # Borrar la entrada anterior
                del users_enc[self.username_enc]
                
                # Actualizar referencia
                old_username = self.username
                self.username_enc = new_username_enc
                self.username = new_username
                user_data = users_enc[new_username_enc]
                username_cambio = True
                
                print(f"Username cambiado de {old_username} a {new_username}")
            
            # Actualizar datos encriptados
            user_data['nombre_enc'] = encrip_aes.encrypt_data(nombre, self.master_key)
            user_data['apellidos_enc'] = encrip_aes.encrypt_data(apellidos, self.master_key)
            user_data['email_enc'] = encrip_aes.encrypt_data(correo, self.master_key)
            user_data['telefono_enc'] = encrip_aes.encrypt_data(telefono, self.master_key)
            user_data['nacionalidad_enc'] = encrip_aes.encrypt_data(nacionalidad, self.master_key)
            
            # Guardar cambios
            users_enc[self.username_enc] = user_data
            encrip_aes.save_users_aes(users_enc)
            
            # ACTUALIZAR TAMBIÉN LOS PUNTAJES Y ARCHIVOS SI CAMBIÓ EL USERNAME
            if username_cambio:
                self.actualizar_puntajes_username(old_username_enc)
                self.actualizar_archivos_usuario(old_username_enc, self.username_enc)
            
            messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            self.volver()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")
    
    def actualizar_puntajes_username(self, old_username_enc):
        """Actualiza los puntajes cuando cambia el username_enc"""
        try:
            import gestion_puntajes
            
            # Cargar puntajes actuales
            puntajes = gestion_puntajes.load_puntajes()
            
            # Si el usuario anterior tenía puntajes, transferirlos al nuevo
            if old_username_enc and old_username_enc in puntajes:
                # Transferir puntajes al nuevo username_enc
                puntajes[self.username_enc] = puntajes[old_username_enc]
                # Borrar puntajes del username anterior
                del puntajes[old_username_enc]
                # Guardar cambios
                gestion_puntajes.save_puntajes(puntajes)
                print(f"Puntajes transferidos de {old_username_enc} a {self.username_enc}")
            else:
                print("No se encontraron puntajes para transferir")
                
        except Exception as e:
            print(f"Error al actualizar puntajes: {e}")
    
    def actualizar_archivos_usuario(self, old_username_enc, new_username_enc):
        """Actualiza los archivos de cara y foto de perfil cuando cambia el username"""
        try:
            import os
            import shutil
            
            # Convertir usernames encriptados a nombres de archivo seguros
            old_safe_username = old_username_enc.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            new_safe_username = new_username_enc.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            
            # 1. Actualizar archivo de datos faciales (.npy)
            users_lbph_dir = os.path.join(os.path.dirname(__file__), "users_lbph")
            old_face_file = os.path.join(users_lbph_dir, f"{old_safe_username}.npy")
            new_face_file = os.path.join(users_lbph_dir, f"{new_safe_username}.npy")
            
            if os.path.exists(old_face_file):
                shutil.move(old_face_file, new_face_file)
                print(f"Archivo facial renombrado: {old_safe_username}.npy → {new_safe_username}.npy")
            else:
                print(f"No se encontró archivo facial: {old_face_file}")
            
            # 2. Actualizar foto de perfil (.jpg)
            profile_photos_dir = os.path.join(os.path.dirname(__file__), "profile_photos")
            old_photo_file = os.path.join(profile_photos_dir, f"profile_{old_safe_username}.jpg")
            new_photo_file = os.path.join(profile_photos_dir, f"profile_{new_safe_username}.jpg")
            
            if os.path.exists(old_photo_file):
                shutil.move(old_photo_file, new_photo_file)
                print(f"Foto de perfil renombrada: profile_{old_safe_username}.jpg → profile_{new_safe_username}.jpg")
            else:
                print(f"No se encontró foto de perfil: {old_photo_file}")
                
        except Exception as e:
            print(f"Error al actualizar archivos de usuario: {e}")

    def volver(self):
        """Vuelve a la ventana anterior"""
        self.modify_frame.destroy()
        self.callback_volver()

    def get_updated_data(self):
        """Retorna los datos actualizados del usuario"""
        return {
            'username': self.username,
            'username_enc': self.username_enc
        }

# Función para usar desde otros módulos - SIMPLIFICADA
def mostrar_modificar_datos(root, username, username_enc, callback_volver, c1, c2, c3, c4, c5, c6, c7):
    """Función helper para mostrar la interfaz de modificación de datos"""
    # Limpiar ventana
    for widget in root.winfo_children():
        widget.destroy()
    
    # Crear interfaz de modificación
    modificador = ModificarDatosUsuario(root, username, username_enc, callback_volver, c1, c2, c3, c4, c5, c6, c7)
    
    # Retornar la instancia para poder acceder a los datos actualizados
    return modificador