from backend.hashing import hash_password
import itertools

def ai_attack_plain(password, first_name, last_name):
    """AI-based attack for plain password"""
    # Generate smart guesses based on personal info
    guesses = []
    
    # Personal info variations
    if first_name:
        guesses.extend([first_name, first_name.lower(), first_name.upper(), first_name.capitalize()])
    if last_name:
        guesses.extend([last_name, last_name.lower(), last_name.upper(), last_name.capitalize()])
    
    # Common patterns with names
    for name in [first_name, last_name]:
        if name:
            for num in ['123', '1234', '12345', '2024', '2025', '!', '@123']:
                guesses.append(name + num)
                guesses.append(name.lower() + num)
    
    # Check guesses
    for guess in guesses:
        if guess == password:
            return True, guess, "AI Pattern Match"
    
    return False, None, "AI Search Failed"

def ai_attack_hash(target_hash, algorithm, first_name, last_name):
    """AI-based attack for hash value"""
    # Generate smart guesses
    guesses = []
    
    # Personal info variations
    if first_name:
        guesses.extend([first_name, first_name.lower(), first_name.upper(), first_name.capitalize()])
    if last_name:
        guesses.extend([last_name, last_name.lower(), last_name.upper(), last_name.capitalize()])
    
    # Common patterns with names
    for name in [first_name, last_name]:
        if name:
            for num in ['123', '1234', '12345', '2024', '2025', '!', '@123']:
                guesses.append(name + num)
                guesses.append(name.lower() + num)
    
    # Check guesses
    for guess in guesses:
        if hash_password(guess, algorithm).lower() == target_hash.lower():
            return True, guess, f"AI Pattern Match with {algorithm}"
    
    return False, None, f"AI Search Failed with {algorithm}"
