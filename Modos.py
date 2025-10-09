# theme_manager.py
from colorsys import rgb_to_hls, hls_to_rgb

def adjust_brightness(hex_color, factor=0.7):
    """
    Ajusta el brillo de un color hex.
    factor < 1.0 => más oscuro
    factor > 1.0 => más claro
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = rgb_to_hls(r / 255, g / 255, b / 255)
    l = max(0, min(1, l * factor))
    r, g, b = hls_to_rgb(h, l, s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def apply_dark_mode(app):
    """
    Aplica un modo oscuro reduciendo el brillo de los colores actuales.
    """
    app.colors = [adjust_brightness(c, 0.6) for c in app.colors]
    app.c1, app.c2, app.c3, app.c4, app.c5, app.c6, app.c7 = app.colors

    app.root.configure(bg=app.colors[0])
    app.show_login_window()  # Recrea la interfaz con nuevos colores

def apply_light_mode(app):
    """
    Restaura los colores originales (modo claro).
    """
    app.colors = [
        "#000000", "#1a1a1a", "#535353", "#cc0000",
        "#990000", "#FFFFFF", "#CCCCCC"
    ]
    app.c1, app.c2, app.c3, app.c4, app.c5, app.c6, app.c7 = app.colors

    app.root.configure(bg=app.colors[0])
    app.show_login_window()
