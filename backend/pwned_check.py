"""
PwnedCheck Module - Have I Been Pwned Password Checker
Checks passwords against the Pwned Passwords API using k-Anonymity model
"""

import hashlib
import requests
from typing import Dict

def get_risk_level(count: int) -> str:
    """Determine risk level based on exposure count"""
    if count <= 10:
        return "Low"
    elif count <= 1000:
        return "Medium"
    else:
        return "High"

def check_password_exposure(password: str) -> Dict[str, any]:
    """
    Check if password has been exposed in data breaches using Have I Been Pwned API
    
    Args:
        password (str): Password to check
        
    Returns:
        dict: {
            "found": bool,
            "exposure_count": int,
            "risk_level": str,
            "message": str
        }
    """
    try:
        # Convert password to SHA-1 hash (uppercase)
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        
        # Split hash: first 5 chars for API, remaining for comparison
        hash_prefix = sha1_hash[:5]
        hash_suffix = sha1_hash[5:]
        
        # Query Pwned Passwords API with k-Anonymity model
        api_url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
        
        # Make API request with timeout
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        # Parse response - each line contains hash_suffix:count
        hash_lines = response.text.splitlines()
        
        # Search for our hash suffix in the results
        for line in hash_lines:
            if ':' in line:
                returned_suffix, count = line.split(':', 1)
                
                # Compare hash suffixes (case-insensitive)
                if returned_suffix.upper() == hash_suffix:
                    exposure_count = int(count)
                    risk_level = get_risk_level(exposure_count)
                    
                    return {
                        "found": True,
                        "exposure_count": exposure_count,
                        "risk_level": risk_level,
                        "message": f"Password exposed {exposure_count:,} times. Risk: {risk_level}"
                    }
        
        # Password not found in breaches
        return {
            "found": False,
            "exposure_count": 0,
            "risk_level": "None",
            "message": "Password not found in breach database."
        }
        
    except requests.exceptions.Timeout:
        return {
            "found": False,
            "exposure_count": 0,
            "risk_level": "Unknown",
            "message": "Request timeout. Please try again."
        }
        
    except requests.exceptions.ConnectionError:
        return {
            "found": False,
            "exposure_count": 0,
            "risk_level": "Unknown",
            "message": "Network error. Check internet connection."
        }
        
    except requests.exceptions.HTTPError as e:
        return {
            "found": False,
            "exposure_count": 0,
            "risk_level": "Unknown",
            "message": f"API error: {e.response.status_code}"
        }
        
    except Exception as e:
        return {
            "found": False,
            "exposure_count": 0,
            "risk_level": "Unknown",
            "message": f"Unexpected error: {str(e)}"
        }
