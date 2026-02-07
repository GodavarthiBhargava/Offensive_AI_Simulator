import os
from backend.hashing import hash_password

def dictionary_attack(target_hash, algorithm, wordlist_path="resources/wordlist.txt"):
    """Simulate dictionary attack by comparing hashes"""
    if not os.path.exists(wordlist_path):
        return False, None
    
    with open(wordlist_path, 'r') as f:
        for line in f:
            word = line.strip()
            if hash_password(word, algorithm) == target_hash:
                return True, word
    return False, None
