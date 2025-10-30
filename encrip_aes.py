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
    key = AESGCM.generate_key(bit_length=256)  # AES-256
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
    
def verify_cvv(username: str, cvv_input: str) -> bool:
    cards = load_cards_aes()
    if username not in cards:
        return False
    
    stored_hash = cards[username]['cvv_hash']
    return verify_password(stored_hash, cvv_input)

# -----------------------
# Manejo de archivo users.txt
# -----------------------
USERS_FILE = "users.txt"
CARDS_FILE = "cards.txt"

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

def load_cards_aes() -> dict:
    if not os.path.exists(CARDS_FILE):
        return {}
    
    # Verificar si el archivo está vacío
    if os.path.getsize(CARDS_FILE) == 0:
        return {}
    
    try:
        with open(CARDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Si el archivo no es JSON válido, crear uno nuevo
        print("⚠️ Archivo users.txt corrupto, creando uno nuevo...")
        return {}

def save_users_aes(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def save_cards_aes(cards: dict):
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)



def get_users_decrypted() -> dict:
    users_enc = load_users_aes()
    users_dec = {}
    for enc_username, data in users_enc.items():
        try:
            dec_username = decrypt_data(enc_username, master_key)
            users_dec[dec_username] = data
        except Exception:
            continue
    return users_dec

def get_cards_decrypted() -> dict:
    cards_enc = load_cards_aes()
    cards_dec = {}
    for enc_username, data in cards_enc.items():
        try:
            dec_username = decrypt_data(enc_username, master_key)
            cards_dec[dec_username] = data
        except Exception:
            continue
    return cards_dec



# -----------------------
# Registro y login
# -----------------------
def register_user_aes(username: str, password: str, nombre: str, email: str, 
                      nacionalidad: str, apellidos: str, telefono: str,
                      pregunta_seguridad: str = None, respuesta_seguridad: str = None,
                      save_photo_callback = None):
    users = load_users_aes()
    enc_username = encrypt_data(username, master_key)
    if enc_username in users:
        print("❌ Usuario ya existe")
        return False

    # Hash de contraseña
    pwd_hash = hash_password(password)

    # Cifrado de datos personales
    enc_nombre = encrypt_data(nombre, master_key)
    enc_email = encrypt_data(email, master_key)
    enc_nacionalidad = encrypt_data(nacionalidad, master_key)
    enc_apellidos = encrypt_data(apellidos, master_key)
    enc_telefono = encrypt_data(telefono, master_key)

    # Preparar datos del usuario
    user_data = {
        "password_hash": pwd_hash,
        "nombre_enc": enc_nombre,
        "email_enc": enc_email,
        "nacionalidad_enc": enc_nacionalidad,
        "apellidos_enc": enc_apellidos,
        "telefono_enc": enc_telefono,
        "primerIngreso": True
    }

    # Guardar foto de perfil si se proporciona el callback
    if save_photo_callback:
        try:
            final_photo_path = save_photo_callback(enc_username)
            if final_photo_path:
                enc_profile_photo = encrypt_data(final_photo_path, master_key)
                user_data["profile_photo_enc"] = enc_profile_photo
        except Exception as e:
            print(f"Error guardando foto de perfil: {e}")

    # Agregar pregunta de seguridad si se proporciona
    if pregunta_seguridad and respuesta_seguridad:
        enc_pregunta = encrypt_data(pregunta_seguridad, master_key)
        respuesta_hash = hash_password(respuesta_seguridad.lower().strip())
        user_data["security_question_enc"] = enc_pregunta
        user_data["security_answer_hash"] = respuesta_hash

    users[enc_username] = user_data
    save_users_aes(users)
    return True

def register_user_card(username: str, cvv: str, numero: str, expiry: str, titular: str):
    cards = load_cards_aes()
    if username in cards:
        print("❌ Usuario ya existe")
        return

    # Hash del CVV
    cvv_hash = hash_password(cvv)

    # Cifrado de datos personales
    enc_username = encrypt_data(username, master_key)
    enc_numero = encrypt_data(numero, master_key)
    enc_expiry = encrypt_data(expiry, master_key)
    enc_titular = encrypt_data(titular, master_key)

    cards[enc_username] = {
        "numero_enc": enc_numero,
        "expiry_enc": enc_expiry,
        "cvv_hash": cvv_hash,
        "titular_enc": enc_titular
    }
    save_cards_aes(cards)
    print(f"✅ Tarjeta del usuario {username} registrada con éxito")

def login_user(username: str, password: str):
    users = load_users_aes()
    key = None
    for enc_username in users:
        try:
            dec_username = decrypt_data(enc_username, master_key)
            if username == dec_username:
                key = enc_username
                break
        except Exception:
            continue
    
    if not key:
        print("❌ Usuario no encontrado")
        return

    record = users[key]
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
    register_user_aes("juan", "1234", "Juan Pérez", "juan@example.com")
    register_user_aes("ana", "abcd", "Ana López", "ana@example.com")

    # Intentar loguearse
    login_user("juan", "1234")   # ✅ Correcto
    login_user("juan", "mala")   # ❌ Incorrecto
