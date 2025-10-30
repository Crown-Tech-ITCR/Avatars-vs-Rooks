import encrip_aes
import json

def check_user(username):
    """Verifica si un usuario tiene pregunta de seguridad"""
    users = encrip_aes.load_users_aes()
    master_key = encrip_aes.master_key
    
    for enc_username, data in users.items():
        try:
            dec_username = encrip_aes.decrypt_data(enc_username, master_key)
            if dec_username == username:
                print(f"\n✅ Usuario encontrado: {username}")
                print(f"📋 Campos disponibles:")
                for key in data.keys():
                    print(f"   - {key}")
                
                if "security_question_enc" in data:
                    pregunta = encrip_aes.decrypt_data(data["security_question_enc"], master_key)
                    print(f"\n✅ Tiene pregunta de seguridad: {pregunta}")
                else:
                    print(f"\n❌ NO tiene pregunta de seguridad configurada")
                return
        except:
            continue
    
    print(f"❌ Usuario '{username}' no encontrado")

if __name__ == "__main__":
    username = input("Ingresa el username a verificar: ")
    check_user(username)