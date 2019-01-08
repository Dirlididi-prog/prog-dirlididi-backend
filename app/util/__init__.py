from random import choice
from string import ascii_letters, digits

def key_generator(size=9, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(size))