import sqlite3
import os
from datetime import datetime

DB_PATH = "database/forensics_cases.db"

def init_database():
    """Initialize SQLite database and create table if not exists"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            password_input TEXT,
            password_type TEXT,
            attack_type TEXT,
            selected_algorithm TEXT,
            result TEXT,
            cracked_password TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_case_id():
    """Generate unique case ID like CASE2026_001"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    year = datetime.now().year
    cursor.execute('SELECT COUNT(*) FROM case_records WHERE case_id LIKE ?', (f'CASE{year}_%',))
    count = cursor.fetchone()[0]
    
    conn.close()
    return f"CASE{year}_{str(count + 1).zfill(3)}"

def save_case_record(case_id, first_name, last_name, password_input, password_type, 
                    attack_type, selected_algorithm, result, cracked_password):
    """Save a case record to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO case_records 
        (case_id, first_name, last_name, password_input, password_type, attack_type, 
         selected_algorithm, result, cracked_password, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (case_id, first_name, last_name, password_input, password_type, attack_type, 
          selected_algorithm, result, cracked_password, timestamp))
    
    conn.commit()
    conn.close()

def get_all_cases():
    """Retrieve all case records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM case_records ORDER BY id DESC')
    records = cursor.fetchall()
    
    conn.close()
    return records

def get_case_by_id(case_id):
    """Get specific case by case_id"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM case_records WHERE case_id = ?', (case_id,))
    record = cursor.fetchone()
    
    conn.close()
    return record

def search_cases(search_term=None, attack_type=None, result=None, password_type=None):
    """Search and filter cases"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = 'SELECT * FROM case_records WHERE 1=1'
    params = []
    
    if search_term:
        query += ' AND (first_name LIKE ? OR last_name LIKE ? OR case_id LIKE ?)'
        params.extend([f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'])
    
    if attack_type:
        query += ' AND attack_type = ?'
        params.append(attack_type)
    
    if result:
        query += ' AND result = ?'
        params.append(result)
    
    if password_type:
        query += ' AND password_type = ?'
        params.append(password_type)
    
    query += ' ORDER BY id DESC'
    
    cursor.execute(query, params)
    records = cursor.fetchall()
    
    conn.close()
    return records

def get_case_history(first_name, last_name):
    """Get all attempts for a specific person"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM case_records 
        WHERE first_name = ? AND last_name = ?
        ORDER BY timestamp DESC
    ''', (first_name, last_name))
    
    records = cursor.fetchall()
    conn.close()
    return records
