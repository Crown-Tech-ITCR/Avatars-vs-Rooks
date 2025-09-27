# Encriptación de datos
alfa = '0123456789abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ@.'
beta = 'aGQhBRl2WZmp5ñq0cVSOJÑ@7Ii9xEvHz8ujfCMLnAgYrosD1P.Nd3yK46wbXTkUeFt'

def encriptar(texto, clave):
    hola = {c: clave[i] for i, c in enumerate(alfa)}
    return "".join(hola.get(c, c) for c in texto)

def desencriptar(texto, clave):
    hola = {clave[i]: c for i, c in enumerate(alfa)}
    return "".join(hola.get(c, c) for c in texto)

mensaje = "HolaMundo123"
encriptado = encriptar(mensaje, beta)
desencriptado = desencriptar(encriptado, beta)

print("Mensaje original: ", mensaje)
print("Encriptado:       ", encriptado)
print("Desencriptado:    ", desencriptado)
