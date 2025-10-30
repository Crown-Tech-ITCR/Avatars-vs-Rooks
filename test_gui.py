import tkinter as tk

def test_gui():
    root = tk.Tk()
    root.title("Test GUI")
    root.geometry("400x300")
    root.configure(bg="white")
    
    label = tk.Label(root, text="¡Hola! Esta es una prueba", bg="white", fg="black", font=("Arial", 16))
    label.pack(pady=50)
    
    button = tk.Button(root, text="Botón de prueba", bg="lightblue", fg="black")
    button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_gui()