from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from chatbot.rule_engine import get_response
import database as db
import auth
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'medical_kiosk_secret_key_2026'

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# API Keys
CEREBRAS_API_KEY = os.getenv('CEREBRAS_API_KEY', '')

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
        if not auth.verify_password(user['password_hash'], password):
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
    if not auth.verify_password(user['password_hash'], current_password):
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
# HEALTH TRACKER
# ============================================

@app.route('/health-tracker')
@auth.login_required
def health_tracker():
    """Health Tracker page (protected)"""
    user_id = session.get('user_id')
    user = db.get_user_by_id(user_id)
    return render_template('health_tracker.html', user=user)


# ============================================
# COMMUNITY
# ============================================

@app.route('/community')
@auth.login_required
def community():
    """Community page (protected)"""
    user_id = session.get('user_id')
    user = db.get_user_by_id(user_id)
    return render_template('community.html', user=user)


# ============================================
# HEALTH REPORTING (Community Awareness)
# ============================================

def format_message_locally(description: str) -> str:
    """
    Local text formatter - cleans up text without AI.
    Capitalizes sentences, adds punctuation, generates relevant hashtags.
    """
    text = description.strip()
    
    # Capitalize first letter of each sentence
    sentences = re.split(r'([.!?]+)', text)
    cleaned = []
    for i, part in enumerate(sentences):
        part = part.strip()
        if part and not re.match(r'^[.!?]+$', part):
            part = part[0].upper() + part[1:] if len(part) > 1 else part.upper()
            cleaned.append(part)
        elif part:
            cleaned.append(part)
    
    text = ' '.join(cleaned) if cleaned else text.capitalize()
    
    # Ensure it ends with punctuation
    if text and text[-1] not in '.!?':
        text += '.'
    
    # Generate relevant hashtags based on keywords
    hashtag_map = {
        'water': '#CleanWater', 'drink': '#CleanWater',
        'dengue': '#DenguePrevention', 'mosquito': '#MosquitoControl',
        'fever': '#FeverAlert', 'malaria': '#MalariaPrevention',
        'medicine': '#MedicineAccess', 'drug': '#MedicineAccess',
        'doctor': '#HealthcareAccess', 'hospital': '#HealthcareAccess', 'clinic': '#HealthcareAccess',
        'food': '#FoodSafety', 'hunger': '#FoodSecurity',
        'pollution': '#AirQuality', 'air': '#AirQuality', 'smoke': '#AirQuality',
        'covid': '#COVID19', 'vaccine': '#Vaccination', 'vaccination': '#Vaccination',
        'diarrhea': '#WaterborneDisease', 'cholera': '#WaterborneDisease',
        'child': '#ChildHealth', 'children': '#ChildHealth', 'baby': '#ChildHealth',
        'pregnant': '#MaternalHealth', 'pregnancy': '#MaternalHealth',
        'mental': '#MentalHealth', 'stress': '#MentalHealth', 'anxiety': '#MentalHealth',
        'sanitation': '#Sanitation', 'toilet': '#Sanitation', 'sewage': '#Sanitation',
    }
    
    desc_lower = description.lower()
    found_hashtags = set()
    for keyword, hashtag in hashtag_map.items():
        if keyword in desc_lower:
            found_hashtags.add(hashtag)
    
    # Always add general health hashtags
    found_hashtags.add('#PublicHealth')
    found_hashtags.add('#CommunityHealth')
    
    # Limit to 4 hashtags
    hashtags = list(found_hashtags)[:4]
    
    result = f"{text}\n\n{' '.join(hashtags)}"
    
    # Trim to 280 characters
    if len(result) > 280:
        max_text_len = 280 - len('\n\n' + ' '.join(hashtags))
        text = text[:max_text_len - 3] + '...'
        result = f"{text}\n\n{' '.join(hashtags)}"
    
    return result


def format_message_with_ai(description: str) -> tuple:
    """
    Use Cerebras API to format health issue description into Twitter-ready post.
    Returns (formatted_message, ai_used) tuple.
    Falls back to local formatting if AI is unavailable.
    """
    if not CEREBRAS_API_KEY:
        return format_message_locally(description), False
    
    try:
        headers = {
            "Authorization": f"Bearer {CEREBRAS_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3.1-8b",
            "messages": [
                {
                    "role": "system",
                    "content": """You are an AI assistant helping rural communities communicate health issues clearly and professionally to a global audience.

Your task is to rewrite health messages into clear, simple, and impactful public awareness posts suitable for Twitter.

Instructions:
- Fix grammar, spelling, and improve clarity
- Keep the core meaning intact
- Use professional yet accessible language
- Make it concise (under 280 characters total including hashtags)
- Remove any personal names or sensitive information
- Add 2-4 relevant health hashtags at the end based on the topic
- Make it action-oriented and informative
- Focus on public health awareness

Output only the final tweet text with hashtags. Do not include explanations or quotes."""
                },
                {
                    "role": "user",
                    "content": f"Rewrite this health message:\n\n{description}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        response = requests.post(
            "https://api.cerebras.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            formatted_message = data['choices'][0]['message']['content'].strip()
            # Remove quotes if AI wrapped the response
            formatted_message = formatted_message.strip('"').strip("'")
            return formatted_message, True
        else:
            print(f"Cerebras API error: {response.status_code} - {response.text}")
            return format_message_locally(description), False
    
    except Exception as e:
        print(f"Error calling Cerebras API: {e}")
        return format_message_locally(description), False


@app.route('/report-issue')
@auth.login_required
def report_issue():
    """Health Issue Reporting page (protected)"""
    user_id = session.get('user_id')
    user = db.get_user_by_id(user_id)
    return render_template('report_issue.html', user=user)


@app.route('/api/generate-post', methods=['POST'])
@auth.login_required
def generate_post():
    """Generate AI-formatted post from health issue description"""
    try:
        user_id = session.get('user_id')
        
        # Get description
        description = request.form.get('description', '').strip()
        if not description:
            return jsonify({"success": False, "message": "Description is required"}), 400
        
        # Generate formatted message (AI or local fallback)
        ai_message, ai_used = format_message_with_ai(description)
        
        # Save report to database
        report_id = db.add_health_report(
            user_id=user_id,
            description=description,
            image_path=None,
            ai_formatted_message=ai_message
        )
        
        if report_id:
            return jsonify({
                "success": True,
                "report_id": report_id,
                "formatted_message": ai_message,
                "ai_used": ai_used
            })
        else:
            return jsonify({"success": False, "message": "Failed to save report"}), 500
    
    except Exception as e:
        print(f"Error generating post: {e}")
        # Ultimate fallback - still return success with basic formatting
        try:
            fallback_msg = format_message_locally(description)
            report_id = db.add_health_report(
                user_id=session.get('user_id'),
                description=description,
                image_path=None,
                ai_formatted_message=fallback_msg
            )
            return jsonify({
                "success": True,
                "report_id": report_id,
                "formatted_message": fallback_msg,
                "ai_used": False
            })
        except Exception:
            return jsonify({"success": False, "message": "Failed to generate post. Please try again."}), 500


@app.route('/api/post-to-twitter', methods=['POST'])
@auth.login_required
def post_twitter():
    """Mark report as shared via Twitter Intent URL"""
    try:
        user_id = session.get('user_id')
        data = request.json
        
        report_id = data.get('report_id')
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"success": False, "message": "Message is required"}), 400
        
        if not report_id:
            return jsonify({"success": False, "message": "Report ID is required"}), 400
        
        # Verify report belongs to user
        report = db.get_health_report_by_id(report_id)
        if not report or report['user_id'] != user_id:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        
        # Mark as posted in database
        db.update_health_report_twitter_post(report_id, 'intent_shared')
        
        return jsonify({
            "success": True,
            "message": "Report marked as shared"
        })
    
    except Exception as e:
        print(f"Error marking report: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/health-reports', methods=['GET'])
@auth.login_required
def get_health_reports():
    """Get user's health reports"""
    user_id = session.get('user_id')
    limit = request.args.get('limit', type=int)
    
    reports = db.get_user_health_reports(user_id, limit)
    
    return jsonify({
        "success": True,
        "reports": reports
    })


@app.route('/api/health-tracker/add', methods=['POST'])
@auth.login_required
def add_health_entry():
    """Add a new health tracker entry"""
    user_id = session.get('user_id')
    data = request.json
    
    # Extract data with validation
    try:
        weight = float(data.get('weight')) if data.get('weight') else None
        blood_pressure = data.get('blood_pressure', '').strip() or None
        heart_rate = int(data.get('heart_rate')) if data.get('heart_rate') else None
        calories = int(data.get('calories')) if data.get('calories') else None
        water_intake = float(data.get('water_intake')) if data.get('water_intake') else None
        sleep_hours = float(data.get('sleep_hours')) if data.get('sleep_hours') else None
        notes = data.get('notes', '').strip() or None
        date_created = data.get('date_created') or None
        
        # Add entry to database
        entry_id = db.add_health_entry(
            user_id=user_id,
            weight=weight,
            blood_pressure=blood_pressure,
            heart_rate=heart_rate,
            calories=calories,
            water_intake=water_intake,
            sleep_hours=sleep_hours,
            notes=notes,
            date_created=date_created
        )
        
        if entry_id:
            return jsonify({
                "success": True,
                "message": "Health entry added successfully",
                "entry_id": entry_id
            })
        else:
            return jsonify({"success": False, "message": "Failed to add entry"}), 500
            
    except (ValueError, TypeError) as e:
        return jsonify({"success": False, "message": f"Invalid data format: {str(e)}"}), 400


@app.route('/api/health-tracker/entries', methods=['GET'])
@auth.login_required
def get_health_entries():
    """Get all health entries for the current user"""
    user_id = session.get('user_id')
    limit = request.args.get('limit', type=int)
    
    entries = db.get_user_health_entries(user_id, limit)
    
    return jsonify({
        "success": True,
        "entries": entries
    })


@app.route('/api/health-tracker/summary', methods=['GET'])
@auth.login_required
def get_health_summary():
    """Get health summary statistics"""
    user_id = session.get('user_id')
    summary = db.get_health_summary(user_id)
    
    return jsonify({
        "success": True,
        "summary": summary
    })


@app.route('/api/health-tracker/chart-data', methods=['GET'])
@auth.login_required
def get_health_chart_data():
    """Get health data for charts"""
    user_id = session.get('user_id')
    days = request.args.get('days', default=30, type=int)
    
    chart_data = db.get_health_chart_data(user_id, days)
    
    return jsonify({
        "success": True,
        "data": chart_data
    })


@app.route('/api/health-tracker/delete/<int:entry_id>', methods=['DELETE'])
@auth.login_required
def delete_health_entry(entry_id):
    """Delete a health entry"""
    user_id = session.get('user_id')
    
    success = db.delete_health_entry(entry_id, user_id)
    
    if success:
        return jsonify({"success": True, "message": "Entry deleted successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to delete entry"}), 500


# ============================================
# CHATBOT API
# ============================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    Saves to database if user is logged in
    Supports session-based chat storage
    """
    user_msg = request.json.get('message', '')
    session_id = request.json.get('session_id')
    
    if not user_msg:
        return jsonify({"error": "Message required"}), 400
    
    # Get bot response
    reply = get_response(user_msg)
    
    # Save to database if user is logged in
    if auth.is_authenticated():
        user = auth.get_current_user()
        
        # If session_id is provided, save to that session
        if session_id:
            db.save_chat_message(session_id, 'user', user_msg)
            db.save_chat_message(session_id, 'bot', reply)
        
        # Also save to legacy chat_history table
        db.save_chat(user['id'], user_msg, reply)
    
    return jsonify({
        "reply": reply,
        "timestamp": datetime.now().isoformat()
    })


# ============================================
# CHAT SESSION API
# ============================================

@app.route('/api/chat-sessions', methods=['GET', 'POST'])
@auth.login_required
def chat_sessions():
    """
    GET: List all chat sessions for the user
    POST: Create a new chat session
    """
    user_id = session.get('user_id')
    
    if request.method == 'GET':
        sessions = db.get_user_chat_sessions(user_id)
        return jsonify({"success": True, "sessions": sessions})
    
    elif request.method == 'POST':
        data = request.json or {}
        title = data.get('title', 'New Chat')
        
        session_id = db.create_chat_session(user_id, title)
        
        if session_id:
            return jsonify({"success": True, "session_id": session_id, "title": title})
        else:
            return jsonify({"success": False, "message": "Failed to create session"}), 500


@app.route('/api/chat-sessions/<int:session_id>', methods=['GET', 'DELETE'])
@auth.login_required
def chat_session_detail(session_id):
    """
    GET: Get a specific session with all messages
    DELETE: Delete a session
    """
    user_id = session.get('user_id')
    
    # Verify session belongs to user
    chat_session = db.get_chat_session(session_id)
    if not chat_session or chat_session['user_id'] != user_id:
        return jsonify({"success": False, "message": "Session not found"}), 404
    
    if request.method == 'GET':
        messages = db.get_session_messages(session_id)
        return jsonify({
            "success": True,
            "session": chat_session,
            "messages": messages
        })
    
    elif request.method == 'DELETE':
        success = db.delete_chat_session(session_id, user_id)
        if success:
            return jsonify({"success": True, "message": "Session deleted"})
        else:
            return jsonify({"success": False, "message": "Failed to delete session"}), 500


@app.route('/api/chat-sessions/<int:session_id>/title', methods=['PUT'])
@auth.login_required
def update_session_title(session_id):
    """
    Update the title of a chat session
    """
    user_id = session.get('user_id')
    
    # Verify session belongs to user
    chat_session = db.get_chat_session(session_id)
    if not chat_session or chat_session['user_id'] != user_id:
        return jsonify({"success": False, "message": "Session not found"}), 404
    
    data = request.json or {}
    new_title = data.get('title', '').strip()
    
    if not new_title:
        return jsonify({"success": False, "message": "Title required"}), 400
    
    success = db.update_chat_session_title(session_id, new_title)
    
    if success:
        return jsonify({"success": True, "message": "Title updated"})
    else:
        return jsonify({"success": False, "message": "Failed to update title"}), 500


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

