import tkinter as tk
from tkinter import Canvas, Label
from PIL import Image, ImageTk
import colorsys

class ColorPicker(tk.Frame):
    def __init__(self, master=None, width=256, height=256, bar_width=28):
        super().__init__(master)
        self.width = width
        self.height = height
        self.bar_width = bar_width
        self.selected_color = "#FFFFFF"
        
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

    def select_sv(self, event):
        # Asegurar que las coordenadas estén dentro de los límites
        x = max(0, min(event.x, self.width - 1))
        y = max(0, min(event.y, self.height - 1))
        
        self.hue = x / self.width
        self.saturation = y / self.height
        self.update_selected_color()

    def select_value(self, event):
        # Asegurar que las coordenadas estén dentro de los límites
        y = max(0, min(event.y, self.height - 1))
        
        self.value = 1 - y / self.height
        self.update_sv_image()
        self.update_selected_color()

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
    root.title("Color Picker")
    cp = ColorPicker(root)
    cp.pack()
    root.mainloop()