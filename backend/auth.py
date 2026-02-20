"""
Authentication utilities for MedAssist Medical Chatbot
Handles password hashing and session management
"""

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for
import re


def hash_password(password: str) -> str:
    """
    Hash a password using werkzeug's security module
    """
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(stored_hash: str, provided_password: str) -> bool:
    """
    Verify a password against its hash
    """
    return check_password_hash(stored_hash, provided_password)


def validate_email(email: str) -> bool:
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""


def create_session(user: dict):
    """
    Create a user session
    """
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    session['user_email'] = user['email']
    session['is_authenticated'] = True


def clear_session():
    """
    Clear user session (logout)
    """
    session.clear()


def is_authenticated() -> bool:
    """
    Check if user is authenticated
    """
    return session.get('is_authenticated', False)


def get_current_user() -> dict:
    """
    Get current user info from session
    """
    if not is_authenticated():
        return None
    
    return {
        'id': session.get('user_id'),
        'name': session.get('user_name'),
        'email': session.get('user_email')
    }


def login_required(f):
    """
    Decorator to protect routes that require authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
