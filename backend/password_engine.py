from backend.hashing import hash_password
from backend.dictionary_attack import dictionary_attack
from backend.brute_force import brute_force_attack
from backend.ai_analyzer import analyze_password
from backend.session_store import session

def simulate_password_attack(credential, algorithm, input_mode="password", username="", fullname=""):
    """Master controller for password attack simulation"""
    result = {
        "cracked": False,
        "attack_used": "None",
        "password_strength": "Strong",
        "ai_risk_level": "Low",
        "cracked_password": None
    }
    
    # Determine target hash based on input mode
    if input_mode == "password":
        password = credential
        target_hash = hash_password(password, algorithm)
    else:  # hash mode
        target_hash = credential.lower()
        password = None  # Unknown password
    
    # Try dictionary attack
    cracked, found_password = dictionary_attack(target_hash, algorithm)
    if cracked:
        result["cracked"] = True
        result["attack_used"] = "Dictionary"
        result["password_strength"] = "Weak"
        result["cracked_password"] = found_password
        password = found_password  # Use cracked password for AI analysis
    else:
        # Try brute force (only if we know it's numeric and <= 4 chars)
        if password and password.isdigit() and len(password) <= 4:
            cracked, found_password = brute_force_attack(target_hash, algorithm)
            if cracked:
                result["cracked"] = True
                result["attack_used"] = "BruteForce"
                result["password_strength"] = "Weak"
                result["cracked_password"] = found_password
    
    # AI risk analysis (only if password is known)
    if password:
        result["ai_risk_level"] = analyze_password(password, username, fullname)
        
        # Determine password strength if not cracked
        if not result["cracked"]:
            if result["ai_risk_level"] == "High":
                result["password_strength"] = "Weak"
            elif result["ai_risk_level"] == "Medium":
                result["password_strength"] = "Medium"
            else:
                result["password_strength"] = "Strong"
    else:
        # Hash mode without cracking - cannot analyze
        result["ai_risk_level"] = "Unknown"
        result["password_strength"] = "Unknown"
    
    # Store in session
    session.set("last_result", result)
    
    return result
