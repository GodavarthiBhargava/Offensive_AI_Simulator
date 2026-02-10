from itertools import product
from backend.hashing_utils import hash_password
import string

def brute_force_plain(password, max_length=4, charset=None):
    """Brute force attack for plain password"""
    if charset is None:
        charset = string.digits + string.ascii_lowercase
    
    for length in range(1, min(len(password), max_length) + 1):
        for attempt in product(charset, repeat=length):
            candidate = ''.join(attempt)
            if candidate == password:
                return True, candidate, "Brute Force"
    
    return False, None, "Not Cracked"

def brute_force_hash(target_hash, algorithm, max_length=4, charset=None):
    """Brute force attack for hash value"""
    if charset is None:
        charset = string.digits + string.ascii_lowercase
    
    for length in range(1, max_length + 1):
        for attempt in product(charset, repeat=length):
            candidate = ''.join(attempt)
            if hash_password(candidate, algorithm) == target_hash:
                return True, candidate, f"Brute Force with {algorithm}"
    
    return False, None, f"Not Cracked with {algorithm}"
