import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2 import PasswordHasher

# -----------------------
# Helpers
# -----------------------
def b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")

def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("utf-8"))

# -----------------------
# Gestión de clave AES
# -----------------------
MASTER_KEY_FILE = "master.key"

def load_or_create_key() -> bytes:
    if os.path.exists(MASTER_KEY_FILE):
        return open(MASTER_KEY_FILE, "rb").read()
    key = os.urandom(16)  # AES-128
    with open(MASTER_KEY_FILE, "wb") as f:
        f.write(key)
    return key

master_key = load_or_create_key()

# -----------------------
# Cifrado AES-GCM (para datos personales)
# -----------------------
def encrypt_data(plaintext: str, key: bytes) -> str:
    aes = AESGCM(key)
    iv = os.urandom(12)
    ct = aes.encrypt(iv, plaintext.encode("utf-8"), None)
    return b64e(iv + ct)

def decrypt_data(b64data: str, key: bytes) -> str:
    raw = b64d(b64data)
    iv = raw[:12]
    ct = raw[12:]
    aes = AESGCM(key)
    pt = aes.decrypt(iv, ct, None)
    return pt.decode("utf-8")

# -----------------------
# Hash Argon2 (para contraseñas)
# -----------------------
ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    try:
        return ph.verify(stored_hash, password)
    except Exception:
        return False

# -----------------------
# Manejo de archivo users.txt
# -----------------------
USERS_FILE = "users.txt"

def load_users_aes() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    
    # Verificar si el archivo está vacío
    if os.path.getsize(USERS_FILE) == 0:
        return {}
    
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Si el archivo no es JSON válido, crear uno nuevo
        print("⚠️ Archivo users.txt corrupto, creando uno nuevo...")
        return {}

def save_users_aes(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# -----------------------
# Registro y login
# -----------------------
def register_user(username: str, password: str, nombre: str, email: str, nacionalidad: str, apellidos: str):
    users = load_users_aes()
    if username in users:
        print("❌ Usuario ya existe")
        return

    # Hash de contraseña
    pwd_hash = hash_password(password)

    # Cifrado de datos personales
    enc_nombre = encrypt_data(nombre, master_key)
    enc_email = encrypt_data(email, master_key)
    enc_nacionalidad = encrypt_data(nacionalidad, master_key)
    enc_apellidos = encrypt_data(apellidos, master_key)

    users[username] = {
        "password_hash": pwd_hash,
        "nombre_enc": enc_nombre,
        "email_enc": enc_email,
        "nacionalidad_enc": enc_nacionalidad,
        "apellidos_enc": enc_apellidos

    }
    save_users_aes(users)
    print(f"✅ Usuario {username} registrado con éxito")

def login_user(username: str, password: str):
    users = load_users_aes()
    if username not in users:
        print("❌ Usuario no encontrado")
        return

    record = users[username]
    if verify_password(record["password_hash"], password):
        # Desciframos datos personales
        nombre = decrypt_data(record["nombre_enc"], master_key)
        email = decrypt_data(record["email_enc"], master_key)
        print(f"✅ Bienvenido {nombre} ({email})")
    else:
        print("❌ Contraseña incorrecta")

# -----------------------
# Ejemplo de uso
# -----------------------
if __name__ == "__main__":
    # Registrar usuarios
    register_user("juan", "1234", "Juan Pérez", "juan@example.com")
    register_user("ana", "abcd", "Ana López", "ana@example.com")

    # Intentar loguearse
    login_user("juan", "1234")   # ✅ Correcto
    login_user("juan", "mala")   # ❌ Incorrecto
