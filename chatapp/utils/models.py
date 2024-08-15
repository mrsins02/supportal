import os
import random
import string


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1]


def upload_location(instance, filename: str) -> str:
    return f'/{instance._meta.label}/{instance.id}{get_file_extension(filename)}'


def generate_random_number(length: int = 4) -> str:
    return ''.join([random.choice(string.digits) for i in range(length)])
