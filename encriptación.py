# Encriptación de datos
class Encriptacion:
    def __init__(self):
        self.alfa = '0123456789abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ@./'
        self.beta = 'aGQhBRl2WZmp5ñq0cVSOJ/Ñ@7Ii9xEvHz8ujfCMLnAgYrosD1P.Nd3yK46wbXTkUeFt'

    def encriptar(self, texto):
        hola = {c: self.beta[i] for i, c in enumerate(self.alfa)}
        return "".join(hola.get(c, c) for c in texto)

    def desencriptar(self, texto):
        hola = {self.beta[i]: c for i, c in enumerate(self.alfa)}
        return "".join(hola.get(c, c) for c in texto)

encriptador = Encriptacion()

def encriptar(texto):
    return encriptador.encriptar(texto)

def desencriptar(texto):
    return encriptador.desencriptar(texto)
