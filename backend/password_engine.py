import re
from backend.hashing import hash_password
from backend.dictionary_attack import dictionary_attack
from backend.brute_force import brute_force_attack
from backend.ai_analyzer import analyze_password
from backend.session_store import session


def classify_password(password, username="", fullname=""):
    """
    Decide which attack strategy should be used
    """
    pwd = password.lower()
    uname = username.lower()
    fname_parts = fullname.lower().split()

    # Check context FIRST (highest priority)
    if uname and uname in pwd:
        return "CONTEXT"

    for part in fname_parts:
        if part and part in pwd:
            return "CONTEXT"

    # Then check other patterns
    if len(pwd) < 5:
        return "BRUTE_FORCE"

    if pwd.isdigit():
        return "BRUTE_FORCE"

    if pwd.isalpha():
        return "DICTIONARY"

    if re.fullmatch(r"[^\w]+", pwd):
        return "BRUTE_FORCE"

    return "AI_ONLY"


def simulate_password_attack(password, algorithm, username="", fullname=""):
    """
    Simulate password attack using dictionary and brute force methods
    """
    result = {
        "cracked": False,
        "attack_used": "None",
        "password_strength": "Strong",
        "ai_risk_level": "Low",
        "cracked_password": None
    }
    
    # Hash the password
    target_hash = hash_password(password, algorithm)
    attack_type = classify_password(password, username, fullname)
    
    cracked = False
    found_password = None
    
    # Dictionary attack
    if attack_type == "DICTIONARY":
        cracked, found_password = dictionary_attack(target_hash, algorithm)
        result["attack_used"] = "Dictionary"
    
    # Context-aware attack
    elif attack_type == "CONTEXT":
        result["attack_used"] = "Context-Aware Dictionary"
        candidates = []
        if username:
            candidates.append(username.lower())
        if fullname:
            candidates.extend(fullname.lower().split())
        
        for word in candidates:
            if hash_password(word, algorithm) == target_hash:
                cracked = True
                found_password = word
                break
    
    # Brute force attack
    elif attack_type == "BRUTE_FORCE":
        cracked, found_password = brute_force_attack(target_hash, algorithm)
        result["attack_used"] = "Brute Force"
    
    # Handle results
    if cracked:
        result["cracked"] = True
        result["password_strength"] = "Weak"
        result["cracked_password"] = found_password
    
    # AI Risk Analysis
    risk = analyze_password(password, username, fullname)
    result["ai_risk_level"] = risk
    
    # Adjust strength based on AI analysis if not cracked
    if not cracked:
        if risk == "High":
            result["password_strength"] = "Weak"
        elif risk == "Medium":
            result["password_strength"] = "Medium"
        else:
            result["password_strength"] = "Strong"
    
    # Store in session
    session.set("last_result", result)
    return result
