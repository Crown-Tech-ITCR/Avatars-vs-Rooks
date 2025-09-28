import tkinter as tk
from Login import LoginAvatarsRooks

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginAvatarsRooks(root)
    # si hubo un login exitoso 
    def on_login_success(username):
        login_app.login_frame.pack_forget() 
        global app
        app = root
    login_app.on_login_success = on_login_success # Asignamos la función de callback al login
    
    root.mainloop()