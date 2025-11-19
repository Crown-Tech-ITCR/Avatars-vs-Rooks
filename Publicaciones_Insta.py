import os
import requests
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

ACCESS_TOKEN_IG = os.environ.get("ACCESS_TOKEN_IG", "EAApuKKqS4fUBPyzis1IJZABfn0vzDMZClvaUKdR5KC8zsZC6k9TTZAQMn0APg6GaY5ZCQHQGhXgq3YzHKwU6zzJyPjFy5FveH6soI4eEL3pbcbBUQZAClESfobUd6ceCF3xtaE1lVLWN5kFKHC9H5JvoJtSsDy2dtqNI3wiREKMY0KauyIAN1F3f2cRRWzr6gP")
IG_USER_ID = os.environ.get("IG_USER_ID", "17841478466089347")

GRAPH_API_VERSION = os.environ.get("FB_GRAPH_API_VERSION", "v19.0")


def _crear_contenedor_media(image_url: str, caption: str) -> Dict[str, Any]:
    """Crea un contenedor de media en Instagram"""
    url_media = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{IG_USER_ID}/media"
    data = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN_IG,
    }

    r = requests.post(url_media, data=data, timeout=15)
    try:
        return r.json()
    except Exception:
        return {"error": "invalid_response", "raw": r.text}


def _publicar_contenedor(creation_id: str) -> Dict[str, Any]:
    """Publica el contenedor creado en el feed de Instagram."""
    url_publish = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{IG_USER_ID}/media_publish"
    data = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN_IG,
    }
    r = requests.post(url_publish, data=data, timeout=15)
    try:
        return r.json()
    except Exception:
        return {"error": "invalid_response", "raw": r.text}


def publicar_top_salon_instagram(
    nivel: int,
    top_actual: List[Tuple[str, float, Any, Any, Any]],
    nombres_descifrados: Optional[Dict[str, str]] = None,
    image_url: Optional[str] = None,
    caption_template: Optional[str] = None,
) -> Dict[str, Any]:
    """Publica el top del salón de la fama en Instagram.
    Se utiliza un url de una imagen publicada en la pagina de Facebook creada para que esta imagen se publique en todos los mensajes de instagram.

    """
    if nombres_descifrados is None:
        nombres_descifrados = {}

    # Generar caption decorado igual que X/Twitter si no se proporcionó
    if not caption_template:

        nombres_nivel = {1: "Fácil", 2: "Medio", 3: "Difícil"}
        nivel_nombre = nombres_nivel.get(nivel, "Desconocido")
        emojis_medalla = ["🥇", "🥈", "🥉"]
        caption = f"🎮 Nuevo TOP 3 - Salón de la Fama 🎮\n"
        caption += f"Nivel: {nivel_nombre}\n\n"
        for idx, (username_enc, puntaje, fecha, tempo, popularidad) in enumerate(top_actual):
            username_display = nombres_descifrados.get(username_enc, "Usuario desconocido")
            emoji = emojis_medalla[idx] if idx < len(emojis_medalla) else "⭐"
            caption += f"{emoji} #{idx+1}: {username_display}\n"
            caption += f"   Puntos: {puntaje:.1f}\n"
        caption += f"\n¡Únete al juego Avatars vs Rooks! 🎯"
        timestamp = datetime.now().strftime("%H:%M:%S")
        caption += f"\n\n⏰ {timestamp}"
    else:
        caption = caption_template

    if not image_url:
        # URL de ejemplo; idealmente proporcione una URL pública propia
        image_url = os.environ.get(
            "IMAGE_PUBLIC_URL",
            "https://scontent.fsjo6-1.fna.fbcdn.net/v/t39.30808-6/579218483_1177892667830859_350385537043235397_n.jpg?stp=dst-jpg_p526x296_tt6&_nc_cat=107&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=9auYg_Sg9asQ7kNvwE98-bm&_nc_oc=AdkNp-59VVARr5Ih-aMbBEWxPFjjanzP6Pf5EBXTF4OelDjJeqBc3tRo4DKbEOVKrZ8&_nc_zt=23&_nc_ht=scontent.fsjo6-1.fna&_nc_gid=1Ad0vrIzDd70XHPv-MRZsQ&oh=00_AfhWnGKn3-vhoAPtG7j4Ytp38JaO3ESlavMbp5jwDD8vAQ&oe=692309B7",
        )

    if not ACCESS_TOKEN_IG or not IG_USER_ID:
        return {"error": "missing_credentials", "message": "ACCESS_TOKEN_IG o IG_USER_ID no configurados."}

    try:
        media_resp = _crear_contenedor_media(image_url=image_url, caption=caption)
        if "id" not in media_resp:
            return {"error": "create_media_failed", "response": media_resp}

        creation_id = media_resp["id"]
        publish_resp = _publicar_contenedor(creation_id=creation_id)
        return {"create": media_resp, "publish": publish_resp}
    except requests.RequestException as e:
        return {"error": "request_exception", "message": str(e)}


if __name__ == "__main__":
    print("Ejecutando prueba ")
    resp = publicar_top_salon_instagram(1, [("dummy_enc", 123.45)], {"dummy_enc": "usuario_prueba"})
    print(resp)
