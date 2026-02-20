from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from chatbot.rule_engine import get_response
import database as db
import auth

app = Flask(__name__)
app.secret_key = 'medical_kiosk_secret_key_2026'

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================
# PUBLIC ROUTES
# ============================================

@app.route('/')
def home():
    """Landing page for guests"""
    if auth.is_authenticated():
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/chat')
def chat_page():
    """Chatbot interface (accessible to both guests and logged-in users)"""
    user = auth.get_current_user()
    return render_template('chatbot.html', user=user)


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if auth.is_authenticated():
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validate input
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password required"}), 400
        
        # Get user from database
        user = db.get_user_by_email(email)
        
        if not user:
            return jsonify({"success": False, "message": "Invalid email or password"}), 401
        
        # Verify password
        if not auth.verify_password(user['password'], password):
            return jsonify({"success": False, "message": "Invalid email or password"}), 401
        
        # Create session
        auth.create_session(user)
        
        return jsonify({"success": True, "redirect": "/dashboard"})
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Registration page and handler"""
    if auth.is_authenticated():
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validate input
        if not name or not email or not password:
            return jsonify({"success": False, "message": "All fields are required"}), 400
        
        if not auth.validate_email(email):
            return jsonify({"success": False, "message": "Invalid email format"}), 400
        
        is_valid, error_msg = auth.validate_password(password)
        if not is_valid:
            return jsonify({"success": False, "message": error_msg}), 400
        
        # Check if email already exists
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({"success": False, "message": "Email already registered"}), 409
        
        # Hash password and create user
        hashed_password = auth.hash_password(password)
        user_id = db.create_user(name, email, hashed_password)
        
        if user_id:
            # Auto-login after registration
            user = db.get_user_by_id(user_id)
            auth.create_session(user)
            return jsonify({"success": True, "redirect": "/dashboard"})
        else:
            return jsonify({"success": False, "message": "Registration failed"}), 500
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    """Logout user and clear session"""
    auth.clear_session()
    return redirect(url_for('home'))


# ============================================
# PROTECTED ROUTES
# ============================================

@app.route('/dashboard')
@auth.login_required
def dashboard():
    """User dashboard (protected)"""
    user = auth.get_current_user()
    return render_template('dashboard.html', user=user)


@app.route('/api/dashboard-data')
@auth.login_required
def dashboard_data():
    """API endpoint to get dashboard statistics"""
    user = auth.get_current_user()
    stats = db.get_dashboard_stats(user['id'])
    
    return jsonify({
        "success": True,
        "data": {
            "name": user['name'],
            "email": user['email'],
            "total_chats": stats['total_chats'],
            "recent_symptoms": stats['recent_symptoms'],
            "recent_chats": stats['recent_chats']
        }
    })


# ============================================
# PROFILE ROUTES
# ============================================

@app.route('/profile')
@auth.login_required
def profile():
    """User profile page (protected)"""
    user_id = session.get('user_id')
    user = db.get_user_by_id(user_id)
    return render_template('profile.html', user=user)


@app.route('/api/profile/update', methods=['POST'])
@auth.login_required
def update_profile():
    """Update user profile information"""
    data = request.json
    user_id = session.get('user_id')
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    
    # Validate input
    if not name or not email:
        return jsonify({"success": False, "message": "Name and email are required"}), 400
    
    if not auth.validate_email(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400
    
    # Update profile
    success = db.update_user_profile(user_id, name, email)
    
    if not success:
        return jsonify({"success": False, "message": "Email already in use"}), 409
    
    # Update session
    session['user_name'] = name
    session['user_email'] = email
    
    return jsonify({"success": True, "message": "Profile updated successfully"})


@app.route('/api/profile/update-password', methods=['POST'])
@auth.login_required
def update_password():
    """Update user password"""
    data = request.json
    user_id = session.get('user_id')
    
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    
    # Validate input
    if not current_password or not new_password or not confirm_password:
        return jsonify({"success": False, "message": "All fields are required"}), 400
    
    if new_password != confirm_password:
        return jsonify({"success": False, "message": "New passwords do not match"}), 400
    
    # Validate new password strength
    is_valid, error_msg = auth.validate_password(new_password)
    if not is_valid:
        return jsonify({"success": False, "message": error_msg}), 400
    
    # Verify current password
    user = db.get_user_by_id(user_id)
    if not auth.verify_password(user['password'], current_password):
        return jsonify({"success": False, "message": "Current password is incorrect"}), 401
    
    # Update password
    hashed_password = auth.hash_password(new_password)
    success = db.update_user_password(user_id, hashed_password)
    
    if success:
        return jsonify({"success": True, "message": "Password updated successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to update password"}), 500


@app.route('/api/profile/upload-image', methods=['POST'])
@auth.login_required
def upload_profile_image():
    """Upload profile picture"""
    user_id = session.get('user_id')
    
    # Check if file is present
    if 'profile_image' not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400
    
    file = request.files['profile_image']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Invalid file type. Only JPG, JPEG, and PNG are allowed"}), 400
    
    # Create secure filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    extension = file.filename.rsplit('.', 1)[1].lower()
    filename = f"user_{user_id}_{timestamp}.{extension}"
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Store relative path in database
    relative_path = f"/static/uploads/{filename}"
    success = db.update_profile_image(user_id, relative_path)
    
    if success:
        return jsonify({
            "success": True, 
            "message": "Profile image uploaded successfully",
            "image_path": relative_path
        })
    else:
        return jsonify({"success": False, "message": "Failed to update profile image"}), 500


# ============================================
# CHATBOT API
# ============================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    Saves to database if user is logged in
    """
    user_msg = request.json.get('message', '')
    
    if not user_msg:
        return jsonify({"error": "Message required"}), 400
    
    # Get bot response
    reply = get_response(user_msg)
    
    # Save to database if user is logged in
    if auth.is_authenticated():
        user = auth.get_current_user()
        db.save_chat(user['id'], user_msg, reply)
    
    return jsonify({
        "reply": reply,
        "timestamp": datetime.now().isoformat()
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

