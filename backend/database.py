import sqlite3
import os
from datetime import datetime

DB_PATH = "database/case_records.db"

def init_database():
    """Initialize SQLite database and create table if not exists"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            password_type TEXT,
            attack_type TEXT,
            selected_algorithm TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_case_record(first_name, last_name, password_type, attack_type, selected_algorithm, result):
    """Save a case record to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO case_records 
        (first_name, last_name, password_type, attack_type, selected_algorithm, result, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, password_type, attack_type, selected_algorithm, result, timestamp))
    
    conn.commit()
    conn.close()

def get_all_records():
    """Retrieve all case records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM case_records ORDER BY id DESC')
    records = cursor.fetchall()
    
    conn.close()
    return records
