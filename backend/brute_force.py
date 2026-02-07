from itertools import product
from backend.hashing import hash_password

def brute_force_attack(target_hash, algorithm, max_length=4):
    """Simulate safe brute force attack (numeric only, max length 4)"""
    charset = "0123456789"
    
    for length in range(1, max_length + 1):
        for attempt in product(charset, repeat=length):
            password = ''.join(attempt)
            if hash_password(password, algorithm) == target_hash:
                return True, password
    return False, None
