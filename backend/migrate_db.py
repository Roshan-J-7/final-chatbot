"""
Database Migration Script
Adds profile_image_path column to existing users table
Run this once if you have an existing database
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

def migrate_database():
    """Add profile_image_path column to users table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profile_image_path' not in columns:
            print("Adding profile_image_path column to users table...")
            cursor.execute('ALTER TABLE users ADD COLUMN profile_image_path TEXT DEFAULT NULL')
            conn.commit()
            print("✓ Migration completed successfully!")
        else:
            print("✓ Column profile_image_path already exists. No migration needed.")
    
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
