from random import choice
from string import ascii_letters, digits
from hashlib import sha512

def key_generator(size=9, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(size))


def hash_password(password):
    hash = sha512()
    hash.update(password.encode())
    return hash.hexdigest()