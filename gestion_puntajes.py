import json
import os
from datetime import datetime

PUNTAJES_FILE = "puntajes.txt"

def load_puntajes():
    """Carga todos los puntajes del archivo"""
    if not os.path.exists(PUNTAJES_FILE):
        return {}
    
    if os.path.getsize(PUNTAJES_FILE) == 0:
        return {}
    
    try:
        with open(PUNTAJES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(" Archivo puntajes.txt corrupto, creando uno nuevo...")
        return {}

def save_puntajes(puntajes):
    """Guarda todos los puntajes en el archivo"""
    with open(PUNTAJES_FILE, "w", encoding="utf-8") as f:
        json.dump(puntajes, f, ensure_ascii=False, indent=4)

def agregar_puntaje(username_enc, nivel, puntaje, tempo, popularidad):
    """Agrega un nuevo puntaje para un usuario SOLO SI ES UN NUEVO RÉCORD en ese nivel"""
    puntajes = load_puntajes()
    
    # Crear entrada para el usuario si no existe
    if username_enc not in puntajes:
        puntajes[username_enc] = []
    
    # Obtener el mejor puntaje anterior del usuario en este nivel
    puntajes_nivel = [r for r in puntajes[username_enc] if r["nivel"] == nivel]
    
    # Si ya tiene puntajes en este nivel, verificar si el nuevo es mejor
    if puntajes_nivel:
        mejor_anterior = max(puntajes_nivel, key=lambda x: x["puntaje"])
        # Si el nuevo puntaje no es mejor que el anterior, no agregarlo
        if puntaje <= mejor_anterior["puntaje"]:
            print(f"Puntaje no agregado: {puntaje:.2f} no es mejor que el récord de {mejor_anterior['puntaje']:.2f}")
            return False
    
    # Crear nuevo registro de puntaje
    nuevo_puntaje = {
        "nivel": nivel,
        "puntaje": round(puntaje, 2),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tempo": tempo,
        "popularidad": popularidad
    }
    
    puntajes[username_enc].append(nuevo_puntaje)
    
    # Guardar cambios
    save_puntajes(puntajes)
    print(f"Puntaje guardado: Nivel {nivel}, Puntos {puntaje:.2f}")
    return True

def obtener_top_nivel(nivel, limit=3):
    """Obtiene el top N de jugadores para un nivel específico
    
    Retorna lista de tuplas: [(username_enc, puntaje_max, fecha, tempo, popularidad), ...]
    """
    puntajes = load_puntajes()
    
    # Diccionario para almacenar el mejor puntaje de cada usuario por nivel
    mejores_por_usuario = {}
    
    for username_enc, registros in puntajes.items():
        # Filtrar solo los puntajes del nivel solicitado
        puntajes_nivel = [r for r in registros if r["nivel"] == nivel]
        
        if puntajes_nivel:
            # Obtener el mejor puntaje de este usuario en este nivel
            mejor = max(puntajes_nivel, key=lambda x: x["puntaje"])
            mejores_por_usuario[username_enc] = mejor
    
    # Ordenar por puntaje descendente y tomar los top N
    ranking = sorted(
        mejores_por_usuario.items(),
        key=lambda x: x[1]["puntaje"],
        reverse=True
    )[:limit]
    
    # Formatear resultado
    resultado = [
        (
            username_enc,
            registro["puntaje"],
            registro["fecha"],
            registro["tempo"],
            registro["popularidad"]
        )
        for username_enc, registro in ranking
    ]
    
    return resultado

def obtener_posicion_usuario(username_enc, nivel):
    """Obtiene la posición exacta de un usuario en el ranking de un nivel
    
    Retorna: posicion (int) - 0 si no existe en el ranking, o su posición (1, 2, 3, ...)
    """
    puntajes = load_puntajes()
    
    # Diccionario para almacenar el mejor puntaje de cada usuario por nivel
    mejores_por_usuario = {}
    
    for user_enc, registros in puntajes.items():
        # Filtrar solo los puntajes del nivel solicitado
        puntajes_nivel = [r for r in registros if r["nivel"] == nivel]
        
        if puntajes_nivel:
            # Obtener el mejor puntaje de este usuario en este nivel
            mejor = max(puntajes_nivel, key=lambda x: x["puntaje"])
            mejores_por_usuario[user_enc] = mejor
    
    # Ordenar por puntaje descendente
    ranking_completo = sorted(
        mejores_por_usuario.items(),
        key=lambda x: x[1]["puntaje"],
        reverse=True
    )
    
    # Buscar la posición del usuario
    for posicion, (user_enc, _) in enumerate(ranking_completo, 1):
        if user_enc == username_enc:
            return posicion
    
    return 0  # Usuario no está en el ranking

def obtener_puntajes_usuario(username_enc, nivel=None):
    """Obtiene todos los puntajes de un usuario, opcionalmente filtrados por nivel"""
    puntajes = load_puntajes()
    
    if username_enc not in puntajes:
        return []
    
    registros = puntajes[username_enc]
    
    if nivel is not None:
        registros = [r for r in registros if r["nivel"] == nivel]
    
    # Ordenar por puntaje descendente
    return sorted(registros, key=lambda x: x["puntaje"], reverse=True)

def obtener_mejor_puntaje_usuario(username_enc, nivel):
    """Obtiene el mejor puntaje de un usuario en un nivel específico"""
    puntajes = load_puntajes()
    
    if username_enc not in puntajes:
        return None
    
    puntajes_nivel = [r for r in puntajes[username_enc] if r["nivel"] == nivel]
    
    if not puntajes_nivel:
        return None
    
    # Retornar el mejor puntaje
    mejor = max(puntajes_nivel, key=lambda x: x["puntaje"])
    return mejor["puntaje"]