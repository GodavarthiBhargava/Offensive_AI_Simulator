from backend.hashing import hash_password

def dictionary_attack_plain(password, wordlist_files, first_name, last_name):
    """Dictionary attack for plain password"""
    # Check personal information first
    if password.lower() == first_name.lower() or password.lower() == last_name.lower():
        return True, password, "Personal Information Match"
    
    # Check wordlists
    for wordlist_path in wordlist_files:
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip()
                    if word == password:
                        return True, word, "Dictionary Attack"
        except Exception as e:
            continue
    
    return False, None, "Not Found"

def dictionary_attack_hash(target_hash, algorithm, wordlist_files, first_name, last_name):
    """Dictionary attack for hash value"""
    # Check personal information first
    for name in [first_name, last_name]:
        if name and hash_password(name, algorithm) == target_hash:
            return True, name, f"Personal Information Match with {algorithm}"
    
    # Check wordlists
    for wordlist_path in wordlist_files:
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip()
                    if hash_password(word, algorithm) == target_hash:
                        return True, word, f"Dictionary Attack with {algorithm}"
        except Exception as e:
            continue
    
    return False, None, f"Not Cracked with {algorithm}"
