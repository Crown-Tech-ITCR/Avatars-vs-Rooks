import math

class SistemaPuntos:
    """Sistema de cálculo de puntos del juego"""
    
    def calcular_puntaje(self, tempo, popularidad, avatars_matados, puntos_vida_acumulados):
        """Calcula el puntaje ajustado"""
        
        # Calcular límite máximo
        limite_maximo = 0.20 * (tempo + popularidad + avatars_matados + puntos_vida_acumulados)
        
        # Calcular media armónica
        if tempo > 0 and popularidad > 0:
            media_armonica = 2 / ((1 / tempo) + (1 / popularidad))
        else:
            media_armonica = 0
        
        # Calcular factor de intensidad
        factor_intensidad = (avatars_matados / (tempo + 1)) * 0.05
        
        # Calcular factor avatar
        factor_avatar = 1 + math.sqrt(puntos_vida_acumulados / 500)
        
        # Calcular puntaje ajustado
        puntaje_ajustado = (media_armonica + (factor_intensidad * 100)) * factor_avatar
        
        # Aplicar límite máximo
        if puntaje_ajustado > limite_maximo:
            puntaje_ajustado = limite_maximo
        
        return puntaje_ajustado