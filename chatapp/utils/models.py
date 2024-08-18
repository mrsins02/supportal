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
    return f'{instance.__class__.__name__.lower()}/{instance.id}{get_file_extension(filename)}'


class GenerateRandomCode:
    """
    A class to generate random code and return as a string or integer.
    - To use class first build an instance of that
    - then call the instance
    - For integer returning you must set the argument <return_string=False>
    """

    def __init__(self, length: int, return_string: bool = True):
        if not isinstance(length, int):
            raise TypeError('length must be an integer')
        if not isinstance(return_string, bool):
            raise TypeError('return_string must be a boolean')
        self.length = length
        self.return_string = return_string

    def __call__(self) -> str | int:
        code = self.generate_random_code(self.length)

        return code if self.return_string else int(code)

    def generate_random_code(self, length) -> str:
        return ''.join([random.choice(string.digits) for i in range(length)])
