import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Class to handle en- and decryption. 
class Crypto():
        
    def __init__(self):
        self.__tmp_key = Fernet.generate_key()

    
    # Function to setup cryptography and to return the salt
    def generate_salt(self):
        salt = os.urandom(16)
        return salt

    # Function to encrypt to be saved passwords
    def encrypt(self, data, salt, enc_password):
        password = self.tmp_decrypt(enc_password)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        data = f.encrypt(str.encode(data))
        print(type(data))
        return data

    # Funcion to decrypt saved passwords
    def decrypt(self, data, salt, enc_password):
        password = self.tmp_decrypt(enc_password)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        data = f.decrypt(data)
        return data

    # Function to encrypt the masterpassword
    def tmp_encrypt(self, data):
        data = str.encode(data)
        f = Fernet(self.__tmp_key)
        data = f.encrypt(data)
        return data

    # Function to decrypt the masterpassword
    def tmp_decrypt(self, data):
        f = Fernet(self.__tmp_key)
        data = f.decrypt(data)
        return data