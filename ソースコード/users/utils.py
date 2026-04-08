import secrets
import string


def generate_password(size=8):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for x in range(size))
