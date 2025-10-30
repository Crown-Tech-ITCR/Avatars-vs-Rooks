class Entidad:
    """Clase base para todas las entidades del juego (rooks, avatars, etc.)."""
    def __init__(self, tipo: str, vida: int = 10, dano: int = 1, movil: bool = False):
        self.tipo = tipo
        self.vida = vida
        self.dano = dano
        self.posicion = None  # (fila, col)
        self.movil = movil

        #Atributos de animacion suave
        self.x_visual = 0  # Posición X en píxeles para dibujo
        self.y_visual = 0  # Posición Y en píxeles para dibujo
        self.animando = False  # ¿Está en medio de una animación?
        self.origen_x = 0  # Punto de inicio de la animación
        self.origen_y = 0
        self.destino_x = 0  # Punto final de la animación
        self.destino_y = 0
        self.progreso_animacion = 0.0  # Progreso de 0.0 a 1.0
        self.duracion_animacion = 900  # Duración en milisegundos 


    def set_pos(self, fila, col):
        """Establece la posición de la entidad e inicia animación suave."""
        from game_logic import TAM_CASILLA
        
        # Si es la primera vez que se posiciona (spawn/creación)
        if self.posicion is None:
            self.posicion = (fila, col)
            # Calcular posición visual inicial (centro de la casilla)
            self.x_visual = col * TAM_CASILLA + TAM_CASILLA // 2
            self.y_visual = fila * TAM_CASILLA + TAM_CASILLA // 2
            self.animando = False
        else:
            # Ya tiene una posición previa, entonces iniciar animación
            
            # Guardar origen (posición visual ACTUAL)
            self.origen_x = self.x_visual
            self.origen_y = self.y_visual
            
            # Calcular destino (nueva posición en píxeles)
            self.destino_x = col * TAM_CASILLA + TAM_CASILLA // 2
            self.destino_y = fila * TAM_CASILLA + TAM_CASILLA // 2
            
            # Iniciar animación
            self.animando = True
            self.progreso_animacion = 0.0
            
            #Actualizar posicion logica
            self.posicion = (fila, col)

    def take_damage(self, cantidad: int):
        """Aplica daño a la entidad y la elimina de la matriz si muere."""
        self.vida -= cantidad
        if self.vida <= 0:
            if self.posicion is not None:
                f, c = self.posicion
                # Importación local para evitar dependencia circular
                from game_logic import get_matriz_juego
                matriz_juego = get_matriz_juego()
                if self in matriz_juego[f][c]:
                    matriz_juego[f][c].remove(self)
                self.posicion = None

    def tick(self):
        """Método llamado en cada actualización del juego."""
        pass

    def actualizar_animacion_movimiento(self, delta_ms):
        """Actualiza la animación de movimiento suave."""
        if not self.animando:
            return
        
        # Calcular cuánto avanzar en la animación
        incremento = delta_ms / self.duracion_animacion
        self.progreso_animacion += incremento
        
        if self.progreso_animacion >= 1.0:
            # Animación completada
            self.progreso_animacion = 1.0
            self.x_visual = self.destino_x
            self.y_visual = self.destino_y
            self.animando = False
        else:
            # Interpolar posición (movimiento suave)
            self.x_visual = self.lerp(self.origen_x, self.destino_x, self.progreso_animacion)
            self.y_visual = self.lerp(self.origen_y, self.destino_y, self.progreso_animacion)
    
    def lerp(self, inicio, fin, t):
        """Interpolación lineal entre dos valores."""
        return inicio + (fin - inicio) * t

# CLASES DE ROOKS
class Rook(Entidad):
    """Rook base: no se desplaza, puede disparar si su cooldown está a cero."""
    def __init__(self, vida: int = 10, dano: int = 10, shot_cooldown_max: int = 0, costo: int = 0):
        super().__init__("rook", vida=vida, dano=dano, movil=False)
        self.shot_cooldown = 0
        self.shot_cooldown_max = shot_cooldown_max if shot_cooldown_max > 0 else 10
        self.costo = costo
        self.color = "green"

    def can_shoot(self) -> bool:
        """Verifica si el rook puede disparar."""
        return self.shot_cooldown == 0

    def shoot(self):
        """Dispara una rafaga y reinicia el cooldown."""
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano)

    def tick(self):
        """Actualiza el cooldown del rook."""
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1



# TIPOS ESPECÍFICOS DE ROOKS

class RookRoca(Rook):
    """Rook de Roca: Resistente pero daño moderado."""
    def __init__(self):
        super().__init__(vida=12, dano=6, shot_cooldown_max=12, costo=100)
        self.tipo = "rook_roca"
        self.color = "gray"

    def shoot(self): 
        """Dispara una rafaga de roca y reinicia el cooldown."""
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano, tipo_rafaga="roca")


class RookFuego(Rook):
    """Rook de Fuego: Buen daño y resistencia equilibrada."""
    def __init__(self):
        super().__init__(vida=14, dano=10, shot_cooldown_max=15, costo=125)
        self.tipo = "rook_fuego"
        self.color = "orange"

    def shoot(self): 
        """Dispara una rafaga de roca y reinicia el cooldown."""
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano, tipo_rafaga="fuego")


class RookAgua(Rook):
    """Rook de Agua: Alta resistencia y alto daño."""
    def __init__(self):
        super().__init__(vida=15, dano=17, shot_cooldown_max=17, costo=150)
        self.tipo = "rook_agua"
        self.color = "cyan"

    def shoot(self): 
        """Dispara una rafaga de roca y reinicia el cooldown."""
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano, tipo_rafaga="agua")


class RookArena(Rook):
    """Rook de Arena: Barato pero frágil y poco daño."""
    def __init__(self):
        super().__init__(vida=8, dano=4, shot_cooldown_max=9, costo=50)
        self.tipo = "rook_arena"
        self.color = "yellow"

    def shoot(self): 
        """Dispara una rafaga de roca y reinicia el cooldown."""
        self.shot_cooldown = self.shot_cooldown_max
        return Rafaga(self.dano, tipo_rafaga="arena")


# CLASES DE AVATARS
# CLASES DE AVATARS
class Avatar(Entidad):
    """Avatar base: se mueve y puede atacar rooks."""
    def __init__(self, vida: int = 10, dano: int = 10, regeneracion: int = 0, move_cooldown_max: int = 3, 
                 ataque_a_distancia: bool = False, shot_cooldown_max: int = 3):
        super().__init__("avatar", vida=vida, dano=dano, movil=True)
        self.regeneracion = regeneracion
        self.move_cooldown_max = move_cooldown_max
        self.move_cooldown = 0  # Cooldown actual para movimiento
        
        # Sistema de ataque a distancia
        self.ataque_a_distancia = ataque_a_distancia
        self.shot_cooldown = 0
        self.shot_cooldown_max = shot_cooldown_max

        # Sistema de animación
        self.frame_actual = 1
        self.contador_frames = 0
        self.frames_por_cambio = 6

    def can_move(self) -> bool:
        """Verifica si el avatar puede moverse."""
        return self.move_cooldown == 0

    def can_shoot(self) -> bool:
        """Verifica si el avatar puede disparar."""
        return self.shot_cooldown == 0 and self.ataque_a_distancia

    def shoot(self):
        """Dispara un proyectil y reinicia el cooldown."""
        if self.can_shoot():
            self.shot_cooldown = self.shot_cooldown_max
            return ProyectilAvatar(self.dano)
        return None

    def hay_rooks_en_camino(self, matriz_juego, mi_fila, mi_columna):
        """Verifica si hay rooks en el camino hacia arriba."""
        for f in range(mi_fila - 1, -1, -1):
            rooks_en_fila = [r for r in matriz_juego[f][mi_columna] if isinstance(r, Rook)]
            if rooks_en_fila:
                return True
        return False
    
    def hay_rooks_adelante(self, matriz_juego, mi_fila, mi_columna):
        """Verifica si hay rooks en TODA la columna hacia arriba (para avatars a distancia)."""
        for f in range(mi_fila - 1, -1, -1):
            rooks_en_fila = [r for r in matriz_juego[f][mi_columna] if isinstance(r, Rook)]
            if rooks_en_fila:
                return True  # Hay al menos un rook adelante
        return False  # No hay rooks en toda la columna hacia arriba

    def move_tick(self):
        """Actualiza el cooldown de movimiento."""
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

    def reset_move_cooldown(self):
        """Reinicia el cooldown de movimiento después de moverse."""
        self.move_cooldown = self.move_cooldown_max

    def attack(self, objetivo):
        """Ataca a un objetivo si puede recibir daño."""
        if hasattr(objetivo, "take_damage"):
            objetivo.take_damage(self.dano)

    def tick(self):
        self.move_tick()
        # Actualizar cooldown de disparo
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

    def actualizar_animacion(self):
        """Actualiza el frame de animación del avatar de forma recursiva"""
        self.contador_frames += 1
        
        # Solo cambiar frame cada tantas updates
        if self.contador_frames >= self.frames_por_cambio:
            self.contador_frames = 0
            
            # Cambiar al siguiente frame
            self.frame_actual += 1
            if self.frame_actual > 3:
                self.frame_actual = 1
        
        return self.frame_actual

    def get_imagen_path(self):
        """Retorna el path de la imagen actual según el frame de animación"""
        return f"./images/avatars/{self.tipo}_{self.frame_actual}.png"

# TIPOS ESPECÍFICOS DE AVATARS
# Velocidades: Flechador (más lento) -> Escudero -> Leñador -> Caníbal (más rápido)

class AvatarFlechador(Avatar):
    """Avatar Flechador: Ataca a distancia, más lento, poco daño pero se regenera."""
    def __init__(self):
        super().__init__(vida=8, dano=2, regeneracion=2, move_cooldown_max=6, 
                        ataque_a_distancia=True, shot_cooldown_max=12)  # Dispara cada 4 ticks
        self.tipo = "avatar_flechador"
        self.color = "orange"

    def shoot(self):  
        """Dispara un proyectil de flechador y reinicia el cooldown."""
        if self.can_shoot():
            self.shot_cooldown = self.shot_cooldown_max
            return ProyectilAvatar(self.dano, tipo_proyectil="flechador")
        return None


class AvatarEscudero(Avatar):
    """Avatar Escudero: Ataca a distancia, velocidad media-lenta con regeneración moderada."""
    def __init__(self):
        super().__init__(vida=12, dano=3, regeneracion=1, move_cooldown_max=5, 
                        ataque_a_distancia=True, shot_cooldown_max=10)  # Dispara cada 3 ticks
        self.tipo = "avatar_escudero"
        self.color = "blue"

    def shoot(self):  
        """Dispara un proyectil de flechador y reinicia el cooldown."""
        if self.can_shoot():
            self.shot_cooldown = self.shot_cooldown_max
            return ProyectilAvatar(self.dano, tipo_proyectil="escudero")
        return None


class AvatarLenador(Avatar):
    """Avatar Leñador: Ataque cuerpo a cuerpo, velocidad media-rápida, alto daño sin regeneración."""
    def __init__(self):
        super().__init__(vida=20, dano=9, regeneracion=0, move_cooldown_max=4, 
                        ataque_a_distancia=False)  # Solo cuerpo a cuerpo
        self.tipo = "avatar_lenador"
        self.color = "sienna"


class AvatarCanibal(Avatar):
    """Avatar Caníbal: Ataque cuerpo a cuerpo, más rápido, alto daño y regeneración alta."""
    def __init__(self):
        super().__init__(vida=22, dano=12, regeneracion=4, move_cooldown_max=4, 
                        ataque_a_distancia=False)  # Solo cuerpo a cuerpo
        self.tipo = "avatar_canibal"
        self.color = "red"

# CLASE PROYECTIL DE AVATAR
class ProyectilAvatar:
    """Proyectil disparado por los avatars."""
    def __init__(self, dano: int = 3, tipo_proyectil: str = "flechador"):
        self.tipo = "proyectil_avatar"
        self.tipo_proyectil = tipo_proyectil
        self.dano = dano
        self.posicion = None
        self.move_cooldown = 0
        self.move_cooldown_max = 3  # Velocidad media

        #Atributos para animacion
        self.x_visual = 0
        self.y_visual = 0
        self.animando = False
        self.origen_x = 0
        self.origen_y = 0
        self.destino_x = 0
        self.destino_y = 0
        self.progreso_animacion = 0.0
        self.duracion_animacion = 800  # Proyectiles muy rápidos 

    def can_move(self) -> bool:
        """Verifica si el proyectil puede moverse."""
        return self.move_cooldown == 0

    def move_tick(self):
        """Actualiza el cooldown de movimiento."""
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

    def reset_move_cooldown(self):
        """Reinicia el cooldown de movimiento después de moverse."""
        self.move_cooldown = self.move_cooldown_max

    def set_pos(self, fila, col):
        """Establece la posición del proyectil e inicia animación."""
        from game_logic import TAM_CASILLA
        
        if self.posicion is None:
            # Primera vez (spawn)
            self.posicion = (fila, col)
            self.x_visual = col * TAM_CASILLA + TAM_CASILLA // 2
            self.y_visual = fila * TAM_CASILLA + TAM_CASILLA // 2
            self.animando = False
        else:
            # Movimiento posterior
            self.origen_x = self.x_visual
            self.origen_y = self.y_visual
            self.destino_x = col * TAM_CASILLA + TAM_CASILLA // 2
            self.destino_y = fila * TAM_CASILLA + TAM_CASILLA // 2
            self.animando = True
            self.progreso_animacion = 0.0
            self.posicion = (fila, col)

    def take_damage(self, cantidad: int):
        """Los proyectiles no reciben daño, pero implementamos el método por consistencia."""
        pass

    def tick(self):
        """Actualiza el cooldown de movimiento."""
        self.move_tick()

    def actualizar_animacion_movimiento(self, delta_ms):
        """Actualiza la animación de movimiento suave."""
        if not self.animando:
            return
        
        incremento = delta_ms / self.duracion_animacion
        self.progreso_animacion += incremento
        
        if self.progreso_animacion >= 1.0:
            self.progreso_animacion = 1.0
            self.x_visual = self.destino_x
            self.y_visual = self.destino_y
            self.animando = False
        else:
            self.x_visual = self.lerp(self.origen_x, self.destino_x, self.progreso_animacion)
            self.y_visual = self.lerp(self.origen_y, self.destino_y, self.progreso_animacion)
    
    def lerp(self, inicio, fin, t):
        """Interpolación lineal entre dos valores."""
        return inicio + (fin - inicio) * t

# CLASE RAFAGA
class Rafaga:
    """Proyectil disparado por los rooks."""
    def __init__(self, dano: int = 5, tipo_rafaga: str = "arena"):
        self.tipo = "rafaga"
        self.tipo_rafaga = tipo_rafaga
        self.dano = dano
        self.posicion = None
        self.move_cooldown = 0  # Cooldown para controlar velocidad
        self.move_cooldown_max = 3  # Ajusta este valor: más alto = más lento (aumentado para hacer más lentas)

        #Atributos para animacion visual
        self.x_visual = 0
        self.y_visual = 0
        self.animando = False
        self.origen_x = 0
        self.origen_y = 0
        self.destino_x = 0
        self.destino_y = 0
        self.progreso_animacion = 0.0
        self.duracion_animacion = 700

    def can_move(self) -> bool:
        """Verifica si la ráfaga puede moverse."""
        return self.move_cooldown == 0

    def move_tick(self):
        """Actualiza el cooldown de movimiento."""
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

    def reset_move_cooldown(self):
        """Reinicia el cooldown de movimiento después de moverse."""
        self.move_cooldown = self.move_cooldown_max

    def set_pos(self, fila, col):
        """Establece la posición de la ráfaga e inicia animación."""
        from game_logic import TAM_CASILLA
        
        # Calcular nueva posición en píxeles
        nuevo_x = col * TAM_CASILLA + TAM_CASILLA // 2
        nuevo_y = fila * TAM_CASILLA + TAM_CASILLA // 2
        
        if self.posicion is None:
            #Primera vez (spawn) - colocar directamente sin animar
            self.posicion = (fila, col)
            self.x_visual = nuevo_x
            self.y_visual = nuevo_y
            self.animando = False
        else:
            #Movimiento posterior - SIEMPRE animar
            # Guardar origen ANTES de cambiar posición lógica
            self.origen_x = self.x_visual
            self.origen_y = self.y_visual
            self.destino_x = nuevo_x
            self.destino_y = nuevo_y
            
            # Iniciar animación
            self.animando = True
            self.progreso_animacion = 0.0
            
            # Actualizar posición lógica DESPUÉS de guardar origen
            self.posicion = (fila, col)

    def take_damage(self, cantidad: int):
        """Las ráfagas no reciben daño, pero implementamos el método por consistencia."""
        pass

    def tick(self):
        """Actualiza el cooldown de movimiento."""
        self.move_tick()

    #metodos para animacion visual
    def actualizar_animacion_movimiento(self, delta_ms):
        """Actualiza la animación de movimiento suave."""
        if not self.animando:
            return
        
        incremento = delta_ms / self.duracion_animacion
        self.progreso_animacion += incremento
        
        if self.progreso_animacion >= 1.0:
            self.progreso_animacion = 1.0
            self.x_visual = self.destino_x
            self.y_visual = self.destino_y
            self.animando = False
        else:
            self.x_visual = self.lerp(self.origen_x, self.destino_x, self.progreso_animacion)
            self.y_visual = self.lerp(self.origen_y, self.destino_y, self.progreso_animacion)
    
    def lerp(self, inicio, fin, t):
        """Interpolación lineal entre dos valores."""
        return inicio + (fin - inicio) * t

# Diccionario de ayuda para crear rooks por tipo
TIPOS_ROOK = {
    "roca": RookRoca,
    "fuego": RookFuego,
    "agua": RookAgua,
    "arena": RookArena
}

# Diccionario de ayuda para crear avatars por tipo
TIPOS_AVATAR = {
    "flechador": AvatarFlechador,
    "escudero": AvatarEscudero,
    "canibal": AvatarCanibal,
    "lenador": AvatarLenador
}

# FUNCIONES DE UTILIDAD

def crear_rook(tipo: str):
    """Crea un rook del tipo especificado."""
    if tipo in TIPOS_ROOK:
        return TIPOS_ROOK[tipo]()
    return None


def crear_avatar(tipo: str):
    """Crea un avatar del tipo especificado."""
    if tipo in TIPOS_AVATAR:
        return TIPOS_AVATAR[tipo]()
    return None

