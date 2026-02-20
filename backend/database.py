"""
Database operations for MedAssist Medical Chatbot
Handles user management and chat history storage
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), 'medical_chatbot.db')


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile_image_path TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()


# ============================================
# USER OPERATIONS
# ============================================

def create_user(name: str, email: str, hashed_password: str) -> Optional[int]:
    """
    Create a new user account
    Returns user_id if successful, None if email exists
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve user by email address
    Returns user dict or None if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve user by ID
    Returns user dict or None if not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None


def update_user_profile(user_id: int, name: str, email: str) -> bool:
    """
    Update user's name and email
    Returns True if successful, False if email already exists
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET name = ?, email = ? WHERE id = ?',
            (name, email, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def update_user_password(user_id: int, hashed_password: str) -> bool:
    """
    Update user's password
    Returns True if successful
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (hashed_password, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False


def update_profile_image(user_id: int, image_path: str) -> bool:
    """
    Update user's profile image path
    Returns True if successful
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET profile_image_path = ? WHERE id = ?',
            (image_path, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating profile image: {e}")
        return False


# ============================================
# CHAT HISTORY OPERATIONS
# ============================================

def save_chat(user_id: int, user_message: str, bot_response: str) -> bool:
    """
    Save chat interaction to database
    Returns True if successful
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)',
            (user_id, user_message, bot_response)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving chat: {e}")
        return False


def get_user_chats(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieve chat history for a user
    Returns list of chat dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
        (user_id, limit)
    )
    chats = cursor.fetchall()
    conn.close()
    
    return [dict(chat) for chat in chats]


def get_user_chat_count(user_id: int) -> int:
    """
    Get total number of chats for a user
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM chat_history WHERE user_id = ?', (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_recent_symptoms(user_id: int, limit: int = 10) -> List[str]:
    """
    Extract recent symptoms mentioned by user
    Returns list of unique symptom keywords
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT user_message FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
        (user_id, limit)
    )
    messages = cursor.fetchall()
    conn.close()
    
    # Extract symptom keywords (simple approach)
    symptom_keywords = set()
    common_symptoms = [
        'fever', 'headache', 'cough', 'cold', 'pain', 'nausea', 
        'fatigue', 'dizziness', 'chest', 'stomach', 'throat', 'back'
    ]
    
    for msg in messages:
        text = msg[0].lower()
        for symptom in common_symptoms:
            if symptom in text:
                symptom_keywords.add(symptom)
    
    return list(symptom_keywords)


def get_dashboard_stats(user_id: int) -> Dict[str, Any]:
    """
    Get comprehensive dashboard statistics for user
    """
    chat_count = get_user_chat_count(user_id)
    recent_chats = get_user_chats(user_id, limit=5)
    recent_symptoms = get_recent_symptoms(user_id, limit=20)
    
    return {
        'total_chats': chat_count,
        'recent_chats': recent_chats,
        'recent_symptoms': recent_symptoms[:5]  # Limit to 5 most recent
    }


# Initialize database on module import
init_database()
