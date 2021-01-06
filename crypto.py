import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Originally I thought about writing a hashfunction myself but
# I don't fell like doing that right now.

# Class to handle en- and decryption.  I made a class here because
# a key was more useful as a global variable.


class Crypto:
    __key = None
    # Function to create the salt

    def setup():
        salt = os.urandom(16)
        return salt

    # Function to encrypt session data.

    def tmp_encrypt(
        data,
    ):
        __key = Fernet.generate_key()
        f = Fernet(__key)
        data = f.encrypt(str.encode(data))

        print(__key)

        return data

    # Function to decrypt session data.

    def tmp_decrypt(data):
        f = Fernet(__key)
        data = f.decrypt(data)

        print(data)
        return data

    # Function to encrypt data.

    def encrypt(data, salt):
        return data

    # Function to decrypt data.

    def decrypt(data, salt):
        return data