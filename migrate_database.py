import sqlite3
import os

def migrate_database():
    """Add app_password column to existing users table"""
    db_path = "cases/users.db"
    
    if not os.path.exists(db_path):
        print("No existing database found. Will be created on first run.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if app_password column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'app_password' not in columns:
            print("Adding app_password column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN app_password TEXT DEFAULT ''")
            conn.commit()
            print("✅ Migration successful! app_password column added.")
        else:
            print("✅ Database already up to date.")
        
        conn.close()
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate_database()
