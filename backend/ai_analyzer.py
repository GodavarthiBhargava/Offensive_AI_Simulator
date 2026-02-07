import re

def analyze_password(password, username="", fullname=""):
    """Rule-based AI analysis of password strength with user context"""
    risk_score = 0
    
    # Length check
    if len(password) < 6:
        risk_score += 3
    elif len(password) < 8:
        risk_score += 2
    elif len(password) < 12:
        risk_score += 1
    
    # Numeric only
    if password.isdigit():
        risk_score += 3
    
    # Common patterns
    common_patterns = ['123', 'password', 'admin', 'qwerty', '000', '111']
    if any(pattern in password.lower() for pattern in common_patterns):
        risk_score += 2
    
    # No uppercase
    if not any(c.isupper() for c in password):
        risk_score += 1
    
    # No special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        risk_score += 1
    
    # User context analysis
    password_lower = password.lower()
    
    # Check if username appears in password
    if username and len(username) >= 3 and username.lower() in password_lower:
        risk_score += 2
    
    # Check if name appears in password
    if fullname:
        name_parts = fullname.lower().split()
        for part in name_parts:
            if len(part) >= 3 and part in password_lower:
                risk_score += 2
                break
    
    # Determine risk level
    if risk_score >= 6:
        return "High"
    elif risk_score >= 3:
        return "Medium"
    else:
        return "Low"
