class Entidad:
    """Clase base para todas las entidades del juego (rooks, avatars, etc.)."""
    def __init__(self, tipo: str, vida: int = 10, dano: int = 1, movil: bool = False):
        self.tipo = tipo
        self.vida = vida
        self.dano = dano
        self.posicion = None  # (fila, col)
        self.movil = movil

    def set_pos(self, fila, col):
        """Establece la posición de la entidad."""
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

# CLASES DE ROOKS
class Rook(Entidad):
    """Rook base: no se desplaza, puede disparar si su cooldown está a cero."""
    def __init__(self, vida: int = 10, dano: int = 10, shot_cooldown_max: int = 0, costo: int = 0):
        super().__init__("rook", vida=vida, dano=dano, movil=False)
        self.shot_cooldown = 0
        self.shot_cooldown_max = shot_cooldown_max
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
        super().__init__(vida=12, dano=4, shot_cooldown_max=0, costo=100)
        self.tipo = "rook_roca"
        self.color = "gray"


class RookFuego(Rook):
    """Rook de Fuego: Buen daño y resistencia equilibrada."""
    def __init__(self):
        super().__init__(vida=12, dano=8, shot_cooldown_max=0, costo=150)
        self.tipo = "rook_fuego"
        self.color = "orange"


class RookAgua(Rook):
    """Rook de Agua: Alta resistencia y alto daño."""
    def __init__(self):
        super().__init__(vida=15, dano=10, shot_cooldown_max=0, costo=150)
        self.tipo = "rook_agua"
        self.color = "cyan"


class RookArena(Rook):
    """Rook de Arena: Barato pero frágil y poco daño."""
    def __init__(self):
        super().__init__(vida=8, dano=2, shot_cooldown_max=0, costo=50)
        self.tipo = "rook_arena"
        self.color = "yellow"


# CLASES DE AVATARS
class Avatar(Entidad):
    """Avatar base: se mueve y puede atacar rooks."""
    def __init__(self, vida: int = 10, dano: int = 10, regeneracion: int = 0, move_cooldown_max: int = 3, rango_ataque: int = 1, ataque_a_distancia: bool = False):
        super().__init__("avatar", vida=vida, dano=dano, movil=True)
        self.regeneracion = regeneracion
        self.move_cooldown_max = move_cooldown_max
        self.move_cooldown = 0  # Cooldown actual para movimiento
        self.rango_ataque = rango_ataque  # Nuevo: rango de ataque
        self.ataque_a_distancia = ataque_a_distancia  # Nuevo: si ataca a distancia
        self.shot_cooldown = 0  # Nuevo: cooldown de disparo
        self.shot_cooldown_max = 3  # Nuevo: cooldown máximo de disparo

    def can_move(self) -> bool:
        """Verifica si el avatar puede moverse."""
        return self.move_cooldown == 0

    def can_shoot(self) -> bool:
        """Verifica si el avatar puede disparar."""
        return self.shot_cooldown == 0 and self.ataque_a_distancia

    def move_tick(self):
        """Actualiza el cooldown de movimiento."""
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

    def reset_move_cooldown(self):
        """Reinicia el cooldown de movimiento después de moverse."""
        self.move_cooldown = self.move_cooldown_max

    def shoot(self):
        """Dispara una ráfaga si puede atacar a distancia."""
        if self.can_shoot():
            self.shot_cooldown = self.shot_cooldown_max
            from Entidades import Rafaga  # Importación local para evitar problemas
            rafaga = Rafaga(self.dano)
            rafaga.tipo = f"rafaga_{self.tipo}"  # Identificar origen
            return rafaga
        return None

    def buscar_objetivo_en_rango(self, matriz_juego, mi_fila, mi_columna):
        """Busca rooks en el rango de ataque del avatar."""
        objetivos = []
        
        # Buscar rooks hacia arriba (dirección de avance del avatar)
        for f in range(mi_fila - 1, max(-1, mi_fila - self.rango_ataque - 1), -1):
            if f >= 0:
                rooks_en_fila = [r for r in matriz_juego[f][mi_columna] if isinstance(r, Rook)]
                if rooks_en_fila:
                    objetivos.extend(rooks_en_fila)
                    break  # Solo atacar al primer rook encontrado en línea recta
        
        return objetivos

    def puede_avanzar_sin_rooks(self, matriz_juego, mi_fila, mi_columna):
        """Verifica si hay rooks en toda la columna por delante."""
        if not self.ataque_a_distancia:
            return True  # Los avatars normales siempre pueden avanzar
        
        # Para avatars a distancia, verificar si hay rooks en toda la columna hacia arriba
        for f in range(mi_fila - 1, -1, -1):
            rooks_en_fila = [r for r in matriz_juego[f][mi_columna] if isinstance(r, Rook)]
            if rooks_en_fila:
                return False  # Hay al menos un rook en la columna
        
        return True  # No hay rooks en toda la columna

    def attack(self, objetivo):
        """Ataca a un objetivo si puede recibir daño."""
        if hasattr(objetivo, "take_damage"):
            objetivo.take_damage(self.dano)

    def tick(self):
        # Actualizar cooldown de disparo
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1



# TIPOS ESPECÍFICOS DE AVATARS
# Velocidades: Flechador (más lento) -> Escudero -> Leñador -> Caníbal (más rápido)

class AvatarFlechador(Avatar):
    """Avatar Flechador: Ataca a distancia, más lento, poco daño pero se regenera."""
    def __init__(self):
        super().__init__(vida=5, dano=3, regeneracion=2, move_cooldown_max=5, rango_ataque=3, ataque_a_distancia=True)
        self.tipo = "avatar_flechador"
        self.color = "orange"
        self.shot_cooldown_max = 4  # Más lento para disparar


class AvatarEscudero(Avatar):
    """Avatar Escudero: Ataca a distancia, velocidad media-lenta con regeneración moderada."""
    def __init__(self):
        super().__init__(vida=8, dano=4, regeneracion=1, move_cooldown_max=4, rango_ataque=2, ataque_a_distancia=True)
        self.tipo = "avatar_escudero"
        self.color = "blue"
        self.shot_cooldown_max = 3  # Más rápido que el flechador


class AvatarLenador(Avatar):
    """Avatar Leñador: Ataque cuerpo a cuerpo, velocidad media-rápida, alto daño sin regeneración."""
    def __init__(self):
        super().__init__(vida=20, dano=9, regeneracion=0, move_cooldown_max=3, rango_ataque=1, ataque_a_distancia=False)
        self.tipo = "avatar_lenador"
        self.color = "sienna"


class AvatarCanibal(Avatar):
    """Avatar Caníbal: Ataque cuerpo a cuerpo, más rápido, alto daño y regeneración alta."""
    def __init__(self):
        super().__init__(vida=25, dano=12, regeneracion=4, move_cooldown_max=2, rango_ataque=1, ataque_a_distancia=False)
        self.tipo = "avatar_canibal"
        self.color = "red"


# CLASE RAFAGA
class Rafaga:
    """Proyectil disparado por los rooks."""
    def __init__(self, dano: int = 5):
        self.tipo = "rafaga"
        self.dano = dano
        self.posicion = None
        self.move_cooldown = 0  # Cooldown para controlar velocidad
        self.move_cooldown_max = 5  # Ajusta este valor: más alto = más lento (aumentado para hacer más lentas)

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
        """Establece la posición de la ráfaga."""
        self.posicion = (fila, col)

    def take_damage(self, cantidad: int):
        """Las ráfagas no reciben daño, pero implementamos el método por consistencia."""
        pass

    def tick(self):
        """Actualiza el cooldown de movimiento."""
        self.move_tick()


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


