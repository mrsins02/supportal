import os
import random
import string


def get_file_extension(filename: str) -> str:
    """
    Returns given file's extension
    """
    return os.path.splitext(filename)[1]


def upload_location(instance, filename: str) -> str:
    """
    Returns a path to save files in media based of model name
    """
    return f"{instance.__class__.__name__.lower()}/{instance.id}{get_file_extension(filename)}"


def generate_random_number(length) -> str:
    return "".join([random.choice(seq=string.digits) for i in range(length)])


def generate_random_string(length) -> str:
    return "".join(
        [
            random.choice(seq=(string.digits + string.ascii_letters))
            for i in range(length)
        ]
    )
