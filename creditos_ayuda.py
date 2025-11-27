import tkinter as tk
from tkinter import Toplevel, Frame, Label, Button
from PIL import Image, ImageTk
from Traducciones import t
import tkinter as tk
from tkinter import Toplevel, Frame, Label, Button, Canvas, Scrollbar


def show_credits(parent, colors):
    """
    Muestra una ventana emergente con la información de créditos del juego.
    Incluye el nombre, rol, descripción e imagen de cada integrante del equipo.
    """

    # Creación y configuración de la ventana de créditos
    # Se define su tamaño, color de fondo y título usando el sistema de traducción.
    ventana_creditos = Toplevel(parent)
    ventana_creditos.title(t("credits_title"))
    ventana_creditos.geometry("850x650")
    ventana_creditos.config(bg=colors[0])


    # Muestra el título "Créditos" centrado en la parte superior de la ventana.
    titulo = Label(
        ventana_creditos,
        text=t("credits_title"),
        font=("Arial Black", 16),
        fg=colors[6],
        bg=colors[0]
    )
    titulo.pack(pady=20)


    # Se crea un frame donde se ubicarán las tarjetas con la información de cada integrante.
    frame_equipo = Frame(ventana_creditos, bg=colors[0])
    frame_equipo.pack(expand=True)

    # Datos de los integrantes del equipo
    # Se define una lista de diccionarios con los datos de cada miembro:
    # nombre, rol, descripción y ruta de su foto.
    integrantes = [
        {"nombre": "Alanna Mendoza", "rol": t("credits_leader"), "descripcion": t("credits_leader"), "foto": "./images/Alanna.png"},
        {"nombre": "Fabricio Coto", "rol": t("credits_admin"), "descripcion": t("credits_member"), "foto": "./images/Fabricio.png"},
        {"nombre": "Ariel Rodriguez", "rol": t("credits_ux"), "descripcion": t("credits_member"), "foto": "./images/Ariel.png"},
        {"nombre": "Mauricio Lopez", "rol": t("credits_tester"), "descripcion": t("credits_member"), "foto": "./images/Mau.png"},
    ]

    # Creación de tarjetas por integrante
    # Cada integrante se representa como una "tarjeta" con su foto, nombre, rol y descripción.
    # Las tarjetas se distribuyen en una cuadrícula de 2 columnas.
    columnas = 2
    for i, miembro in enumerate(integrantes):
        fila = i // columnas
        columna = i % columnas

        # Se crea la tarjeta contenedora con bordes y fondo de color secundario
        card = Frame(frame_equipo, bg=colors[1], bd=2, relief="ridge", padx=10, pady=10, width=320, height=300)
        card.grid(row=fila, column=columna, padx=25, pady=25, sticky="nsew")

        # Cargar y mostrar la imagen de cada integrante
        # Si no se encuentra, se muestra un marcador de texto “[Foto]”.
        try:
            imagen = Image.open(miembro["foto"]).resize((100, 100))
            imagen = ImageTk.PhotoImage(imagen)
            img_label = Label(card, image=imagen, bg=colors[1])
            img_label.image = imagen  
            img_label.pack(pady=5)
        except:
            Label(card, text="[Foto]", fg=colors[6], bg=colors[1]).pack(pady=5)

        # Información del integrante
        # Etiquetas: nombre, rol y una breve descripción.
        Label(card, text=miembro["nombre"], font=("Arial", 12, "bold"), fg=colors[6], bg=colors[1]).pack(pady=2)
        Label(card, text=miembro["rol"], font=("Arial", 10, "italic"), fg=colors[3], bg=colors[1]).pack()
        Label(card, text=miembro["descripcion"], font=("Arial", 9), fg=colors[6], bg=colors[1], wraplength=200, justify="center").pack(pady=5)


    # Agrega un botón en la parte inferior para cerrar la ventana y volver al menú anterior.
    Button(
        ventana_creditos,
        text=t("credits_back"),
        font=("Arial Black", 11),
        bg=colors[4],
        fg=colors[6],
        activebackground=colors[3],
        activeforeground=colors[6],
        command=ventana_creditos.destroy
    ).pack(pady=10)



def show_help(parent, colors):
    """
    Crea una ventana con información de ayuda del juego.
    Incluye un scroll vertical para navegar por todas las secciones.
    """

    # Crear la ventana de ayuda
    ventana_ayuda = Toplevel(parent)
    ventana_ayuda.title(t("help_title"))  # Traducción activa
    ventana_ayuda.geometry("750x600")
    ventana_ayuda.config(bg=colors[0])


    # Título principal de la ventana
    titulo = Label(
        ventana_ayuda,
        text=t("help_title"),
        font=("Arial Black", 16),
        fg=colors[6],
        bg=colors[0]
    )
    titulo.pack(pady=20)


    # Crear un contenedor con scroll
    contenedor = Frame(ventana_ayuda, bg=colors[0])
    contenedor.pack(fill="both", expand=True, padx=20, pady=10)

    # Canvas para permitir el desplazamiento
    canvas = Canvas(contenedor, bg=colors[0], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar vertical vinculada al Canvas
    scrollbar = Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configurar el Canvas para usar el scroll
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Frame interior donde estará el contenido de texto
    frame_texto = Frame(canvas, bg=colors[0])
    canvas.create_window((0, 0), window=frame_texto, anchor="nw")


    # Secciones traducidas (mantienen el t)
    secciones = [
        {"titulo": t("help_section_login"), "texto": t("help_section_login_text")},
        {"titulo": t("help_section_register"), "texto": t("help_section_register_text")},
        {"titulo": t("help_section_forgot"), "texto": t("help_section_forgot_text")},
    ]


    # Secciones nuevas (Español)
    secciones_nuevas = [
        {
            "titulo": "🎯 Objetivo del Juego",
            "texto": (
                "Tu meta es evitar que los Avatars lleguen al extremo superior del tablero. "
                "Para lograrlo, deberás colocar Rooks (torres) que ataquen automáticamente "
                "a los enemigos que se aproximen."
            )
        },
        {
            "titulo": "🕹️Controles Básicos",
            "texto": (
                "Durante la partida podrás colocar torres en el tablero de 9 filas y 5 columnas. "
                "Cada torre tiene un costo en monedas y diferentes atributos de vida y ataque. "
                "Administra tus recursos para construir la mejor defensa posible."
            )
        },
        {
            "titulo": "⚙️ Niveles de Dificultad",
            "texto": (
                "El juego cuenta con tres niveles: Fácil, Medio y Difícil. "
                "A medida que aumente la dificultad, los Avatars serán más rápidos y resistentes. "
                "Si uno logra llegar a la parte superior, perderás la partida."
            )
        },
        {
            "titulo": "💰 Monedas y Puntos",
            "texto": (
                "Comenzarás cada partida con 350 monedas. "
                "Durante el juego, aparecerán monedas aleatorias en el tablero por un tiempo limitado. "
                "Recógelas para obtener más recursos y colocar nuevas torres."
            )
        },
        {
            "titulo": "🏰 Tipos de Rooks (Torres)",
            "texto": (
                "Las torres son tu defensa principal contra los Avatars. "
                "Cada una posee atributos únicos que determinan su efectividad:\n\n"
                "• Arena: 8 de vida, 2 de daño, cuesta 50 monedas.\n"
                "• Piedra: 12 de vida, 4 de daño, cuesta 100 monedas.\n"
                "• Fuego: 12 de vida, 8 de daño, cuesta 150 monedas.\n"
                "• Agua: 15 de vida, 10 de daño, cuesta 150 monedas.\n\n"
                "Cada torre lanza ataques en su columna para eliminar a los enemigos."
            )
        },
        {
            "titulo": "👾 Tipos de Avatars (Enemigos)",
            "texto": (
                "Los Avatars son los enemigos del juego y se mueven verticalmente hacia la parte superior del tablero. "
                "Cada tipo tiene habilidades y tiempos de ataque diferentes:\n\n"
                "• Flechador: ataca cada 2 segundos, inflige 2 puntos de daño.\n"
                "• Escudero: ataca cada 4 segundos, inflige 3 puntos de daño.\n"
                "• Leñador: ataca cada 10 segundos, inflige 9 puntos de daño.\n"
                "• Caníbal: ataca cada 12 segundos, inflige 12 puntos de daño."
            )
        },
        {
            "titulo": "🏆 Salón de la Fama",
            "texto": (
                "El Salón de la Fama muestra a los 5 jugadores con los puntajes más altos. "
                "Supera tus propias marcas y compite para alcanzar los primeros lugares del ranking."
            )
        }
    ]

    # Combinar todas las secciones
    secciones.extend(secciones_nuevas)


    # Mostrar cada sección en orden
    for sec in secciones:
        Label(
            frame_texto,
            text=sec["titulo"],
            font=("Arial Black", 12),
            fg=colors[3],
            bg=colors[0],
            anchor="w",
            justify="left"
        ).pack(anchor="w", pady=(10, 0))
        Label(
            frame_texto,
            text=sec["texto"],
            font=("Arial", 10),
            fg=colors[6],
            bg=colors[0],
            wraplength=650,
            justify="left"
        ).pack(anchor="w", pady=(0, 10))

    # Separador visual
    Label(
        frame_texto,
        text="─" * 80,
        fg=colors[3],
        bg=colors[0],
        font=("Arial", 8)
    ).pack(anchor="w", pady=15)

    # Frame para sección adicional destacada
    frame_seccion_adicional = Frame(
        frame_texto,
        bg=colors[0],
        bd=2,
        relief="ridge",
        padx=15,
        pady=15
    )
    frame_seccion_adicional.pack(anchor="w", fill="x", pady=10)

    # Título de la sección adicional
    Label(
        frame_seccion_adicional,
        text="ℹ️ Funciones del control",
        font=("Arial Black", 12),
        fg=colors[3],
        bg=colors[0],
        anchor="w",
        justify="left"
    ).pack(anchor="w", pady=(0, 10))
    
    # Crear un frame interno para el contenido con scroll
    frame_contenido = Frame(frame_seccion_adicional, bg=colors[0])
    frame_contenido.pack(anchor="w", fill="both", expand=True)
    
    # Lista de secciones dentro del marco
    secciones_control = [
        {
            "titulo": "🎮 Uso general del control:",
            "puntos": [
                "El control no funciona en el menú ni fuera de los niveles.",
                "Solo dentro del juego podrás mover el cursor y colocar torres."
            ]
        },
        {
            "titulo": "🕹️ Movimiento:",
            "puntos": [
                "Usa el joystick para moverte entre las casillas donde puedes construir torres."
            ]
        },
        {
            "titulo": "🏰 Colocación de Torres:",
            "subtitulo": "Los botones de colores colocan una torre diferente en la casilla seleccionada:",
            "puntos": [
                "🔵 Botón Azul → Torre de Fuego",
                "🟢 Botón Verde → Torre de Roca",
                "🟡 Botón Amarillo → Torre de Arena",
                "🟠 Botón Anaranjado → Torre de Agua"
            ]
        },
        {
            "titulo": "💰 Funciones Centrales:",
            "puntos": [
                "⬅️ Botón central amarillo izquierdo → Recoger monedas en la casilla",
                "➡️ Botón central blanco derecho → Pausar / Reanudar la partida"
            ]
        }
    ]
    
    # Mostrar cada sección
    for sec in secciones_control:
        Label(
            frame_contenido,
            text=sec["titulo"],
            font=("Arial", 10, "bold"),
            fg=colors[3],
            bg=colors[0],
            anchor="w",
            justify="left"
        ).pack(anchor="w", pady=(5, 2))
        
        if "subtitulo" in sec:
            Label(
                frame_contenido,
                text=sec["subtitulo"],
                font=("Arial", 10),
                fg=colors[6],
                bg=colors[0],
                wraplength=600,
                anchor="w",
                justify="left"
            ).pack(anchor="w", pady=(0, 3))
        
        for punto in sec["puntos"]:
            Label(
                frame_contenido,
                text="• " + punto,
                font=("Arial", 10),
                fg=colors[6],
                bg=colors[0],
                wraplength=580,
                anchor="w",
                justify="left"
            ).pack(anchor="w", pady=1)
        
        Label(
            frame_contenido,
            text="",
            bg=colors[0]
        ).pack(pady=3)
    
    # Conclusión
    Label(
        frame_contenido,
        text="Estas funciones son todo lo que necesitas para jugar de manera sencilla y rápida.",
        font=("Arial", 10),
        fg=colors[6],
        bg=colors[0],
        wraplength=600,
        justify="left"
    ).pack(anchor="w", pady=(5, 0))


    # Botón para cerrar la ventana
    Button(
        ventana_ayuda,
        text=t("help_back"),
        font=("Arial Black", 11),
        bg=colors[4],
        fg=colors[6],
        activebackground=colors[3],
        activeforeground=colors[6],
        command=ventana_ayuda.destroy
    ).pack(pady=10)


    # Permitir desplazamiento con la rueda del mouse
    def on_mousewheel(event):
        try:
            # Verificar si el canvas aún existe y está válido
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            # Si el widget ya no existe, no hacer nada
            pass

    ventana_ayuda.bind_all("<MouseWheel>", on_mousewheel)
