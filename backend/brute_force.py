import itertools
import hashlib

def brute_force_attack(
    target_value,
    password_type,
    algorithm=None,
    first_name=None,
    last_name=None,
    max_length=6,
    charset_type="lowercase_numbers",
    log_callback=None
):
    """Full brute force attack with personal info check and charset selection"""
    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)
    
    log("[INFO] Starting brute force attack...")
    
    charsets = {
        "lowercase": "abcdefghijklmnopqrstuvwxyz",
        "lowercase_numbers": "abcdefghijklmnopqrstuvwxyz0123456789",
        "full": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    }
    
    charset = charsets.get(charset_type, charsets["lowercase"])
    total_combinations = sum(len(charset) ** length for length in range(1, max_length + 1))
    
    log(f"[INFO] Max Length: {max_length}")
    log(f"[INFO] Charset: {charset_type}")
    log(f"[INFO] Total Combinations: {total_combinations:,}")
    
    if total_combinations > 3_000_000_000:
        log("[WARNING] Search space is very large. Execution may take significant time.")
        log("[INFO] Proceeding with attack...")
    
    # STEP 1: Personal Information Check
    if password_type == "Plain":
        if first_name and target_value.lower() == first_name.lower():
            log(f"[SUCCESS] Personal info match: {first_name}")
            return {"status": "CRACKED", "method": "Personal Info Match",
                    "password": target_value, "total_combinations": 0}
        if last_name and target_value.lower() == last_name.lower():
            log(f"[SUCCESS] Personal info match: {last_name}")
            return {"status": "CRACKED", "method": "Personal Info Match",
                    "password": target_value, "total_combinations": 0}
    
    log("[INFO] Personal info check complete. No match found.")
    log("[INFO] Executing brute force combinations...")
    log(f"[DEBUG] Entering brute force loop with max_length={max_length}, charset_type={charset_type}")
    
    # STEP 2: Execute Brute Force
    attempts = 0
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            guess = ''.join(attempt)
            attempts += 1
            
            if attempts <= 10:
                log(f"[DEBUG] Testing: {guess}")
            
            if attempts % 10000 == 0:
                log(f"[INFO] Checked {attempts} combinations...")
            
            if password_type == "Plain":
                if guess == target_value:
                    log(f"[SUCCESS] Brute force match found: {guess}")
                    return {"status": "CRACKED", "method": "Brute Force",
                            "password": guess, "total_combinations": attempts}
            
            elif password_type == "Hash":
                if algorithm == "MD5":
                    guess_hash = hashlib.md5(guess.encode()).hexdigest()
                elif algorithm == "SHA256":
                    guess_hash = hashlib.sha256(guess.encode()).hexdigest()
                elif algorithm == "SHA1":
                    guess_hash = hashlib.sha1(guess.encode()).hexdigest()
                else:
                    continue
                
                if guess_hash == target_value.lower():
                    log(f"[SUCCESS] Brute force match found: {guess}")
                    return {"status": "CRACKED", "method": "Brute Force",
                            "password": guess, "total_combinations": attempts}
    
    log(f"[INFO] Brute force complete. Checked {attempts} combinations.")
    log("[FAILED] No match found.")
    return {"status": "NOT CRACKED", "method": "Brute Force",
            "password": None, "total_combinations": attempts}
