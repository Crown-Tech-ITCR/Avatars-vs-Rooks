import numpy as np
import random
from Moneda import Moneda

# Configuración de distribuciones
LAMBDA_POISSON = {
    100: 0.3,  # Pocas monedas de 100
    50: 1.0,   # Algunas monedas de 50
    25: 2.0    # Más monedas de 25
}

LAMBDA_EXPONENCIAL = 0.1  # Tiempo promedio: 10 segundos


def generar_cantidades_poisson():
    """
    Genera cantidades de monedas usando distribución de Poisson.
    Versión optimizada que garantiza resultado rápido.
    
    Returns:
        dict: Cantidad de cada denominación {100: n1, 50: n2, 25: n3}
    """
    # Combinaciones válidas predefinidas que suman 100
    combinaciones_validas = [
        {100: 1, 50: 0, 25: 0},
        {100: 0, 50: 2, 25: 0},
        {100: 0, 50: 1, 25: 2},
        {100: 0, 50: 0, 25: 4},
    ]
    
    # Intentar con Poisson solo 10 veces (evita bucles largos)
    for intento in range(10):
        cant_100 = np.random.poisson(LAMBDA_POISSON[100])
        cant_50 = np.random.poisson(LAMBDA_POISSON[50])
        cant_25 = np.random.poisson(LAMBDA_POISSON[25])
        
        total = cant_100 * 100 + cant_50 * 50 + cant_25 * 25
        
        if total == 100:
            print(f"✅ Poisson exitoso: {cant_100}x100 + {cant_50}x50 + {cant_25}x25 = 100")
            return {100: cant_100, 50: cant_50, 25: cant_25}
        
        # Intentar ajustar si está cerca
        if total < 100 and (100 - total) <= 100:
            diferencia = 100 - total
            if diferencia == 100:
                print(f"✅ Ajustado: agregando 1x100")
                return {100: cant_100 + 1, 50: cant_50, 25: cant_25}
            elif diferencia == 50:
                print(f"✅ Ajustado: agregando 1x50")
                return {100: cant_100, 50: cant_50 + 1, 25: cant_25}
            elif diferencia % 25 == 0:
                print(f"✅ Ajustado: agregando {diferencia // 25}x25")
                return {100: cant_100, 50: cant_50, 25: cant_25 + diferencia // 25}
    
    # Fallback: usar combinaciones predefinidas con probabilidades según Poisson
    # Mayor peso para combinaciones con más monedas pequeñas
    pesos = [10, 20, 30, 40]  # Mayor peso para 4x25
    combinacion = random.choices(combinaciones_validas, weights=pesos)[0]
    print(f"⚠️ Usando fallback: {combinacion}")
    return combinacion


def generar_tiempo_limite_exponencial():
    """
    Genera un tiempo límite usando distribución exponencial.
    
    Returns:
        float: Tiempo en segundos (mínimo 3, promedio 10)
    """
    tiempo = np.random.exponential(1 / LAMBDA_EXPONENCIAL)
    # Establecer un mínimo de 3 segundos para que sea jugable
    return max(3.0, tiempo)


def crear_monedas_en_tablero(matriz_juego, filas, columnas):
    """
    Crea monedas en el tablero que suman 100.
    
    Args:
        matriz_juego: Matriz del juego
        filas (int): Número de filas
        columnas (int): Número de columnas
        
    Returns:
        list: Lista de objetos Moneda creados
    """
    print("🔄 Generando cantidades con Poisson...")
    
    # Generar cantidades con Poisson
    cantidades = generar_cantidades_poisson()
    
    # Crear lista de monedas a colocar
    monedas_a_colocar = []
    for valor, cantidad in cantidades.items():
        for _ in range(cantidad):
            tiempo_limite = generar_tiempo_limite_exponencial()
            monedas_a_colocar.append((valor, tiempo_limite))
    
    print(f"📊 Total monedas a colocar: {len(monedas_a_colocar)}")
    
    # Buscar casillas vacías
    casillas_vacias = []
    for f in range(filas):
        for c in range(columnas):
            # Verificar que la casilla esté completamente vacía
            if len(matriz_juego[f][c]) == 0:
                casillas_vacias.append((f, c))
    
    print(f"📍 Casillas vacías disponibles: {len(casillas_vacias)}")
    
    # Si no hay suficientes casillas vacías, usar las que haya
    if len(casillas_vacias) < len(monedas_a_colocar):
        print(f"⚠️ Solo hay {len(casillas_vacias)} casillas vacías para {len(monedas_a_colocar)} monedas")
    
    # Colocar monedas aleatoriamente
    random.shuffle(casillas_vacias)
    monedas_creadas = []
    
    for i, (valor, tiempo_limite) in enumerate(monedas_a_colocar):
        if i < len(casillas_vacias):
            fila, col = casillas_vacias[i]
            moneda = Moneda(valor, fila, col, tiempo_limite)
            matriz_juego[fila][col].append(moneda)
            monedas_creadas.append(moneda)
            print(f"💰 Moneda de {valor} colocada en ({fila}, {col}) - expira en {tiempo_limite:.1f}s")
    
    print(f"✅ {len(monedas_creadas)} monedas creadas exitosamente")
    return monedas_creadas


def verificar_monedas_expiradas(matriz_juego, filas, columnas):
    """
    Verifica y elimina monedas que han expirado.
    
    Args:
        matriz_juego: Matriz del juego
        filas (int): Número de filas
        columnas (int): Número de columnas
    """
    for f in range(filas):
        for c in range(columnas):
            entidades = list(matriz_juego[f][c])
            for entidad in entidades:
                if isinstance(entidad, Moneda) and entidad.esta_expirada():
                    if entidad in matriz_juego[f][c]:
                        matriz_juego[f][c].remove(entidad)
                        print(f"⏰ Moneda de {entidad.valor} expiró en ({f}, {c})")