import tweepy
from datetime import datetime


API_KEY = "DwXL4rux9O7NuujUm9BI8TEon"
API_SECRET = "UVHRvf6DnNz9DgaxFHW4KrWmOTP9qxJDI78tSQHX7QfxM4gMVq"
ACCESS_TOKEN = "1988830856027447296-ruQcu4i2vPAeOamHIEGjQcTSl3akKA"
ACCESS_SECRET = "Vs2fgWb4W11wya1QSXfLHOX79EBBolEHjJhH5s9Ci4ARR"

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

def publicar_top_salon_fama(nivel, top3_data, nombres_descifrados):
    """
    Publica un tweet con el top 3 del Salón de la Fama para un nivel específico.
    """
    try:
        # Mapear números de nivel a nombres descriptivos
        nombres_nivel = {1: "Fácil", 2: "Medio", 3: "Difícil"}
        nivel_nombre = nombres_nivel.get(nivel, "Desconocido")
        
        # Validar que hay datos para publicar
        if not top3_data or len(top3_data) == 0:
            print(f"No hay datos para publicar en el nivel {nivel_nombre}")
            return False
        
        # Construir el contenido del tweet
        emojis_medalla = ["🥇", "🥈", "🥉"]
        
        tweet_content = f"🎮 Nuevo TOP 3 - Salón de la Fama 🎮\n"
        tweet_content += f"Nivel: {nivel_nombre}\n"
        tweet_content += f"\n"
        
        # Agregar cada miembro del top 3
        for idx, (username_enc, puntaje, fecha, tempo, popularidad) in enumerate(top3_data):
            username_display = nombres_descifrados.get(username_enc, "Usuario desconocido")
            emoji = emojis_medalla[idx] if idx < len(emojis_medalla) else "⭐"
            tweet_content += f"{emoji} #{idx+1}: {username_display}\n"
            tweet_content += f"   Puntos: {puntaje:.1f}\n"
        
        tweet_content += f"\n¡Únete al juego Avatars vs Rooks! 🎯"
        
        # Añadir timestamp para evitar duplicados de X/Twitter
        timestamp = datetime.now().strftime("%H:%M:%S")
        tweet_content += f"\n\n⏰ {timestamp}"
        
        # Enviar el tweet
        resp = client.create_tweet(text=tweet_content)
        print(f"✓ Tweet enviado correctamente para el nivel {nivel_nombre}. ID: {resp.data['id']}")
        return True
        
    except tweepy.TweepyException as e:
        print(f"✗ Error de Tweepy al publicar tweet: {e}")
        return False
    except Exception as e:
        print(f"✗ Error al publicar tweet del Salón de la Fama: {e}")
        return False
