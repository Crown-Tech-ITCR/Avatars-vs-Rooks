import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os
import numpy as np
import threading
import pygame
import time as time

class Face_Recognition:
    def __init__(self, root):
        self.USERS_DIR = "users_lbph"
        if not os.path.exists(self.USERS_DIR):
            os.makedirs(self.USERS_DIR)
        self.root = root
        self.login_thread_active = False
        self.setup_gui()

    def setup_gui(self):
        """Configurar la interfaz gráfica con colores claros"""
        primary_color = "#6C6C6C"     # Gris medio oscuro
        secondary_color = "#E0E0E0"   # Gris claro
        accent_color = "#4A4A4A"      # Gris oscuro
        text_color = "#2C2C2C"        # Texto gris oscuro
        bg_color = "#F5F5F5"          # Fondo gris muy claro
        
        self.root.title("Reconocimiento Facial")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        self.root.configure(bg=bg_color)
        
        # Centrar en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 550) // 2
        self.root.geometry(f'500x550+{x}+{y}')
        
        title_label = tk.Label(
            self.root,
            text="Avatars VS Rooks",
            font=("Arial", 28, "bold"),
            fg="#2C2C2C",
            bg=bg_color
        )
        title_label.pack(pady=(30, 10))
        
        subtitle_label = tk.Label(
            self.root,
            text="Login con reconocimiento facial",
            font=("Arial", 14),
            fg=accent_color,
            bg=bg_color
        )
        subtitle_label.pack(pady=(0, 40))
        
        buttons_frame = tk.Frame(self.root, bg=secondary_color, padx=30, pady=30)
        buttons_frame.pack(padx=40, pady=(0, 30))
        
        tk.Button(
            buttons_frame,
            text="Registrar nuevo rostro",
            command=self.register_face_gui,
            font=("Arial", 12, "bold"),
            bg=primary_color,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            width=25,
            height=2,
            cursor="hand2"
        ).pack(pady=(0, 20))
        
        tk.Button(
            buttons_frame,
            text="Iniciar sesión con rostro",
            command=self.login_with_face_gui,
            font=("Arial", 12, "bold"),
            bg=primary_color,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            width=25,
            height=2,
            cursor="hand2"
        ).pack()
        
        info_label = tk.Label(
            self.root,
            text="💡 Asegúrate de tener buena iluminación y mira directamente a la cámara",
            font=("Arial", 10),
            fg=text_color,
            bg=bg_color,
            wraplength=400,
            justify=tk.CENTER
        )
        info_label.pack(pady=(20, 30))
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Limpiar recursos al cerrar la ventana"""
        self.login_thread_active = False
        time.sleep(0.2)
        self.root.destroy()

    def SolicitarNombre(self):
        """Ventana para solicitar nombre de usuario con colores claros"""
        primary_color = "#6C6C6C"     # Gris medio oscuro
        secondary_color = "#E0E0E0"   # Gris claro
        accent_color = "#4A4A4A"      # Gris oscuro
        text_color = "#2C2C2C"        # Texto gris oscuro
        bg_color = "#F5F5F5"          # Fondo gris muy claro
        
        # Variables para el resultado
        self.nombre_resultado = None
        self.nombre_confirmado = False
        
        nombre_window = tk.Toplevel(self.root)
        nombre_window.title("Registro de Usuario")
        nombre_window.geometry("400x250")
        nombre_window.resizable(False, False)
        nombre_window.configure(bg=bg_color)
        nombre_window.transient(self.root)  # Mantener siempre encima de la ventana principal
        nombre_window.grab_set()  # Bloquear interacción con ventana principal
        
        x = (nombre_window.winfo_screenwidth() - 400) // 2
        y = (nombre_window.winfo_screenheight() - 250) // 2
        nombre_window.geometry(f'400x250+{x}+{y}')
        
        title_label = tk.Label(
            nombre_window,
            text="📝 Registro de Usuario",
            font=("Arial", 15, "bold"),
            fg=text_color,
            bg=bg_color
        )
        title_label.pack(pady=(30, 15))
        
        main_frame = tk.Frame(nombre_window, bg=secondary_color, padx=30, pady=25)
        main_frame.pack(padx=30, pady=(0, 20))
        
        instruccion_label = tk.Label(
            main_frame,
            text="Ingresa tu nombre de usuario:",
            font=("Arial", 12),
            fg=text_color,
            bg=secondary_color
        )
        instruccion_label.pack(pady=(0, 15))
        
        nombre_entry = tk.Entry(
            main_frame,
            font=("Arial", 14),
            bg="white",
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            width=20,
            justify=tk.CENTER
        )
        nombre_entry.pack(pady=(0, 20))
        nombre_entry.focus_set()  # Dar foco inmediatamente
        
        botones_frame = tk.Frame(main_frame, bg=secondary_color)
        botones_frame.pack()
        
        def confirmar_nombre():
            nombre = nombre_entry.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Por favor ingresa un nombre")
                return
            self.nombre_resultado = nombre.lower()
            self.nombre_confirmado = True
            nombre_window.destroy()
        
        def cancelar():
            self.nombre_resultado = None
            self.nombre_confirmado = False
            nombre_window.destroy()
        
        tk.Button(
            botones_frame,
            text=" Confirmar",
            command=confirmar_nombre,
            font=("Arial", 10, "bold"),
            bg=primary_color,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            width=12, 
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            botones_frame,
            text="Cancelar",
            command=cancelar,
            font=("Arial", 10),
            bg=bg_color,
            fg=text_color,
            activebackground="#E8E8E8",
            activeforeground=text_color,
            relief=tk.RAISED,
            width=12,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        
        def enter_pressed(event):
            confirmar_nombre()
        
        nombre_entry.bind("<Return>", enter_pressed)
        nombre_window.protocol("WM_DELETE_WINDOW", cancelar)
        nombre_window.wait_window()
        
        if self.nombre_confirmado:
            return self.nombre_resultado
        else:
            return None

    def register_face_gui(self):
        """Registrar rostro con OpenCV LBPH"""
        name = self.SolicitarNombre()
        if not name:
            messagebox.showerror("Error", "Nombre inválido.")
            return 
        
        name = name.strip().lower()
        if not os.path.exists(self.USERS_DIR):
            os.makedirs(self.USERS_DIR)
        
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        count = 0
        faces_data = []
        
        messagebox.showinfo("Instrucción", "Mira a la cámara directamente.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "No se pudo acceder a la cámara.")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (100, 100))
                faces_data.append(face_resized)
                count += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captura {count}/10", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Centrar en la pantalla la ventana de camara
            if count == 1:
                cv2.namedWindow("Registrando rostro", cv2.WINDOW_NORMAL)
                cv2.moveWindow("Registrando rostro", 400, 200)
            
            cv2.imshow("Registrando rostro", frame)
            
            if count >= 10 or cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if faces_data:
            mean_face = np.mean(faces_data, axis=0)  # Promediar las 10 capturas
            filepath = os.path.join(self.USERS_DIR, f"{name}.npy")
            np.save(filepath, mean_face)
            messagebox.showinfo("Registro exitoso", f" Hola {name} !, tu rostro se ha registrado correctamente")
        else:
            messagebox.showwarning("¡INTENTA DE NUEVO!", "No se capturó ningún rostro.")

    def train_lbph_model(self):
        """Entrenamiento del modelo LBPH"""
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces = []
        labels = []
        label_map = {}
        label_count = 0
        
        for file in os.listdir(self.USERS_DIR):
            if file.endswith(".jpg"):
                path = os.path.join(self.USERS_DIR, file)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                name = file.split("_")[0]
                
                if name not in label_map:
                    label_map[name] = label_count
                    label_count += 1
                
                faces.append(img)
                labels.append(label_map[name])
        
        if not faces:
            return None, {}
        
        recognizer.train(faces, np.array(labels))
        return recognizer, {v: k for k, v in label_map.items()}

    def load_known_faces(self):
        """Cargar rostros conocidos"""
        encodings = []
        names = []
        
        for file in os.listdir(self.USERS_DIR):
            if file.endswith(".npy"):
                path = os.path.join(self.USERS_DIR, file)
                encoding = np.load(path).flatten()
                encodings.append(encoding)
                names.append(os.path.splitext(file)[0])
        
        return encodings, names
    
    def login_with_face_gui(self):
        """Login con rostro automático usando OpenCV"""
        if self.login_thread_active:
            messagebox.showwarning("Espera", "El reconocimiento facial ya está en proceso.")
            return
        
        def login_thread():
            self.login_thread_active = True 
            cap = None
            try:
                known_encodings, known_names = self.load_known_faces()
                if not known_encodings:
                    self.root.after(0, lambda: messagebox.showerror("Error", "No hay rostros registrados."))
                    return
                
                cap = cv2.VideoCapture(0)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                start_time = time.time()
                recognized = False
                
                while True:
                    if not self.login_thread_active:
                        break
                    
                    ret, frame = cap.read()
                    if not ret:
                        self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo acceder a la cámara."))
                        break
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    
                    for (x, y, w, h) in faces:
                        face = cv2.resize(gray[y:y+h, x:x+w], (100, 100)).flatten()
                        distances = [np.linalg.norm(face - known_enc) for known_enc in known_encodings]
                        min_distance = min(distances)
                        best_match_index = np.argmin(distances)
                        
                        if min_distance < 3000:
                            name = known_names[best_match_index]
                            label = f"Reconocido: {name}"
                            color = (0, 255, 0)
                            recognized = True
                            recognized_name = name
                        else:
                            label = "Desconocido"
                            color = (0, 0, 255)
                        
                        # Dibujar recuadro y etiqueta
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        
                        if recognized:
                            cv2.imshow("Login con rostro", frame)
                            cv2.waitKey(1000)
                            if cap:
                                cap.release()
                            cv2.destroyAllWindows()
                            self.root.after(0, lambda name=recognized_name: self.MostrarExito(name))
                            return
                    
                    if 'window_positioned' not in locals():
                        cv2.namedWindow("Login con rostro", cv2.WINDOW_NORMAL)
                        cv2.moveWindow("Login con rostro", 400, 200)
                        window_positioned = True
                    
                    cv2.imshow("Login con rostro", frame)
                    
                    if time.time() - start_time > 15:
                        break
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                if cap:
                    cap.release()
                cv2.destroyAllWindows()
                self.root.after(0, lambda: messagebox.showinfo("Login fallido", "No se reconoció ningún rostro o se canceló el login."))
                
            except Exception as e:
                if cap:
                    cap.release()
                cv2.destroyAllWindows()
                error_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror("Error inesperado", error_msg))
            finally:
                self.login_thread_active = False
        
        thread = threading.Thread(target=login_thread, daemon=True)
        thread.start()

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

    def MostrarExito(self, username):
        """Muestra un mensaje de exito"""
        messagebox.showinfo("Bienvenido", "Se ha logeado exitosamente")