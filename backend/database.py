"""
Database operations for MedAssist Medical Chatbot
Handles user management and chat history storage
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

# Database file in project root for persistence across local and hosted environments
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')  # Better concurrency
    conn.execute('PRAGMA foreign_keys=ON')   # Enforce foreign keys
    return conn


def _migrate_password_column():
    """Migrate old 'password' column to 'password_hash' if needed"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'password' in columns and 'password_hash' not in columns:
        print("[DB Migration] Renaming 'password' column to 'password_hash'...")
        cursor.execute('ALTER TABLE users RENAME COLUMN password TO password_hash')
        conn.commit()
        print("[DB Migration] Done.")
    conn.close()


def init_database():
    """Initialize database with required tables"""
    # Migrate old DB file to new location if it exists
    old_db = os.path.join(os.path.dirname(__file__), 'medical_chatbot.db')
    if os.path.exists(old_db) and not os.path.exists(DB_PATH):
        import shutil
        print(f"[DB Migration] Moving database to project root: {DB_PATH}")
        shutil.copy2(old_db, DB_PATH)
        os.rename(old_db, old_db + '.bak')  # Keep backup
        print("[DB Migration] Old database backed up as medical_chatbot.db.bak")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
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
    
    # Create chat_sessions table for storing chat conversations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL DEFAULT 'New Chat',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create chat_messages table for storing individual messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'bot')),
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
        )
    ''')
    
    # Create health_tracker table for tracking user health metrics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight REAL,
            blood_pressure TEXT,
            heart_rate INTEGER,
            calories INTEGER,
            water_intake REAL,
            sleep_hours REAL,
            notes TEXT,
            date_created DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create health_reports table for community health awareness posts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            image_path TEXT,
            ai_formatted_message TEXT,
            twitter_post_id TEXT,
            status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'posted', 'failed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

    # Migrate password column name if upgrading from old schema
    _migrate_password_column()


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
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
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
            'UPDATE users SET password_hash = ? WHERE id = ?',
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


# ============================================
# CHAT SESSION OPERATIONS
# ============================================

def create_chat_session(user_id: int, title: str = "New Chat") -> Optional[int]:
    """
    Create a new chat session
    Returns session ID if successful, None otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_sessions (user_id, title) VALUES (?, ?)',
            (user_id, title)
        )
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    except sqlite3.Error:
        return None


def get_user_chat_sessions(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Get all chat sessions for a user
    Returns list of session dictionaries ordered by most recent
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT id, title, created_at, updated_at 
           FROM chat_sessions 
           WHERE user_id = ? 
           ORDER BY updated_at DESC 
           LIMIT ?''',
        (user_id, limit)
    )
    sessions = cursor.fetchall()
    conn.close()
    return [dict(session) for session in sessions]


def get_chat_session(session_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific chat session by ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat_sessions WHERE id = ?', (session_id,))
    session = cursor.fetchone()
    conn.close()
    return dict(session) if session else None


def update_chat_session_title(session_id: int, title: str) -> bool:
    """
    Update the title of a chat session
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE chat_sessions SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (title, session_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error:
        return False


def update_chat_session_timestamp(session_id: int) -> bool:
    """
    Update the updated_at timestamp of a chat session
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (session_id,)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error:
        return False


def delete_chat_session(session_id: int, user_id: int) -> bool:
    """
    Delete a chat session (only if it belongs to the user)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM chat_sessions WHERE id = ? AND user_id = ?',
            (session_id, user_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error:
        return False


def save_chat_message(session_id: int, role: str, message: str) -> Optional[int]:
    """
    Save a message to a chat session
    role should be 'user' or 'bot'
    Returns message ID if successful
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_messages (session_id, role, message) VALUES (?, ?, ?)',
            (session_id, role, message)
        )
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Update session timestamp
        update_chat_session_timestamp(session_id)
        
        return message_id
    except sqlite3.Error:
        return None


def get_session_messages(session_id: int) -> List[Dict[str, Any]]:
    """
    Get all messages for a specific session
    Returns list of message dictionaries ordered by creation time
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT id, role, message, created_at 
           FROM chat_messages 
           WHERE session_id = ? 
           ORDER BY created_at ASC''',
        (session_id,)
    )
    messages = cursor.fetchall()
    conn.close()
    return [dict(msg) for msg in messages]


def generate_chat_title(first_user_message: str) -> str:
    """
    Generate a chat title from the first user message
    Takes first 5 words or 50 characters, whichever is shorter
    """
    if not first_user_message:
        return "New Chat"
    
    # Clean the message
    message = first_user_message.strip()
    
    # Take first 5 words
    words = message.split()[:5]
    title = ' '.join(words)
    
    # Limit to 50 characters
    if len(title) > 50:
        title = title[:47] + '...'
    
    # Capitalize first letter
    if title:
        title = title[0].upper() + title[1:]
    
    return title if title else "New Chat"


# ============================================
# HEALTH TRACKER OPERATIONS
# ============================================

def add_health_entry(user_id: int, weight: Optional[float] = None, 
                    blood_pressure: Optional[str] = None, 
                    heart_rate: Optional[int] = None,
                    calories: Optional[int] = None, 
                    water_intake: Optional[float] = None,
                    sleep_hours: Optional[float] = None, 
                    notes: Optional[str] = None,
                    date_created: Optional[str] = None) -> Optional[int]:
    """
    Add a new health tracker entry
    Returns entry ID if successful, None otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if date_created:
            cursor.execute(
                '''INSERT INTO health_tracker 
                   (user_id, weight, blood_pressure, heart_rate, calories, 
                    water_intake, sleep_hours, notes, date_created) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id, weight, blood_pressure, heart_rate, calories, 
                 water_intake, sleep_hours, notes, date_created)
            )
        else:
            cursor.execute(
                '''INSERT INTO health_tracker 
                   (user_id, weight, blood_pressure, heart_rate, calories, 
                    water_intake, sleep_hours, notes) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id, weight, blood_pressure, heart_rate, calories, 
                 water_intake, sleep_hours, notes)
            )
        
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return entry_id
    except sqlite3.Error as e:
        print(f"Error adding health entry: {e}")
        return None


def get_user_health_entries(user_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get all health entries for a user, ordered by date (newest first)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute(
            '''SELECT * FROM health_tracker 
               WHERE user_id = ? 
               ORDER BY date_created DESC, created_at DESC 
               LIMIT ?''',
            (user_id, limit)
        )
    else:
        cursor.execute(
            '''SELECT * FROM health_tracker 
               WHERE user_id = ? 
               ORDER BY date_created DESC, created_at DESC''',
            (user_id,)
        )
    
    entries = cursor.fetchall()
    conn.close()
    return [dict(entry) for entry in entries]


def get_health_summary(user_id: int) -> Dict[str, Any]:
    """
    Get health summary statistics for a user
    Returns latest weight, average calories, average sleep, and total entries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get latest weight
    cursor.execute(
        '''SELECT weight FROM health_tracker 
           WHERE user_id = ? AND weight IS NOT NULL 
           ORDER BY date_created DESC, created_at DESC 
           LIMIT 1''',
        (user_id,)
    )
    latest_weight_row = cursor.fetchone()
    latest_weight = latest_weight_row[0] if latest_weight_row else None
    
    # Get average calories
    cursor.execute(
        '''SELECT AVG(calories) FROM health_tracker 
           WHERE user_id = ? AND calories IS NOT NULL''',
        (user_id,)
    )
    avg_calories_row = cursor.fetchone()
    avg_calories = round(avg_calories_row[0], 1) if avg_calories_row[0] else None
    
    # Get average sleep hours
    cursor.execute(
        '''SELECT AVG(sleep_hours) FROM health_tracker 
           WHERE user_id = ? AND sleep_hours IS NOT NULL''',
        (user_id,)
    )
    avg_sleep_row = cursor.fetchone()
    avg_sleep = round(avg_sleep_row[0], 1) if avg_sleep_row[0] else None
    
    # Get total entries count
    cursor.execute(
        'SELECT COUNT(*) FROM health_tracker WHERE user_id = ?',
        (user_id,)
    )
    total_entries = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'latest_weight': latest_weight,
        'avg_calories': avg_calories,
        'avg_sleep': avg_sleep,
        'total_entries': total_entries
    }


def get_health_chart_data(user_id: int, days: int = 30) -> Dict[str, Any]:
    """
    Get health data for charts (last N days)
    Returns data formatted for Chart.js
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        '''SELECT date_created, weight, calories, sleep_hours 
           FROM health_tracker 
           WHERE user_id = ? 
           ORDER BY date_created ASC 
           LIMIT ?''',
        (user_id, days)
    )
    
    entries = cursor.fetchall()
    conn.close()
    
    dates = []
    weights = []
    calories_list = []
    sleep_list = []
    
    for entry in entries:
        dates.append(entry[0])
        weights.append(entry[1] if entry[1] is not None else None)
        calories_list.append(entry[2] if entry[2] is not None else None)
        sleep_list.append(entry[3] if entry[3] is not None else None)
    
    return {
        'dates': dates,
        'weights': weights,
        'calories': calories_list,
        'sleep': sleep_list
    }


def delete_health_entry(entry_id: int, user_id: int) -> bool:
    """
    Delete a health entry (only if it belongs to the user)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM health_tracker WHERE id = ? AND user_id = ?',
            (entry_id, user_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error as e:
        print(f"Error deleting health entry: {e}")
        return False


# ============================================
# HEALTH REPORTS OPERATIONS
# ============================================

def add_health_report(user_id: int, description: str, image_path: Optional[str] = None, 
                      ai_formatted_message: Optional[str] = None) -> Optional[int]:
    """
    Add a new health report to the database
    
    Args:
        user_id: ID of the user creating the report
        description: Original health issue description
        image_path: Path to uploaded image (optional)
        ai_formatted_message: AI-formatted message (optional)
    
    Returns:
        Report ID if successful, None otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO health_reports (user_id, description, image_path, ai_formatted_message, status)
            VALUES (?, ?, ?, ?, 'draft')
        ''', (user_id, description, image_path, ai_formatted_message))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return report_id
    except sqlite3.Error as e:
        print(f"Error adding health report: {e}")
        return None


def update_health_report_twitter_post(report_id: int, twitter_post_id: str) -> bool:
    """
    Update health report with Twitter post ID after successful posting
    
    Args:
        report_id: ID of the health report
        twitter_post_id: Twitter post/tweet ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE health_reports
            SET twitter_post_id = ?, status = 'posted'
            WHERE id = ?
        ''', (twitter_post_id, report_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error as e:
        print(f"Error updating Twitter post ID: {e}")
        return False


def update_health_report_status(report_id: int, status: str) -> bool:
    """
    Update health report status
    
    Args:
        report_id: ID of the health report
        status: New status ('draft', 'posted', 'failed')
    
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE health_reports
            SET status = ?
            WHERE id = ?
        ''', (status, report_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error as e:
        print(f"Error updating report status: {e}")
        return False


def get_user_health_reports(user_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get all health reports for a specific user
    
    Args:
        user_id: User ID
        limit: Maximum number of reports to return (optional)
    
    Returns:
        List of health reports as dictionaries
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, user_id, description, image_path, ai_formatted_message, 
                   twitter_post_id, status, created_at
            FROM health_reports
            WHERE user_id = ?
            ORDER BY created_at DESC
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in rows:
            reports.append({
                'id': row['id'],
                'user_id': row['user_id'],
                'description': row['description'],
                'image_path': row['image_path'],
                'ai_formatted_message': row['ai_formatted_message'],
                'twitter_post_id': row['twitter_post_id'],
                'status': row['status'],
                'created_at': row['created_at']
            })
        
        return reports
    except sqlite3.Error as e:
        print(f"Error fetching user health reports: {e}")
        return []


def get_health_report_by_id(report_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific health report by ID
    
    Args:
        report_id: Report ID
    
    Returns:
        Health report as dictionary or None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, description, image_path, ai_formatted_message, 
                   twitter_post_id, status, created_at
            FROM health_reports
            WHERE id = ?
        ''', (report_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'user_id': row['user_id'],
                'description': row['description'],
                'image_path': row['image_path'],
                'ai_formatted_message': row['ai_formatted_message'],
                'twitter_post_id': row['twitter_post_id'],
                'status': row['status'],
                'created_at': row['created_at']
            }
        return None
    except sqlite3.Error as e:
        print(f"Error fetching health report: {e}")
        return None


# Initialize database on module import
init_database()
