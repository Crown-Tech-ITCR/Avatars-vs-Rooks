import tkinter as tk
from tkinter import *
from tkinter import simpledialog, messagebox
import cv2
import os
import numpy as np
import threading
import time as time
import random
import pygame
from PIL import Image, ImageTk
from tkinter import Tk, Label
import requests
from bs4 import BeautifulSoup
import time
from pygame import mixer
from enum import Enum
from tkinter import font as tkfont

nombre = None
USERS_DIR = "users_lbph"

# Constantes
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GRID_SIZE = 6
CARD_SIZE = 80
CARD_MARGIN = 5
GAME_TIME_LIMIT = 10
BONUS_TIME = 7
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 150

# Inicialización de la música del juego
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer_music.load("cancion.mp3")
pygame.mixer_music.play(-1, 0, 0)

# URL para la obtención del tipo de cambio del dólar
url = 'https://gee.bccr.fi.cr/indicadoreseconomicos/Cuadros/frmVerCatCuadro.aspx?idioma=1&CodCuadro=%20400'
response = requests.get(url)

# Rutas de imágenes para el modo clásico
IMAGE_PATHS = []
i = 1
while i < 19:
    IMAGE_PATHS.append(f"sprites\\card ({i}).png")
    i += 1

#Lista de los jugadores actuales
lista_nombres=[]

# Colores para elementos de UI
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#808080"
LIGHT_GRAY = "#C8C8C8"
BLUE = "#0064FF"
RED = "#FF0000"
YELLOW = "#D9B41E"
GREEN = "#00FF00"


# === Registrar rostro con OpenCV LBPH ===
def register_face_gui():
    name = simpledialog.askstring("Registro", "Ingresa tu nombre de usuario:")
    if not name:
        messagebox.showerror("Error", "Nombre inválido.")
        return

    name = name.strip().lower()

    if not os.path.exists(USERS_DIR):
        os.makedirs(USERS_DIR)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    count = 0
    faces_data = []

    messagebox.showinfo("Instrucción", "Mira a la cámara. Se capturarán 10 imágenes automáticamente.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resized = cv2.resize(face, (100, 100))
            faces_data.append(face_resized)
            count += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Captura {count}/10", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Registrando rostro", frame)

        if count >= 10 or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if faces_data:
        mean_face = np.mean(faces_data, axis=0)  # Promediar las 10 capturas
        filepath = os.path.join(USERS_DIR, f"{name}.npy")
        np.save(filepath, mean_face)
        messagebox.showinfo("Éxito", f"Rostro guardado correctamente como '{filepath}'")
    else:
        messagebox.showwarning("Sin capturas", "No se capturó ningún rostro.")


# === Entrenamiento del modelo LBPH ===
def train_lbph_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}
    label_count = 0

    for file in os.listdir(USERS_DIR):
        if file.endswith(".jpg"):
            path = os.path.join(USERS_DIR, file)
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


def load_known_faces():
    encodings = []
    names = []

    for file in os.listdir(USERS_DIR):
        if file.endswith(".npy"):
            path = os.path.join(USERS_DIR, file)
            encoding = np.load(path).flatten()
            encodings.append(encoding)
            names.append(os.path.splitext(file)[0])

    return encodings, names


# === Login con rostro ===
# === Login con rostro automático usando OpenCV ===
def login_with_face_gui():
    def login_thread():
        try:
            known_encodings, known_names = load_known_faces()
            if not known_encodings:
                messagebox.showerror("Error", "No hay rostros registrados.")
                return

            cap = cv2.VideoCapture(0)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

            start_time = time.time()
            recognized = False
            name = None

            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "No se pudo acceder a la cámara.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = cv2.resize(gray[y:y + h, x:x + w], (100, 100)).flatten()
                    distances = [np.linalg.norm(face - known_enc) for known_enc in known_encodings]
                    min_distance = min(distances)
                    best_match_index = np.argmin(distances)

                    if min_distance < 4000:
                        name = known_names[best_match_index]
                        label = f"Reconocido: {name}"
                        color = (0, 255, 0)
                        recognized = True
                    else:
                        label = "Desconocido"
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    if recognized:
                        cv2.imshow("Login con rostro", frame)
                        cv2.waitKey(1000)
                        messagebox.showinfo("Login exitoso", f"Bienvenido, {name}!")
                        global lista_nombres, texto_usuario, patrones, clasico, nombre1
                        lista_nombres.append(name)
                        
                        if len(lista_nombres) == 1:
                            #SOLO activar el modo de patrones si se ingresó un solo jugador
                            nombre1 = lista_nombres[0]
                            texto_usuario.config(text=f"¡Bienvenido, {nombre1}!")
                            patrones.config(command=boton_patrones, bg='gray13')
                        elif len(lista_nombres) == 2:
                            #Cuando ya hay dos, se activa el modo clásico
                            nombre2 = lista_nombres[1]
                            texto_usuario.config(text=f"¡Bienvenidos, {nombre1} y {nombre2}!")
                            clasico.config(command=boton_clasico, bg='gray13')
                            patrones.config(command=boton_patrones, bg='gray13')
                        elif len(lista_nombres) > 2:
                            nombre1 = lista_nombres[-2]
                            nombre2 = lista_nombres[-1]
                            texto_usuario.config(text=f"¡Bienvenidos, {nombre1} y {nombre2}!")
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                cv2.imshow("Login con rostro", frame)

                if time.time() - start_time > 15:
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Login fallido", "No se reconoció ningún rostro o se canceló el login.")
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    threading.Thread(target=login_thread).start()

matriz_modo_solitario = [[0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0]]


def separar(lista_original, nombres, puntaje, i, n):
    if i == n:
        return nombres, puntaje
    elif isinstance(lista_original[i], str):
        nombres.append(lista_original[i])
        puntaje.append(int(lista_original[i + 1]))
    return separar(lista_original, nombres, puntaje, i + 2, n)


def ordenar(puntaje1, puntaje2, nombres1, nombres2, max):
    if len(puntaje1) == 0:
        return nombres2, puntaje2
    else:
        n = encontrar_indice(puntaje1, max, 0)
        puntaje2.append(puntaje1[n])
        nombres2.append(nombres1[n])
        del puntaje1[n]
        del nombres1[n]
        return ordenar(puntaje1, puntaje2, nombres1, nombres2, maximo(puntaje1, 0, 0, len(puntaje1)))


def unir(nombres, puntaje, lista_nueva, i, n):
    if i == n:
        return ' '.join(lista_nueva)
    else:
        lista_nueva.append(nombres[i] + ' ' + str(puntaje[i]))
    return unir(nombres, puntaje, lista_nueva, i + 1, n)


def maximo(puntaje, max, i, n):
    if i == n:
        return max
    elif puntaje[i] > max:
        max = puntaje[i]
    return maximo(puntaje, max, i + 1, n)


# Texto para el salón de fama
salon_clasico = open("salon clasico.txt", "r")
salon_fama_clasico = salon_clasico.read()

salon_patrones = open("salon patrones.txt", "r")
salon_fama_patrones = salon_patrones.read()

nombres_clasico, puntaje_clasico = separar(salon_fama_clasico.split(' '), [], [], 0, len(salon_fama_clasico.split(' ')))
nombres_patrones, puntaje_patrones = separar(salon_fama_patrones.split(' '), [], [], 0, len(salon_fama_patrones.split(' ')))


def encontrar_indice(lista, objetivo, i):
    if lista[i] == objetivo:
        return i
    return encontrar_indice(lista, objetivo, i + 1)


def mutear():
    if pygame.mixer_music.get_busy():
        pygame.mixer_music.pause()
    else:
        pygame.mixer_music.unpause()


def encontrar_indice_matriz(matriz, valor):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == valor:
                return (i, j)


def animacion_ganar(frame=0):
    global frames_animacion, gif_ganar, window

    if frame == 92:
        frame = 0
    image = frames_animacion[frame]

    gif_ganar.configure(image=image, bg='black')
    frame += 1

    window.after(30, lambda: animacion_ganar(frame))


# Botones
def boton_patrones():
    global window
    window.destroy()
    ventana_modo_solitario()


def boton_menu():
    global window
    window.destroy()
    ventana_menu()


def boton_salon():
    global window
    window.destroy()
    ventana_salon_fama()


def boton_clasico():
    global window, lista_nombres
    window.destroy()
    window = tk.Tk()
    game = MemoryGameClassic(window, lista_nombres[-2:])  # Pasa los últimos 2 nombres
    window.mainloop()


# Clases
class modo_solitario:
    def __init__(self, matriz):
        self.matriz = matriz
        self.inicio = 1
        self.meta = 3
        self.botones = []
        self.canvases = []
        self.patron = []
        self.jugando = True
        self.animacion_id = None

    def crear_botones(self):
        global inicio1, inicio2
        n = len(self.matriz)
        ancho = 570 / n
        alto = 690 / n
        self.botones = []
        for i in range(n):
            fila_botones = []
            for j in range(n):
                boton = Button(width=5, height=2, command=lambda i=i, j=j: self.realizar_patron(i, j), bg='gray10',
                               fg='white', font='FixedSys')
                boton.place(x=200 + j * ancho, y=10 + i * alto, width=ancho, height=alto)
                fila_botones.append(boton)
            self.botones.append(fila_botones)
        inicio1 = time.time()
        inicio2 = time.time()

    def volver_ceros(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                self.matriz[i][j] = 0
        self.inicio = 1

    def asignar_patron(self):
        if self.meta == 36:
            return self.reiniciar_patron(3)
        largo = len(self.matriz) - 1

        if self.inicio > self.meta:
            self.inicio = 1
            n = len(self.matriz)
            ancho = 570 / n
            alto = 690 / n
            self.canvases = []
            for i in range(n):
                fila_canvases = []
                for j in range(n):
                    canvas = tk.Canvas(window, width=ancho, height=alto, bg='gray10')
                    canvas.place(x=200 + j * ancho, y=10 + i * alto)
                    fila_canvases.append(canvas)
                self.canvases.append(fila_canvases)
            self.jugando = True
            self.mostrar_patron(0)
            return None

        i, j = random.randint(0, largo), random.randint(0, largo)
        if self.matriz[i][j] == 0 and (i, j) not in self.patron:
            self.matriz[i][j] = self.inicio
            self.inicio += 1
            self.patron.append((i, j))
            self.asignar_patron()
        else:
            self.asignar_patron()

    def mostrar_patron(self, m):
        if not self.jugando:
            return None
        if m >= len(self.patron):
            self.crear_botones()
            return None
        i, j = self.patron[m]

        def animacion_mostrar(n):
            if not self.jugando:
                return None
            colores = ['gray20', 'gray30', 'gray40', 'gray50', 'gray40', 'gray30', 'gray20', 'gray10']
            if n < len(colores):
                self.canvases[i][j].configure(bg=colores[n])
                self.animacion_id = window.after(100, lambda: animacion_mostrar(n + 1))
            else:
                self.mostrar_patron(m + 1)

        animacion_mostrar(0)

    def realizar_patron(self, i, j):
        global inicio1, inicio2
        if self.jugando:
            fin1 = time.time()
            if self.matriz[i][j] == self.inicio and fin1 - inicio1 < 12 and fin1 - inicio2 < 2:
                self.botones[i][j].destroy()
                self.canvases[i][j].configure(bg='gray50')
                self.inicio += 1
                if self.inicio > self.meta:
                    self.ganar()
                else:
                    inicio2 = time.time()
            elif self.matriz[i][j] != self.inicio or fin1 - inicio1 >= 12 or fin1 - inicio2 >= 2:
                self.jugando = False
                self.perder()
        else:
            return None

    def ganar(self):
        global gif_ganar, window, puntaje_patrones, nombres_patrones, nombre1
        tiempo = 3
        gif_ganar = tk.Label(window, image = blank)
        gif_ganar.place(x=355, y=350)
        animacion_ganar(frame = 0)
        temporizador = tk.Label(window, text=f"¡Has ganado!\nSiguiendo con el siguiente patrón en {tiempo}", font=('FixedSys', 17), fg='green', bg='black')
        temporizador.place(x=230, y=250)
        iniciar = time.time()
        finalizar = time.time()
        while finalizar - iniciar < 3:
            finalizar = time.time()
            temporizador.configure(text=f"¡Has ganado!\nSiguiendo con el siguiente patrón en {3- (finalizar - iniciar):.0f} segundos")
            window.update()
        temporizador.configure(text=" ")
        if self.meta > puntaje_patrones[-1] and nombre1 not in nombres_patrones:
            puntaje_patrones.append(self.meta)
            nombres_patrones.append(nombre1)
            nombres_patrones, puntaje_patrones = ordenar(puntaje_patrones, [], nombres_patrones, [], maximo(puntaje_patrones, 0, 0, len(puntaje_patrones)))
        elif nombre1 in nombres_patrones and self.meta > puntaje_patrones[encontrar_indice(nombres_patrones, nombre1, 0)]:
            puntaje_patrones[encontrar_indice(nombres_patrones, nombre1, 0)] = self.meta
            nombres_patrones, puntaje_patrones = ordenar(puntaje_patrones, [], nombres_patrones, [], maximo(puntaje_patrones, 0, 0, len(puntaje_patrones)))
        nuevo_salon_patrones = unir(nombres_patrones, puntaje_patrones, [], 0, len(nombres_patrones))
        with open("salon patrones.txt", "w") as file:
            file.write(nuevo_salon_patrones)
        window.update()
        self.meta += 1
        self.agregar_nueva_casilla()

    def perder(self):
        self.jugando = False
        tiempo = 3
        temporizador = tk.Label(window, text=f"¡Has perdido!\nReiniciando en {tiempo}", font=('FixedSys', 17), fg='red',
                                bg='black')
        temporizador.place(x=360, y=250)
        while tiempo > -1:
            temporizador.configure(text=f"¡Has perdido!\nReiniciando en {tiempo}")
            time.sleep(1)
            tiempo -= 1
            window.update()
        temporizador.configure(text=" ")
        window.update()
        self.meta = 3
        self.reiniciar_patron(self.meta)

    def agregar_nueva_casilla(self):
        largo = len(self.matriz) - 1
        while True:
            i, j = random.randint(0, largo), random.randint(0, largo)
            if (i, j) not in self.patron:
                self.patron.append((i, j))
                self.matriz[i][j] = self.meta
                break
        self.jugando = True
        n = len(self.matriz)
        ancho = 570 / n
        alto = 690 / n
        self.canvases = []
        for i in range(n):
            fila_canvases = []
            for j in range(n):
                canvas = tk.Canvas(window, width=ancho, height=alto, bg='gray10')
                canvas.place(x=200 + j * ancho, y=10 + i * alto)
                fila_canvases.append(canvas)
            self.canvases.append(fila_canvases)

        self.inicio = 1
        self.mostrar_patron(0)

    def reiniciar_patron(self, meta):
        self.patron = []
        if self.animacion_id is not None:
            window.after_cancel(self.animacion_id)
            self.animacion_id = None
        for fila in self.botones:
            for boton in fila:
                boton.destroy()
        for fila in self.canvases:
            for canvas in fila:
                canvas.destroy()
        self.inicio = 1
        self.meta = meta
        self.botones = []
        self.canvases = []
        self.jugando = True
        self.volver_ceros()
        self.asignar_patron()


# Enum para estados del juego
class GameState(Enum):
    #Enumeración de los estados posibles del juego
    MENU = 1  # Estado de menú principal
    PLAYING = 2  # Estado de juego activo
    GAME_OVER = 3  # Estado de juego terminado


# Clase Card
class Card:
    #Representa una carta del juego de memoria

    def __init__(self, canvas, x, y, image_id): #Inicializa una carta en la posición (x,y) con una imagen específica
        # Canvas donde se dibuja
        self.canvas = canvas
        # Posición
        self.x = x
        self.y = y
        # ID de la imagen
        self.card_image_id = image_id
        # Estado de la carta
        self.is_flipped = False  # Si está volteada
        self.is_matched = False  # Si está emparejada
        # IDs de elementos del canvas
        self.rect_id = None  # ID del rectángulo
        self.text_id = None  # ID del texto
        self.image_obj = None  # Objeto de imagen
        self.canvas_image_id = None  # ID de la imagen en el canvas
        # Cargar y dibujar la carta
        self.load_image()
        self.draw()

    def load_image(self):#Carga la imagen de la carta desde el disco

        try:
            # Obtener ruta de la imagen
            image_path = IMAGE_PATHS[self.card_image_id]
            # Abrir y redimensionar imagen
            image = Image.open(image_path)
            image = image.resize((CARD_SIZE, CARD_SIZE), Image.Resampling.LANCZOS)
            # Convertir a formato compatible con tkinter
            self.image_obj = ImageTk.PhotoImage(image)
        except Exception as e:
            # Manejar errores de carga
            print(f"Error cargando imagen {image_path}: {e}")
            self.image_obj = None

    def draw(self):#Dibuja la carta en el canvas según su estado

        # Eliminar elementos anteriores
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        if self.text_id:
            self.canvas.delete(self.text_id)
        if self.canvas_image_id:
            self.canvas.delete(self.canvas_image_id)

        # Dibujar según el estado
        if self.is_matched or self.is_flipped:
            # Carta volteada o emparejada
            if self.image_obj:
                # Dibujar imagen si está disponible
                self.canvas_image_id = self.canvas.create_image(
                    self.x + CARD_SIZE // 2, self.y + CARD_SIZE // 2,
                    image=self.image_obj, anchor=tk.CENTER
                )
                # Configurar borde
                outline_color = GREEN if self.is_matched else BLACK
                outline_width = 4 if self.is_matched else 2
                self.rect_id = self.canvas.create_rectangle(
                    self.x, self.y, self.x + CARD_SIZE, self.y + CARD_SIZE,
                    outline=outline_color, width=outline_width
                )
            else:
                # Dibujar rectángulo si no hay imagen
                fill_color = GREEN if self.is_matched else GRAY
                self.rect_id = self.canvas.create_rectangle(
                    self.x, self.y, self.x + CARD_SIZE, self.y + CARD_SIZE,
                    fill=fill_color, outline=YELLOW, width=2
                )
        else:
            # Carta no volteada
            self.rect_id = self.canvas.create_rectangle(
                self.x, self.y, self.x + CARD_SIZE, self.y + CARD_SIZE,
                fill=LIGHT_GRAY, outline=YELLOW, width=2
            )

    def is_clicked(self, pos):#Verifica si la carta fue clickeada

        if self.is_matched:
            return False  # Cartas emparejadas no se pueden clickear
        x, y = pos
        # Verificar si la posición está dentro de la carta
        return (self.x <= x <= self.x + CARD_SIZE and
                self.y <= y <= self.y + CARD_SIZE)


# Clase GameBoard
class GameBoard:#Representa el tablero de juego para un jugador

    def __init__(self, canvas, player_id, offset_x):#Inicializa el tablero para un jugador

        self.canvas = canvas
        self.player_id = player_id
        self.offset_x = offset_x
        self.cards = []  # Matriz de cartas
        self.flipped_cards = []  # Cartas volteadas
        self.matched_pairs = 0  # Parejas encontradas
        self.attempts = 0  # Intentos realizados
        self._create_board()  # Crear el tablero

    def _create_board(self):#Crea y distribuye las cartas en el tablero

        # Crear lista de IDs de imágenes (pares)
        image_ids = list(range(18)) * 2
        random.shuffle(image_ids)  # Mezclar aleatoriamente

        self.cards = []
        # Crear matriz de cartas
        for row in range(GRID_SIZE):
            card_row = []
            for col in range(GRID_SIZE):
                # Calcular posición
                x = self.offset_x + col * (CARD_SIZE + CARD_MARGIN)
                y = BOARD_OFFSET_Y + row * (CARD_SIZE + CARD_MARGIN)
                # Obtener ID de imagen
                image_id = image_ids[row * GRID_SIZE + col]
                # Crear carta
                card = Card(self.canvas, x, y, image_id)
                card_row.append(card)
            self.cards.append(card_row)

    def handle_click(self, pos):#Maneja el click en una carta

        if len(self.flipped_cards) >= 2:
            return False  # Ya hay dos cartas volteadas

        # Buscar la carta clickeada
        for row in self.cards:
            for card in row:
                if card.is_clicked(pos) and not card.is_flipped and not card.is_matched:
                    # Voltear la carta
                    card.is_flipped = True
                    card.draw()
                    self.flipped_cards.append(card)
                    return True  # Carta volteada
        return False  # No se volteó ninguna carta

    def check_match(self):#Verifica si las cartas volteadas hacen pareja

        if len(self.flipped_cards) == 2:
            card1, card2 = self.flipped_cards
            if card1.card_image_id == card2.card_image_id:
                # Pareja encontrada
                card1.is_matched = True
                card2.is_matched = True
                card1.draw()
                card2.draw()
                self.matched_pairs += 1
                self.flipped_cards.clear()
                self.attempts += 1
                return True
            else:
                # No es pareja
                self.attempts += 1
                return False
        return False

    def reset_flipped_cards(self):#Voltea las cartas que no están emparejadas

        for card in self.flipped_cards:
            if not card.is_matched:
                card.is_flipped = False
                card.draw()
        self.flipped_cards.clear()

    def is_complete(self):#Verifica si se completó el tablero

        return self.matched_pairs == 18


# Clase Player
class Player:#Representa un jugador

    def __init__(self, name, player_id):#Inicializa un jugador con nombre e ID

        self.name = name
        self.player_id = player_id
        self.score = 0  # Puntaje
        self.attempts = 0  # Intentos
        self.pairs_found = 0  # Parejas encontradas

    def update_score(self, attempts, pairs_found):#Actualiza el puntaje del jugador

        self.attempts = attempts
        self.pairs_found = pairs_found
        # Fórmula simple para calcular puntaje
        self.score = max(0, 1000 - attempts * 10)
        print(f"score={self.score}")


# Clase Timer
class Timer:#Temporizador para controlar los turnos


    def __init__(self, duration, update_callback=None):#Inicializa el temporizador con duración y callback

        self.duration = duration  # Duración total
        self.start_time = time.time()  # Tiempo de inicio
        self.paused = False  # Estado de pausa
        self.update_callback = update_callback  # Callback para actualizar

    def get_remaining_time(self):#Obtiene tiempo restante

        if self.paused:
            return self.duration  # Si está pausado, devuelve duración completa
        elapsed = time.time() - self.start_time
        return max(0, self.duration - elapsed)  # Tiempo restante

    def get_remaining_time_rounded(self):#Obtiene tiempo restante redondeado

        return max(0, round(self.get_remaining_time(), 1))

    def is_expired(self):#Verifica si el tiempo se agotó

        return self.get_remaining_time() <= 0

    def reset(self, duration=None):#Reinicia el temporizador

        if duration:
            self.duration = duration
        self.start_time = time.time()
        self.paused = False

    def add_time(self, extra_time):#Añade tiempo adicional

        self.duration += extra_time

    def pause(self):#Pausa el temporizador

        self.paused = True

    def resume(self):#Reanuda el temporizador

        self.paused = False


# Clase principal del juego
class MemoryGameClassic:#Clase principal del juego de memoria en modo clásico


    def __init__(self, root,player_names=None):#Inicializa el juego con la ventana principal

        # Configurar ventana principal
        self.root = root
        self.root.title("Juego de Memoria - Modo Clásico")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Configurar fuentes
        self.font = tkfont.Font(family='FixedSys', size=12)
        self.big_font = tkfont.Font(family='FixedSys', size=16, weight='bold')

        # Crear canvas principal
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BLACK)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.create_buttons()  # Crear botones de interfaz

        # Inicializar jugadores
        global lista_nombres
        if player_names and len(player_names) >= 2:
            self.players = [
                Player(player_names[0], 0),
                Player(player_names[1], 1)
            ]
        else:
            # Si no hay suficientes nombres, usar los últimos dos de lista_nombres
            if len(lista_nombres) >= 2:
                self.players = [
                    Player(lista_nombres[-2], 0),  # Penúltimo nombre
                    Player(lista_nombres[-1], 1)  # Último nombre
                ]
            else:
                # Fallback a nombres predeterminados si no hay suficientes nombres
                self.players = [
                    Player("Jugador 1", 0),
                    Player("Jugador 2", 1)
                ]

        self.current_player = 0  # Jugador actual

        # Crear tableros para cada jugador
        self.boards = [
            GameBoard(self.canvas, 0, BOARD_OFFSET_X),
            GameBoard(self.canvas, 1, BOARD_OFFSET_X + 600)
        ]

        # Configurar temporizador
        self.timer = Timer(GAME_TIME_LIMIT, self.update_timer_display)
        self.timer_display = None  # ID del texto del temporizador
        self.match_message_id = None  # ID del mensaje de pareja

        # Estado del juego
        self.game_state = GameState.PLAYING
        self.winner = None  # Jugador ganador
        self.match_found = False  # Bandera de pareja encontrada
        self.match_timer = 0  # Temporizador para mensajes de pareja

        # Configurar eventos
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Key>", self.on_key_press)

        # Dibujar e iniciar actualizaciones
        self.draw_game()
        self.update_timer_display()
        self.update_game()
        self.update_timer_smoothly()

        # Cargar frames de animación
        self.frames_animacion = []
        self.load_animation_frames()
        self.blank = ImageTk.PhotoImage(Image.open("frames\\blank.png"))
        self.gif_ganar = None

        # Configurar nombres de jugadores
        if player_names and len(player_names) >= 2:
            self.players = [
                Player(player_names[0], 0),
                Player(player_names[1], 1)
            ]
        else:
            # Valores por defecto si no hay nombres
            self.players = [
                Player("Jugador 1", 0),
                Player("Jugador 2", 1)
            ]

        # Configurar sonidos
        self.music_paused = False
        pygame.init()
        mixer.init()
        try:
            self.sound_error = mixer.Sound("Fallo.mp3")
            self.sound_success = mixer.Sound("Correct.mp3")
            self.sound_victory = mixer.Sound("Ventana.mp3")
        except:
            print("Advertencia: No se pudieron cargar algunos efectos de sonido")
            self.sound_error = None
            self.sound_success = None
            self.sound_victory = None

    def load_animation_frames(self):
        # Cargar los 91 frames del GIF
        i = 1
        while i < 92:
            try:
                img = Image.open(f"frames\\frame ({i}).gif")
                frm = ImageTk.PhotoImage(img)
                self.frames_animacion.append(frm)
                i += 1
            except Exception as e:
                print(f"Error cargando frame ({i}).gif: {e}")
                break

    def animacion_gane(self, frame=0):
        if frame >= 92:
            frame = 0
        image = self.frames_animacion[frame]
        self.gif_ganar.configure(image=image)
        frame += 1
        self.root.after(30, lambda: self.animacion_gane(frame))

    def on_click(self, event):#Maneja clicks del mouse

        if self.game_state == GameState.PLAYING:
            self.handle_click((event.x, event.y))

    def on_key_press(self, event):#Maneja pulsaciones de teclas

        if event.keysym == 'Escape':
            pygame.quit()  # Cerrar Pygame
            self.root.quit()  # Salir del juego
        elif event.keysym.lower() == 'r' and self.game_state == GameState.GAME_OVER:
            self.restart_game()  # Reiniciar juego

    def handle_click(self, pos):#Procesa un click en el tablero

        if self.game_state == GameState.PLAYING:
            current_board = self.boards[self.current_player]

            if current_board.handle_click(pos):
                if len(current_board.flipped_cards) == 2:
                    self.match_found = current_board.check_match()
                    if self.match_found:
                        # Reproducir sonido de éxito
                        if self.sound_success:
                            self.sound_success.play()

                        # Añadir tiempo bonus
                        self.timer.add_time(BONUS_TIME)
                        # Actualizar puntaje
                        self.players[self.current_player].update_score(
                            current_board.attempts,
                            current_board.matched_pairs
                        )
                        print(
                            f"Jugador {self.current_player + 1} encontró pareja. "
                            f"Parejas: {current_board.matched_pairs}/18"
                        )
                        # Mostrar mensaje de pareja
                        self.match_timer = time.time()
                        if self.match_message_id:
                            self.canvas.delete(self.match_message_id)
                        self.match_message_id = self.canvas.create_text(
                            WINDOW_WIDTH // 2, 120,
                            text="¡Pareja encontrada!",
                            font=self.big_font, fill=YELLOW
                        )
                        # Verificar si el juego terminó
                        if current_board.is_complete():
                            self.end_game()
                            return
                    else:
                        # Reproducir sonido de error
                        if self.sound_error:
                            self.sound_error.play()
                        self.match_timer = time.time()
                    self.draw_game()

    def update_game(self):#Actualiza el estado del juego periódicamente
        if self.game_state == GameState.PLAYING:# Manejar cartas volteadas
            if len(self.boards[self.current_player].flipped_cards) == 2:
                if time.time() - self.match_timer > 1.5:
                    if not self.match_found:
                        # Voltear cartas si no son pareja
                        self.boards[self.current_player].reset_flipped_cards()
                        # Cambiar turno
                        self.current_player = 1 - self.current_player
                        self.timer.reset(GAME_TIME_LIMIT)
                    else:
                        # Limpiar mensaje de pareja
                        self.match_found = False
                        if self.match_message_id:
                            self.canvas.delete(self.match_message_id)
                            self.match_message_id = None
                    self.draw_game()

            # Cambiar turno si se acaba el tiempo
            if self.timer.is_expired() and len(self.boards[self.current_player].flipped_cards) < 2:
                self.current_player = 1 - self.current_player
                self.timer.reset(GAME_TIME_LIMIT)
                self.draw_game()

        # Programar próxima actualización
        self.root.after(100, self.update_game)

    def update_timer_display(self):#Actualiza la visualización del temporizador

        if self.timer_display:
            self.canvas.delete(self.timer_display)

        # Obtener y mostrar tiempo restante
        remaining_time = self.timer.get_remaining_time_rounded()
        timer_color = RED if remaining_time <= 3 else WHITE  # Rojo si queda poco tiempo
        self.timer_display = self.canvas.create_text(WINDOW_WIDTH // 2, 70, text=f"Tiempo: {remaining_time}s",
                                                     font=self.big_font, fill=timer_color)

    def update_timer_smoothly(self):#Actualiza el temporizador suavemente
        if self.game_state == GameState.PLAYING:
            self.update_timer_display()
        # Programar próxima actualización
        self.root.after(100, self.update_timer_smoothly)

    def end_game(self):#Finaliza el juego
        self.game_state = GameState.GAME_OVER
        self.winner = self.players[self.current_player]
        print(f"¡Juego terminado! {self.winner.name} completó todas las parejas y gana!")
        self.draw_game_over()

    def restart_game(self):#Reinicia el juego
        # Reiniciar pygame y mixer
        pygame.quit()
        pygame.init()
        mixer.init()
        try:
            # Cargar sonidos
            self.sound_error = mixer.Sound("Fallo.mp3")
            self.sound_success = mixer.Sound("Correct.mp3")
            self.sound_victory = mixer.Sound("Ventana.mp3")
        except:
            print("Advertencia: No se pudieron cargar algunos efectos de sonido")
            self.sound_error = None
            self.sound_success = None
            self.sound_victory = None

        # Restablecer estado del juego
        self.game_state = GameState.PLAYING
        self.current_player = 0
        self.winner = None
        self.match_found = False

        # Reiniciar jugadores
        for player in self.players:
            player.score = 0
            player.attempts = 0
            player.pairs_found = 0

        # Limpiar y recrear tableros
        self.canvas.delete("all")
        self.boards = [
            GameBoard(self.canvas, 0, BOARD_OFFSET_X),
            GameBoard(self.canvas, 1, BOARD_OFFSET_X + 600)
        ]

        # Reiniciar temporizador y dibujar
        self.timer.reset(GAME_TIME_LIMIT)
        self.draw_game()
        self.update_timer_display()

    def save_winner_score(self, winner_name, winner_score, filename="salon clasico.txt"):
        global nombres_clasico, puntaje_clasico
        try:
            # Agregar el nuevo puntaje y nombre
            nombres_clasico.append(winner_name)
            puntaje_clasico.append(winner_score)

            # Ordenar los puntajes de mayor a menor
            nombres_sorted, puntaje_sorted = ordenar(puntaje_clasico.copy(), [], nombres_clasico.copy(), [],
                                                     maximo(puntaje_clasico, 0, 0, len(puntaje_clasico)))

            # Limitar a los 5 mejores puntajes
            nombres_sorted = nombres_sorted[:5]
            puntaje_sorted = puntaje_sorted[:5]

            lista_nueva = unir(nombres_sorted, puntaje_sorted, [], 0, len(nombres_sorted))

            # Escribir en el archivo
            with open(filename, "w") as salon:
                salon.write(lista_nueva)

            # Actualizar las listas globales
            nombres_clasico = nombres_sorted
            puntaje_clasico = puntaje_sorted
        except Exception as e:
            print(f"Error al guardar el puntaje: {e}")

    def draw_game(self):#Dibuja la interfaz del juego

        # Limpiar elementos de interfaz anteriores
        items = self.canvas.find_withtag("ui")
        for item in items:
            self.canvas.delete(item)

        # Dibujar información de jugadores
        y_offset = 50
        for i, player in enumerate(self.players):
            # Resaltar jugador actual
            color = GREEN if i == self.current_player else WHITE
            pairs_found = self.boards[i].matched_pairs
            self.canvas.create_text(BOARD_OFFSET_X + i * 600, y_offset,
                                    text=f"{player.name}: {self.boards[i].attempts} intentos, {pairs_found}/18 parejas",
                                    font=self.big_font, fill=color, anchor=tk.NW, tags="ui")
        # Mostrar turno actual
        self.canvas.create_text(WINDOW_WIDTH // 2, 100, text=f"Turno: {self.players[self.current_player].name}",
                                font=self.big_font, fill=BLUE, tags="ui")

    def draw_game_over(self):
        # Guardar el puntaje del ganador
        self.save_winner_score(self.winner.name, self.winner.score)
        # Reproducir sonido de victoria
        if self.sound_victory:
            self.sound_victory.play()

        # Crear ventana de victoria
        victory_window = tk.Toplevel(self.root)
        victory_window.title("¡Juego Terminado!")
        victory_window.geometry("600x500")
        victory_window.configure(bg=BLACK)
        victory_window.resizable(False, False)

        # Centrar ventana
        victory_window.transient(self.root)
        victory_window.grab_set()  # Hacer modal
        x = self.root.winfo_x() + (WINDOW_WIDTH - 600) // 2
        y = self.root.winfo_y() + (WINDOW_HEIGHT - 500) // 2
        victory_window.geometry(f"+{x}+{y}")

        # Frame principal para organizar mejor los elementos
        main_frame = tk.Frame(victory_window, bg=BLACK)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Mostrar animación de victoria
        self.gif_ganar = tk.Label(main_frame, image=self.blank, bg=BLACK)
        self.gif_ganar.pack(pady=(0, 20))
        self.animacion_gane(frame=0)

        # Información del ganador
        tk.Label(
            main_frame,
            text=f"¡{self.winner.name} GANA!",
            font=('Arial', 24, 'bold'),
            fg=GREEN,
            bg=BLACK
        ).pack(pady=(0, 10))

        # Etiqueta de intentos
        tk.Label(
            main_frame,
            text=f"Parejas completadas: {self.boards[self.winner.player_id].matched_pairs}/18\n" +
                 f"Intentos: {self.boards[self.winner.player_id].attempts}",
            font=('Arial', 14),
            fg=WHITE,
            bg=BLACK
        ).pack(pady=(0, 30))

        # Frame especial solo para los botones
        button_frame = tk.Frame(main_frame, bg=BLACK)
        button_frame.pack(fill=tk.X, pady=(20, 10))

        # Botón Jugar de nuevo (a la izquierda)
        tk.Button(
            button_frame,
            text="Jugar de nuevo",
            command=lambda: [self.restart_game(), victory_window.destroy()],
            bg=BLACK,
            fg=YELLOW,
            font=self.font,
            width=15
        ).pack(side=tk.LEFT, expand=True, padx=10)

        # Botón Salir (a la derecha)
        tk.Button(
            button_frame,
            text="Salir",
            command=lambda: [boton_menu(), victory_window.destroy()],
            bg=BLACK,
            fg=YELLOW,
            font=self.font,
            width=15
        ).pack(side=tk.RIGHT, expand=True, padx=10)

        # Manejar teclas en ventana de victoria
        victory_window.bind("<Key>", lambda event: self.handle_victory_key(event, victory_window))

    def handle_victory_key(self, event, victory_window):#Maneja teclas en ventana de victoria

        if event.keysym == 'Escape':
            self.root.quit()  # Salir con Escape
            victory_window.destroy()
        elif event.keysym.lower() == 'r' and self.game_state == GameState.GAME_OVER:
            self.restart_game()  # Reiniciar con R
            victory_window.destroy()

    def create_buttons(self):#Crea los botones de la interfaz

        button_frame = tk.Frame(self.root, bg=BLACK)
        button_frame.place(x=50, y=10, width=1100, height=40)

        # Botón de silencio
        self.button1 = tk.Button(button_frame, text="Silenciar", command=mutear, bg=BLACK, fg=YELLOW, font=self.font)
        self.button1.pack(side=tk.LEFT, padx=10)

        # Botón de reinicio
        self.button2 = tk.Button(button_frame, text="Reinicio", command=lambda: self.restart_game(), bg=BLACK,
                                 fg=YELLOW, font=self.font)
        self.button2.pack(side=tk.LEFT, padx=10)

        # Botón de menú
        self.button3 = tk.Button(button_frame, text="Menú", command=boton_menu, bg=BLACK, fg=YELLOW, font=self.font)
        self.button3.pack(side=tk.LEFT, padx=10)


# Esto es para el modo de patrones xD solo es para reiniciar la vara
def reiniciar():
    global solitaire
    solitaire.reiniciar_patron(3)


# === Interfaz Tkinter ===

def ventana_menu():
    global texto_usuario, window, clasico, patrones,lista_nombre
    window = tk.Tk()
    window.title("Memory Game")
    window.geometry("500x500")
    window.configure(bg="black")

    tk.Label(window, text="Memory Game", font=("FixedSys", 20), bg='black', fg="#D9B41E").pack(pady=10)
    texto_usuario = tk.Label(window, text="Por favor, inicia sesión o registra tu rostro", font=("FixedSys", 14),
                             bg='black', fg="#D9B41E")
    texto_usuario.pack(pady=10)

    tk.Button(window, text="Registrar nuevo rostro", command=register_face_gui, width=30, height=2, font='FixedSys',
              fg="#D9B41E", bg='gray13').pack(pady=10)
    tk.Button(window, text="Iniciar sesión con rostro", command=login_with_face_gui, width=30, height=2,
              font='FixedSys', fg="#D9B41E", bg='gray13').pack(pady=10)
    clasico = tk.Button(window, text="Modo clásico", command=None, width=30, height=2, font='FixedSys', fg="#D9B41E",
                        bg='gray2')
    clasico.pack(pady=10)
    patrones = tk.Button(window, text="Modo patrones", command=None, width=30, height=2, font='FixedSys', fg="#D9B41E",
                         bg='gray2')
    patrones.pack(pady=10)
    premios = tk.Button(window, text="Premios", command=boton_salon, width=30, height=2, font='FixedSys', fg="#D9B41E",
                        bg='gray13')
    premios.pack(pady=10)
    tk.Button(window, text="Salir", command=window.destroy, width=30, height=2, font='FixedSys', fg="#D9B41E",
              bg='gray13').pack(pady=10)
    tk.Button(window, text="Silenciar", font=('FixedSys', 5), bg="gray13", fg="#D9B41E", command=mutear).place(x=25,
                                                                                                               y=432,
                                                                                                               width=80)

    if len(lista_nombres) == 1:
        texto_usuario.config(text=f"¡Bienvenido, {lista_nombres[0]}!")
        patrones.config(command=boton_patrones, bg='gray13')
        clasico.config(command=None, bg='gray2')  # Mantener desactivado
    elif len(lista_nombres) >= 2:
        texto_usuario.config(text=f"¡Bienvenido(a), {lista_nombres[-2]} y {lista_nombres[-1]}!")
        patrones.config(command=boton_patrones, bg='gray13')
        clasico.config(command=boton_clasico, bg='gray13')

    window.mainloop()


def ventana_modo_solitario():
    global window, solitaire, frames_animacion, blank, gif_ganar
    frames_animacion = []
    window = Tk()
    window.minsize(width=800, height=724)
    window.configure(bg="black")

    i = 1
    while i < 92:
        img = Image.open(f"frames\\frame ({i}).gif")
        frm = ImageTk.PhotoImage(img)
        frames_animacion.append(frm)
        i += 1

    blank = ImageTk.PhotoImage(Image.open("frames\\blank.png"))

    tk.Button(window, text="Silenciar", font=('FixedSys', 16), bg="gray13", fg="#D9B41E", command=mutear).place(x=25,
                                                                                                                y=150,
                                                                                                                width=150)
    tk.Button(window, text="Menú inicial", font=('FixedSys', 16), bg="gray13", fg="#D9B41E", command=boton_menu).place(
        x=25, y=250, width=150)
    tk.Button(window, text="Reiniciar", font=('FixedSys', 16), bg="gray13", fg="#D9B41E", command=reiniciar).place(x=25,
                                                                                                                   y=350,
                                                                                                                   width=150)

    solitaire = modo_solitario(matriz_modo_solitario)
    solitaire.asignar_patron()

    window.mainloop()


def ventana_salon_fama():
    global window, boton_volver, nombres_clasico, puntaje_clasico, nombres_patrones, puntaje_patrones

    window = Tk()
    window.title('Battle Elves - Salón de fama')
    window.minsize(width=500, height=500)
    window.configure(bg="black")

    soup = BeautifulSoup(response.text, 'html.parser')
    tipo_cambio = soup.get_text()
    tipo_cambio = int(tipo_cambio[5109:5115].replace(',','')) / 100
    premios_clasico = []
    premios_patrones = []
    for puntos in puntaje_clasico:
        premios_clasico.append(round(100 * tipo_cambio / puntos, 2))
    for puntos in puntaje_patrones:
        premios_patrones.append(round(100 * tipo_cambio / puntos, 2))

    texto_clasico = f'Modo clásico:\n\n{nombres_clasico[0]}    {premios_clasico[0]}\n\n{nombres_clasico[1]}    {premios_clasico[1]}\n\n{nombres_clasico[2]}    {premios_clasico[2]}\n\n{nombres_clasico[3]}    {premios_clasico[3]}\n\n{nombres_clasico[4]}    {premios_clasico[4]}'
    texto_salon_clasico = Label(text=texto_clasico, font='FixedSys', bg='black', fg='#D9B41E')
    texto_salon_clasico.pack(pady=30)

    texto_patrones = f'Modo patrones:\n\n{nombres_patrones[0]}    {premios_patrones[0]}\n\n{nombres_patrones[1]}    {premios_patrones[1]}\n\n{nombres_patrones[2]}    {premios_patrones[2]}\n\n{nombres_patrones[3]}    {premios_patrones[3]}\n\n{nombres_patrones[4]}    {premios_patrones[4]}'
    texto_salon_patrones = Label(text=texto_patrones, font='FixedSys', bg='black', fg='#D9B41E')
    texto_salon_patrones.pack(pady=30)

    boton_volver = Button(text='Menú principal', bg='gray13', fg = '#D9B41E', width=15, command = boton_menu, font='FixedSys')
    boton_volver.pack(pady=50)

    window.mainloop()


if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)
ventana_menu()