import secrets

isProduction = False


#**********random uid****************
def generate_unique_id(len):
    return secrets.token_hex(len)