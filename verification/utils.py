import string
import secrets


def generate_code():
    characters = string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(6))
    return random_string
