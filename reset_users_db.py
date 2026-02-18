import sqlite3
import os

def reset_users_database():
    """Delete old database and create fresh one"""
    db_path = "cases/users.db"
    
    # Delete old database
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Old database deleted")
    
    # Create new database with correct schema
    os.makedirs("cases", exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            app_password TEXT NOT NULL,
            verified INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ New database created with correct schema")
    print("\nYou can now run the application and signup!")

if __name__ == "__main__":
    reset_users_database()
