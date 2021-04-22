from django.utils.crypto import get_random_string


def get_random_code():
    code = get_random_string(length=20, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return code
