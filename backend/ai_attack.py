from backend.hashing_utils import hash_password
import string

def ai_attack_plain(password, first_name, last_name):
    """AI-based attack for plain password using intelligent patterns"""
    candidates = []
    
    # Personal info variations
    if first_name:
        candidates.extend([
            first_name.lower(),
            first_name.capitalize(),
            first_name.upper()
        ])
    
    if last_name:
        candidates.extend([
            last_name.lower(),
            last_name.capitalize(),
            last_name.upper()
        ])
    
    # Common patterns with names
    if first_name and last_name:
        candidates.extend([
            first_name.lower() + last_name.lower(),
            first_name[0].lower() + last_name.lower(),
            first_name.lower() + last_name[0].lower()
        ])
    
    # Common password patterns
    common_patterns = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "password123", "admin", "letmein", "welcome", "monkey"
    ]
    candidates.extend(common_patterns)
    
    # Check all candidates
    for candidate in candidates:
        if candidate == password:
            return True, candidate, "AI Search"
    
    return False, None, "Not Cracked"

def ai_attack_hash(target_hash, algorithm, first_name, last_name):
    """AI-based attack for hash value using intelligent patterns"""
    candidates = []
    
    # Personal info variations
    if first_name:
        candidates.extend([
            first_name.lower(),
            first_name.capitalize(),
            first_name.upper()
        ])
    
    if last_name:
        candidates.extend([
            last_name.lower(),
            last_name.capitalize(),
            last_name.upper()
        ])
    
    # Common patterns with names
    if first_name and last_name:
        candidates.extend([
            first_name.lower() + last_name.lower(),
            first_name[0].lower() + last_name.lower(),
            first_name.lower() + last_name[0].lower()
        ])
    
    # Common password patterns
    common_patterns = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "password123", "admin", "letmein", "welcome", "monkey"
    ]
    candidates.extend(common_patterns)
    
    # Check all candidates
    for candidate in candidates:
        if hash_password(candidate, algorithm) == target_hash:
            return True, candidate, f"AI Search with {algorithm}"
    
    return False, None, f"Not Cracked with {algorithm}"
