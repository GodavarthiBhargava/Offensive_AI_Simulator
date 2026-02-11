import sqlite3
import os
from datetime import datetime
import uuid

DB_PATH = "cases/attack_results.db"

def init_database():
    """Initialize SQLite database with attack results table"""
    os.makedirs("cases", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attack_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT,
            first_name TEXT,
            last_name TEXT,
            password_value TEXT,
            password_type TEXT,
            attack_type TEXT,
            selected_algorithm TEXT,
            charset_type TEXT,
            max_length INTEGER,
            total_combinations INTEGER,
            result TEXT,
            cracked_password TEXT,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def generate_case_id():
    """Generate unique case ID"""
    return f"CASE-{uuid.uuid4().hex[:8].upper()}"

def save_case_record(case_id, first_name, last_name, password_value, password_type, 
                    attack_type, algorithm, result, cracked_password):
    """Save case record to database"""
    init_database()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO attack_results (
            case_id, first_name, last_name, password_value, password_type, attack_type,
            selected_algorithm, result, cracked_password, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id, first_name, last_name, password_value, password_type, attack_type,
        algorithm, result, cracked_password, datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def store_attack_result(
    first_name=None,
    last_name=None,
    password_type=None,
    attack_type=None,
    selected_algorithm=None,
    charset_type=None,
    max_length=None,
    total_combinations=None,
    result=None,
    cracked_password=None
):
    """Store attack result in database"""
    init_database()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO attack_results (
            first_name, last_name, password_type, attack_type,
            selected_algorithm, charset_type, max_length,
            total_combinations, result, cracked_password, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        first_name, last_name, password_type, attack_type,
        selected_algorithm, charset_type, max_length,
        total_combinations, result, cracked_password,
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def get_all_cases():
    """Retrieve all cases from database"""
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM attack_results
        ORDER BY timestamp DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def delete_case(case_id):
    """Delete a case from database"""
    if not os.path.exists(DB_PATH):
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM attack_results WHERE case_id = ?", (case_id,))
    
    conn.commit()
    conn.close()

def get_attack_history(limit=50):
    """Retrieve attack history from database"""
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM attack_results
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results
