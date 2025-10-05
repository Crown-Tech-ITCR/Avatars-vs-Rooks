import tkinter as tk
from tkinter import Canvas, Label, Frame
from PIL import Image, ImageTk
import colorsys

class ColorPicker(tk.Frame):
    def __init__(self, master=None, width=256, height=256, bar_width=28):
        super().__init__(master)
        self.width = width
        self.height = height
        self.bar_width = bar_width
        self.selected_color = "#FFFFFFFF"
        
        # IMPORTANTE: Definir valores HSV ANTES de crear imágenes
        self.value = 1.0
        self.hue = 0.0
        self.saturation = 0.0
        
        # Ahora crear las imágenes (que necesitan self.value)
        self.sv_image = self.create_sv_image()
        self.value_bar_img = self.create_value_bar_img()
        self.sv_photo = ImageTk.PhotoImage(self.sv_image)
        self.bar_photo = ImageTk.PhotoImage(self.value_bar_img)
        
        # Crear canvas
        self.sv_canvas = Canvas(self, width=self.width, height=self.height)
        self.bar_canvas = Canvas(self, width=self.bar_width, height=self.height)
        self.sv_canvas.create_image(0, 0, anchor="nw", image=self.sv_photo)
        self.bar_canvas.create_image(0, 0, anchor="nw", image=self.bar_photo)
        self.sv_canvas.grid(row=0, column=0, padx=(5,0), pady=5)
        self.bar_canvas.grid(row=0, column=1, padx=(5,5), pady=5)
        
        # Bind events - incluyendo arrastrar mouse
        self.sv_canvas.bind("<Button-1>", self.select_sv)
        self.sv_canvas.bind("<B1-Motion>", self.select_sv)  # Arrastrar mouse
        self.bar_canvas.bind("<Button-1>", self.select_value)
        self.bar_canvas.bind("<B1-Motion>", self.select_value)  # Arrastrar mouse
        
        # Actualizar imagen inicial
        self.update_sv_image()
        
        # Label para mostrar color
        self.color_label = Label(self, text="Color: #FFFFFF", font=("Arial", 14))
        self.color_label.grid(row=1, column=0, columnspan=2)
        
        # Frame para la paleta monocromática
        self.palette_frame = Frame(self)
        self.palette_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Label y contenedor para la paleta
        palette_title = Label(self.palette_frame, text="Paleta Monocromática:", font=("Arial", 12, "bold"))
        palette_title.pack()
        
        self.palette_container = Frame(self.palette_frame)
        self.palette_container.pack(pady=5)
        
        # Lista para almacenar los labels de colores de la paleta
        self.palette_labels = []
        self.create_monochromatic_palette()

    def create_sv_image(self):
        img = Image.new("RGB", (self.width, self.height))
        for x in range(self.width):
            h = x / self.width
            for y in range(self.height):
                s = y / self.height
                r, g, b = colorsys.hsv_to_rgb(h, s, self.value)
                img.putpixel((x, y), (int(r*255), int(g*255), int(b*255)))
        return img

    def create_value_bar_img(self):
        img = Image.new("RGB", (self.bar_width, self.height))
        for y in range(self.height):
            v = 1 - y / self.height
            gray = int(v * 255)
            for x in range(self.bar_width):
                img.putpixel((x, y), (gray, gray, gray))
        return img

    def generate_monochromatic_palette(self, base_hue, base_saturation, num_colors=7):
        """
        Genera una paleta monocromática variando el valor (brillo) y ligeramente la saturación
        Incluye el color exacto seleccionado por el usuario
        """
        colors = []
        
        # Usar el valor actual como referencia central
        base_value = self.value
        
        # Calcular el índice donde colocar el color seleccionado (en el centro)
        selected_index = num_colors // 2
        
        # Generar variaciones de brillo alrededor del valor actual
        for i in range(num_colors):
            if i == selected_index:
                # Usar el color exacto seleccionado por el usuario
                value = base_value
                sat_variation = base_saturation
            else:
                # Crear variaciones para los otros colores
                # Determinar si estamos antes o después del color seleccionado
                if i < selected_index:
                    # Colores más oscuros (valores menores)
                    steps_from_center = selected_index - i
                    max_steps = selected_index
                    value = base_value * (1 - 0.7 * (steps_from_center / max_steps)) if max_steps > 0 else base_value
                    value = max(0.1, value)
                else:
                    # Colores más claros (valores mayores)
                    steps_from_center = i - selected_index
                    max_steps = num_colors - 1 - selected_index
                    if max_steps > 0:
                        brightness_increase = (1 - base_value) * (steps_from_center / max_steps)
                        value = min(1.0, base_value + brightness_increase)
                    else:
                        value = base_value
                
                # Variar ligeramente la saturación para mayor riqueza visual
                if base_saturation > 0.1:
                    sat_variation = base_saturation * (0.7 + 0.6 * (i / (num_colors - 1)))
                    sat_variation = min(1.0, max(0.1, sat_variation))
                else:
                    sat_variation = base_saturation
            
            r, g, b = colorsys.hsv_to_rgb(base_hue, sat_variation, value)
            color_hex = '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
            colors.append(color_hex)
        
        return colors

    def create_monochromatic_palette(self):
        """
        Crea los widgets para mostrar la paleta monocromática
        """
        # Generar paleta inicial
        palette_colors = self.generate_monochromatic_palette(self.hue, self.saturation)
        
        # Crear labels para cada color
        for i, color in enumerate(palette_colors):
            # Marcar el color seleccionado con un borde más grueso
            selected_index = len(palette_colors) // 2
            border_width = 3 if i == selected_index else 1
            
            label = Label(self.palette_container, 
                         width=8, height=3, 
                         bg=color, 
                         text=color,
                         font=("Arial", 8),
                         fg="white" if self.is_dark_color(color) else "black",
                         relief="solid",
                         borderwidth=border_width)
            label.grid(row=0, column=i, padx=2)
            self.palette_labels.append(label)

    def update_monochromatic_palette(self):
        """
        Actualiza la paleta monocromática cuando cambia el color seleccionado
        """
        palette_colors = self.generate_monochromatic_palette(self.hue, self.saturation)
        selected_index = len(palette_colors) // 2
        
        for i, (label, color) in enumerate(zip(self.palette_labels, palette_colors)):
            # Marcar el color seleccionado con un borde más grueso
            border_width = 3 if i == selected_index else 1
            
            label.config(bg=color, 
                        text=color,
                        fg="white" if self.is_dark_color(color) else "black",
                        borderwidth=border_width)

    def is_dark_color(self, hex_color):
        """
        Determina si un color es oscuro para elegir el color del texto
        """
        # Convertir hex a RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Calcular luminancia
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5

    def select_sv(self, event):
        # Asegurar que las coordenadas estén dentro de los límites
        x = max(0, min(event.x, self.width - 1))
        y = max(0, min(event.y, self.height - 1))
        
        self.hue = x / self.width
        self.saturation = y / self.height
        self.update_selected_color()
        self.update_monochromatic_palette()

    def select_value(self, event):
        # Asegurar que las coordenadas estén dentro de los límites
        y = max(0, min(event.y, self.height - 1))
        
        self.value = 1 - y / self.height
        self.update_sv_image()
        self.update_selected_color()
        self.update_monochromatic_palette()

    def update_sv_image(self):
        img = Image.new("RGB", (self.width, self.height))
        for x in range(self.width):
            h = x / self.width
            for y in range(self.height):
                s = y / self.height
                r, g, b = colorsys.hsv_to_rgb(h, s, self.value)
                img.putpixel((x, y), (int(r*255), int(g*255), int(b*255)))
        self.sv_photo = ImageTk.PhotoImage(img)
        self.sv_canvas.create_image(0, 0, anchor="nw", image=self.sv_photo)
        self.sv_canvas.image = self.sv_photo

    def update_selected_color(self):
        r, g, b = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
        color_hex = '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
        self.selected_color = color_hex
        self.color_label.config(text=f"Color: {color_hex}", bg=color_hex)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Color Picker con Paleta Monocromática")
    cp = ColorPicker(root)
    cp.pack()
    root.mainloop()