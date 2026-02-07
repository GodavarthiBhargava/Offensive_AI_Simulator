import hashlib

def hash_password(password, algorithm):
    """Hash password using specified algorithm"""
    if algorithm == "MD5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == "SHA256":
        return hashlib.sha256(password.encode()).hexdigest()
    else:
        raise ValueError("Unsupported algorithm")
