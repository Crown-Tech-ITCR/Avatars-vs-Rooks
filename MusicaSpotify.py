import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from io import BytesIO
from PIL import Image

class SpotifyManager:
    def __init__(self):
        """Inicializa el cliente de Spotify"""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="2de5ecec2cb946d09781ac83e97947cf",
            client_secret="90700ec3fc7c482ebf80914786e84abe",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-modify-playback-state user-read-playback-state user-read-recently-played",
            cache_path=".cache"
        ))
        self.dispositivo_pc = None
        self.cancion_actual = None
    
    def _obtener_dispositivo_pc(self):
        """Obtiene el ID del dispositivo Computer"""
        if self.dispositivo_pc:
            return self.dispositivo_pc
        
        dispositivos = self.sp.devices()["devices"]
        for device in dispositivos:
            if device['type'] == 'Computer':
                self.dispositivo_pc = device['id']
                return self.dispositivo_pc
        return None
    
    def buscar_canciones(self, query, limit=3):
        """Busca los primeros resultados de canciones"""
        resultados = self.sp.search(q=query, type="track", limit=limit)["tracks"]["items"]
        return resultados
    
    def reproducir_cancion(self, track_uri):
        """Reproduce la canción en repeat"""
        device_id = self._obtener_dispositivo_pc()
        
        if not device_id:
            return False
            
        
        self.sp.start_playback(device_id=device_id, uris=[track_uri])
        self.sp.repeat("track", device_id=device_id)
        self.cancion_actual = track_uri
        return True
    
    def cambiar_cancion(self, track_uri):
        """Cambia a una nueva canción manteniendo el repeat"""
        return self.reproducir_cancion(track_uri)
    
    def pausar_musica(self):
        """Pausa la reproducción"""
        self.sp.pause_playback()
    
    def reanudar_musica(self):
        """Reanuda la reproducción"""
        device_id = self._obtener_dispositivo_pc()
        if device_id:
            self.sp.start_playback(device_id=device_id)
    
    def detener_musica(self):
        """Detiene la música y desactiva repeat"""
        self.sp.pause_playback()
        device_id = self._obtener_dispositivo_pc()
        if device_id:
            self.sp.repeat("off", device_id=device_id)
        self.cancion_actual = None
    
    def obtener_imagen_album(self, track):
        """Devuelve la imagen del álbum"""
        album = track["album"]
        imagen_url = album["images"][0]["url"]
        response = requests.get(imagen_url)
        img = Image.open(BytesIO(response.content))
        return img
    
    def obtener_tempo(self, track_id):
        """Obtiene el tempo usando análisis del track completo"""
        try:
            if track_id.startswith('spotify:track:'):
                track_id = track_id.split(':')[2]
            
            # Método de estimación basado en género y características
            track_info = self.sp.track(track_id)
            popularidad = track_info['popularity']
            duracion_ms = track_info['duration_ms']
            duracion_min = duracion_ms / 60000
            
            # Obtener género del artista
            artist_id = track_info['artists'][0]['id']
            artist_info = self.sp.artist(artist_id)
            genres = artist_info.get('genres', [])
            
            # Tempo base según género
            tempo_base = 120
            genre_str = ' '.join(genres).lower()
            
            if any(g in genre_str for g in ['edm', 'electronic', 'dance', 'house']):
                tempo_base = 128
            elif any(g in genre_str for g in ['hip hop', 'rap', 'trap']):
                tempo_base = 140
            elif any(g in genre_str for g in ['pop', 'latin']):
                tempo_base = 120
            elif any(g in genre_str for g in ['rock', 'metal']):
                tempo_base = 130
            elif any(g in genre_str for g in ['reggaeton', 'dembow']):
                tempo_base = 95
            
            # Ajustes por duración
            if duracion_min < 2.5:
                tempo_base += 10
            elif duracion_min > 5:
                tempo_base -= 10
            
            # Ajuste por popularidad (hits comerciales)
            if popularidad > 70:
                tempo_base = (tempo_base + 125) / 2
            
            tempo_estimado = round(tempo_base, 2)
            return max(70, min(170, tempo_estimado))
            
        except Exception as e:
            return 120.0
        
    def obtener_popularidad(self, track_id):
        """Obtiene la popularidad de una canción (0-100). Retorna 20 como valor por defecto."""
        try: 
            if track_id.startswith('spotify:track:'):
                track_id = track_id.split(':')[2]
            
            track_info = self.sp.track(track_id)
            
            if track_info and 'popularity' in track_info:
                popularidad = track_info['popularity']
                # Validar que sea un número válido
                if isinstance(popularidad, (int, float)) and 0 <= popularidad <= 100:
                    return popularidad
            
            # Si no hay datos válidos, retornar valor por defecto
            return 20
            
        except Exception as e:
            return 20
    
    def info_cancion(self, track):
        """Devuelve diccionario con info de la canción"""
        return {
            "nombre": track["name"],
            "artista": track["artists"][0]["name"],
            "uri": track["uri"],
            "album": track["album"]["name"],
            "imagen": self.obtener_imagen_album(track)
        }