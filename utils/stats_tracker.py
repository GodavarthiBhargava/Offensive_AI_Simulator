import sqlite3
import os
from datetime import datetime

DB_PATH = "cases/phishing_stats.db"

def _init_db():
    os.makedirs("cases", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS phishing_campaigns
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  target TEXT,
                  template TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def record_phishing_sent(target, template):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO phishing_campaigns (target, template, timestamp) VALUES (?, ?, ?)",
              (target, template, datetime.now().isoformat()))
    conn.commit()
    conn.close()
