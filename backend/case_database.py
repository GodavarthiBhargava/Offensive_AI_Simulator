import sqlite3
import os
from datetime import datetime

def get_case_db_path(case_name):
    """Get database path for specific case"""
    case_dir = os.path.join("cases", case_name)
    os.makedirs(case_dir, exist_ok=True)
    return os.path.join(case_dir, "case_data.db")

def init_case_database(case_name):
    """Initialize all tables for a case"""
    db_path = get_case_db_path(case_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Password attacks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            password_value TEXT,
            password_type TEXT,
            attack_type TEXT,
            algorithm TEXT,
            result TEXT,
            cracked_password TEXT,
            timestamp TEXT
        )
    """)
    
    # Email analysis table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_type TEXT,
            sender TEXT,
            subject TEXT,
            content TEXT,
            risk_score INTEGER,
            classification TEXT,
            phishing_indicators TEXT,
            timestamp TEXT
        )
    """)
    
    # Domain verification table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS domain_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            ssl_valid INTEGER,
            dns_resolved INTEGER,
            is_spoofed INTEGER,
            risk_level TEXT,
            details TEXT,
            timestamp TEXT
        )
    """)
    
    # Phishing campaigns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phishing_campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_name TEXT,
            from_email TEXT,
            to_email TEXT,
            subject TEXT,
            template TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)
    
    # Voice analysis table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voice_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caller_name TEXT,
            scenario TEXT,
            risk_score INTEGER,
            manipulation_detected INTEGER,
            details TEXT,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# Password Attack Functions
def save_password_attack(case_name, first_name, last_name, password_value, password_type, 
                        attack_type, algorithm, result, cracked_password):
    init_case_database(case_name)
    db_path = get_case_db_path(case_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO password_attacks 
        (first_name, last_name, password_value, password_type, attack_type, algorithm, result, cracked_password, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, password_value, password_type, attack_type, algorithm, result, cracked_password, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_password_attacks(case_name):
    db_path = get_case_db_path(case_name)
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM password_attacks ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()
    return results

# Email Analysis Functions
def save_email_analysis(case_name, message_type, sender, subject, content, risk_score, classification, phishing_indicators):
    init_case_database(case_name)
    db_path = get_case_db_path(case_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO email_analysis 
        (message_type, sender, subject, content, risk_score, classification, phishing_indicators, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (message_type, sender, subject, content, risk_score, classification, phishing_indicators, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_email_analysis(case_name):
    db_path = get_case_db_path(case_name)
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM email_analysis ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()
    return results

# Domain Verification Functions
def save_domain_verification(case_name, domain, ssl_valid, dns_resolved, is_spoofed, risk_level, details):
    init_case_database(case_name)
    db_path = get_case_db_path(case_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO domain_verification 
        (domain, ssl_valid, dns_resolved, is_spoofed, risk_level, details, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (domain, ssl_valid, dns_resolved, is_spoofed, risk_level, details, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_domain_verification(case_name):
    db_path = get_case_db_path(case_name)
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM domain_verification ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()
    return results

# Phishing Campaign Functions
def save_phishing_campaign(case_name, from_name, from_email, to_email, subject, template, status):
    init_case_database(case_name)
    db_path = get_case_db_path(case_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO phishing_campaigns 
        (from_name, from_email, to_email, subject, template, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (from_name, from_email, to_email, subject, template, status, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_phishing_campaigns(case_name):
    db_path = get_case_db_path(case_name)
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phishing_campaigns ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()
    return results

# Voice Analysis Functions
def save_voice_analysis(case_name, caller_name, scenario, risk_score, manipulation_detected, details):
    init_case_database(case_name)
    db_path = get_case_db_path(case_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO voice_analysis 
        (caller_name, scenario, risk_score, manipulation_detected, details, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (caller_name, scenario, risk_score, manipulation_detected, details, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_voice_analysis(case_name):
    db_path = get_case_db_path(case_name)
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voice_analysis ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()
    return results

# Analytics Functions
def get_case_analytics(case_name):
    """Get comprehensive analytics for a case"""
    analytics = {
        "password_attacks": {
            "total": 0,
            "cracked": 0,
            "failed": 0,
            "crack_rate": 0
        },
        "email_analysis": {
            "total": 0,
            "phishing": 0,
            "suspicious": 0,
            "safe": 0,
            "avg_risk_score": 0
        },
        "domain_verification": {
            "total": 0,
            "high_risk": 0,
            "suspicious": 0,
            "safe": 0
        },
        "phishing_campaigns": {
            "total": 0,
            "sent": 0
        },
        "voice_analysis": {
            "total": 0,
            "high_risk": 0,
            "avg_risk_score": 0
        },
        "overall_risk_score": 0
    }
    
    # Password attacks
    pwd_attacks = get_password_attacks(case_name)
    analytics["password_attacks"]["total"] = len(pwd_attacks)
    analytics["password_attacks"]["cracked"] = sum(1 for a in pwd_attacks if a[7] == "Cracked")
    analytics["password_attacks"]["failed"] = analytics["password_attacks"]["total"] - analytics["password_attacks"]["cracked"]
    if analytics["password_attacks"]["total"] > 0:
        analytics["password_attacks"]["crack_rate"] = round((analytics["password_attacks"]["cracked"] / analytics["password_attacks"]["total"]) * 100, 1)
    
    # Email analysis
    emails = get_email_analysis(case_name)
    analytics["email_analysis"]["total"] = len(emails)
    for email in emails:
        if email[6] == "Phishing":
            analytics["email_analysis"]["phishing"] += 1
        elif email[6] == "Suspicious":
            analytics["email_analysis"]["suspicious"] += 1
        else:
            analytics["email_analysis"]["safe"] += 1
    if emails:
        analytics["email_analysis"]["avg_risk_score"] = round(sum(e[5] for e in emails) / len(emails), 1)
    
    # Domain verification
    domains = get_domain_verification(case_name)
    analytics["domain_verification"]["total"] = len(domains)
    for domain in domains:
        if domain[5] == "High Risk":
            analytics["domain_verification"]["high_risk"] += 1
        elif domain[5] == "Suspicious":
            analytics["domain_verification"]["suspicious"] += 1
        else:
            analytics["domain_verification"]["safe"] += 1
    
    # Phishing campaigns
    campaigns = get_phishing_campaigns(case_name)
    analytics["phishing_campaigns"]["total"] = len(campaigns)
    analytics["phishing_campaigns"]["sent"] = sum(1 for c in campaigns if c[6] == "Sent")
    
    # Voice analysis
    voices = get_voice_analysis(case_name)
    analytics["voice_analysis"]["total"] = len(voices)
    analytics["voice_analysis"]["high_risk"] = sum(1 for v in voices if v[3] >= 70)
    if voices:
        analytics["voice_analysis"]["avg_risk_score"] = round(sum(v[3] for v in voices) / len(voices), 1)
    
    # Calculate overall risk score
    risk_factors = []
    if analytics["password_attacks"]["total"] > 0:
        risk_factors.append(analytics["password_attacks"]["crack_rate"])
    if analytics["email_analysis"]["total"] > 0:
        risk_factors.append(analytics["email_analysis"]["avg_risk_score"])
    if analytics["voice_analysis"]["total"] > 0:
        risk_factors.append(analytics["voice_analysis"]["avg_risk_score"])
    
    if risk_factors:
        analytics["overall_risk_score"] = round(sum(risk_factors) / len(risk_factors), 1)
    
    return analytics
