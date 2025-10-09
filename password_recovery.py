import encrip_aes
from Traducciones import t, set_language

class PasswordRecovery:
    """Maneja el sistema de preguntas de seguridad para recuperación de contraseña"""
    
    # Preguntas de seguridad disponibles
    SECURITY_QUESTIONS = [
        t("pregunta1"),
        t("pregunta2"),
        t("pregunta3"),
        t("pregunta4")
    ]
    
    def __init__(self, master_key):
        """
        Inicializa el sistema de recuperación
        
        Args:
            master_key: Clave maestra para cifrado AES-GCM
        """
        self.master_key = master_key
    
    def add_security_question(self, username: str, question: str, answer: str):
        """
        Agrega pregunta y respuesta de seguridad al usuario
        
        Args:
            username: Nombre de usuario
            question: Pregunta de seguridad
            answer: Respuesta a la pregunta
        """
        users = encrip_aes.load_users_aes()
        
        if username not in users:
            return False, "Usuario no encontrado"
        
        # Cifrar la pregunta
        enc_question = encrip_aes.encrypt_data(question, self.master_key)
        
        # Hash de la respuesta (como las contraseñas)
        answer_hash = encrip_aes.hash_password(answer.lower().strip())
        
        # Agregar al registro del usuario
        users[username]["security_question_enc"] = enc_question
        users[username]["security_answer_hash"] = answer_hash
        
        encrip_aes.save_users_aes(users)
        return True, "Pregunta de seguridad guardada"
    
    def get_security_question(self, username: str):
        """
        Obtiene la pregunta de seguridad de un usuario
        
        Args:
            username: Nombre de usuario
            
        Returns:
            str: Pregunta de seguridad descifrada o None si no existe
        """
        users = encrip_aes.load_users_aes()
        
        if username not in users:
            return None
        
        if "security_question_enc" not in users[username]:
            return None
        
        # Descifrar la pregunta
        enc_question = users[username]["security_question_enc"]
        question = encrip_aes.decrypt_data(enc_question, self.master_key)
        
        return question
    
    def verify_security_answer(self, username: str, answer: str) -> bool:
        """
        Verifica si la respuesta de seguridad es correcta
        
        Args:
            username: Nombre de usuario
            answer: Respuesta proporcionada por el usuario
            
        Returns:
            bool: True si la respuesta es correcta
        """
        users = encrip_aes.load_users_aes()
        
        if username not in users:
            return False
        
        if "security_answer_hash" not in users[username]:
            return False
        
        stored_hash = users[username]["security_answer_hash"]
        
        # Verificar usando Argon2 (igual que las contraseñas)
        return encrip_aes.verify_password(stored_hash, answer.lower().strip())
    
    def reset_password(self, username: str, new_password: str) -> bool:
        """
        Restablece la contraseña del usuario
        
        Args:
            username: Nombre de usuario
            new_password: Nueva contraseña
            
        Returns:
            bool: True si se actualizó correctamente
        """
        users = encrip_aes.load_users_aes()
        
        if username not in users:
            return False
        
        # Hash de la nueva contraseña con Argon2
        new_hash = encrip_aes.hash_password(new_password)
        users[username]["password_hash"] = new_hash
        
        encrip_aes.save_users_aes(users)
        return True
    
    def user_has_security_question(self, username: str) -> bool:
        """
        Verifica si un usuario tiene pregunta de seguridad configurada
        
        Args:
            username: Nombre de usuario
            
        Returns:
            bool: True si tiene pregunta de seguridad
        """
        users = encrip_aes.load_users_aes()
        
        if username not in users:
            return False
        
        return "security_question_enc" in users[username]