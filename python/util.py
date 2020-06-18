from hashlib import sha512

def hash_password(password, salt = "SHAKE"):
    hasher = sha512()
    hasher.update((password + salt).encode())
    return hasher.hexdigest()