import tkinter as tk
from tkinter import colorchooser, Canvas
import math

def seleccionar_color_y_pintar():
    """
    Abre el selector de color y luego pinta la sección seleccionada en la rueda.
    """
    color_seleccionado = colorchooser.askcolor(title="Seleccionar color")
    if color_seleccionado:  # Si el usuario seleccionó un color
        # Obtener el color en formato hexadecimal (el primer elemento de la tupla)
        color_hex = color_seleccionado[1]
        
        # Aplicar el color a la sección de la rueda (necesita una lógica más avanzada para seleccionar la sección)
        # Por ahora, pintaremos el fondo de la ventana para mostrar el color
        root.config(bg=color_hex)

def crear_rueda_colores():
    """
    Crea la ventana principal y un Canvas para dibujar la rueda de colores.
    """
    global root
    root = tk.Tk()
    root.title("Rueda de Colores")

    # Crear un Canvas para dibujar la rueda
    canvas_width = 400
    canvas_height = 400
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    # Definir el centro y el radio de la rueda
    center_x = canvas_width / 2
    center_y = canvas_height / 2
    radius = 150
    
    # Definir el número de secciones de la rueda
    num_sections = 12
    angle_step = 360 / num_sections  # Ángulo de cada sección

    for i in range(num_sections):
        # Calcular los ángulos de inicio y fin para cada arco
        start_angle = i * angle_step
        end_angle = (i + 1) * angle_step
        
        # Convertir ángulos a radianes y luego a coordenadas para el arco
        # Tkinter usa un sistema de coordenadas donde 0 grados está en el eje X positivo (derecha)
        # y los ángulos aumentan en sentido horario. Para esto, invertimos el ángulo de inicio.
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Coordenadas del bounding box para el arco (x0, y0, x1, y1)
        # La función de Tkinter puede usar ángulos de 0 a 360 en sentido horario
        x0 = center_x - radius
        y0 = center_y - radius
        x1 = center_x + radius
        y1 = center_y + radius
        
        # Dibujar el arco
        # En un ejemplo real, se usaría un selector de color aquí para elegir el color para cada sección
        canvas.create_arc(x0, y0, x1, y1,
                          start=start_angle,
                          extent=angle_step,
                          fill="red",  # Color de ejemplo, debe cambiarse dinámicamente
                          outline="black")

    # Botón para seleccionar un color
    button = tk.Button(root, text="Seleccionar Color", command=seleccionar_color_y_pintar)
    button.pack()

    root.mainloop()

# Crear la rueda de colores
crear_rueda_colores()