import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Originally I thought about writing a hashfunction myself but
# I don't fell like doing that right now.

# Class to handle en- and decryption.  I made a class here because
# a key was more useful as a global variable.

# TODO initiate with password??
__key = Fernet.generate_key()

# Function to create the salt


def setup():
    salt = os.urandom(16)

    return salt


# Function to encrypt session data.


def tmp_encrypt(data):
    f = Fernet(__key)
    data = f.encrypt(str.encode(data))

    return data


# Function to decrypt session data.


def tmp_decrypt(data):
    f = Fernet(__key)
    data = f.decrypt(data)

    return data


# Function to encrypt and decrypt data.


def de_or_encrypt(data, salt, enc_password, mode):
    password = tmp_decrypt(enc_password)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
    )
    key0 = base64.urlsafe_b64encode(kdf.derive(password))
    if isinstance(data, str):
        data = str.encode(data)
    f = Fernet(key0)
    if mode == "encrypt":
        data = f.encrypt(data)
    elif mode == "decrypt":
        f.decrypt(data)
        data = str(data)

    return data