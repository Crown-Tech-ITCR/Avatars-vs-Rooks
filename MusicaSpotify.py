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
            scope="user-modify-playback-state user-read-playback-state",
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
    
    def info_cancion(self, track):
        """Devuelve diccionario con info de la canción"""
        return {
            "nombre": track["name"],
            "artista": track["artists"][0]["name"],
            "uri": track["uri"],
            "album": track["album"]["name"],
            "imagen": self.obtener_imagen_album(track)
        }