import secrets

def generate_secret_token_hex(nbytes: int = 16):
    return secrets.token_hex(nbytes)
