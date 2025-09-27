from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

token = f.encrypt(b"mensaje secreto")
print(token)

original = f.decrypt(token)
print(original)
