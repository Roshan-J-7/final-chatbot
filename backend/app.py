from flask import Flask, request, jsonify, render_template, session
import json
import os
from datetime import datetime, timedelta
import random
from chatbot.rule_engine import get_response
from modules.symptom_checker import get_symptom_checker
from utils.logger import log_message

app = Flask(__name__)
app.secret_key = 'medical_kiosk_secret_key_2026'  # Change in production

def load_json(file_path):
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(full_path, 'r') as f:
        return json.load(f)

# Analytics data (in production, this would come from a database)
def get_analytics_data():
    return {
        "today_visitors": random.randint(100, 150),
        "total_consultations": random.randint(500, 800),
        "active_sessions": random.randint(3, 12),
        "common_symptoms": ["Fever", "Cough", "Headache", "Stomach Pain"],
        "weekly_admissions": [42, 38, 45, 50, 48, 35, 40],
        "symptom_distribution": {
            "Respiratory": 35,
            "Digestive": 20,
            "Pain": 25,
            "Fever": 15,
            "Other": 5
        },
        "severity_breakdown": {
            "Mild": 60,
            "Moderate": 30,
            "Severe": 8,
            "Emergency": 2
        },
        "hourly_traffic": [5, 8, 12, 18, 25, 30, 35, 32, 28, 22, 18, 15],
        "patient_satisfaction": 4.6,
        "average_wait_time": "8 minutes"
    }

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    user_id = session.get('user_id', 'default')
    
    reply = get_response(user_msg, user_id)
    log_message(user_msg, reply)
    
    return jsonify({
        "reply": reply,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/analytics')
def analytics():
    """Get dashboard analytics data"""
    return jsonify(get_analytics_data())

@app.route('/api/symptom_check/start', methods=['POST'])
def start_symptom_check():
    """Start symptom checker assessment"""
    symptom = request.json.get('symptom', '')
    checker = get_symptom_checker()
    
    assessment = checker.start_assessment(symptom)
    return jsonify(assessment)

@app.route('/api/symptom_check/analyze', methods=['POST'])
def analyze_symptoms():
    """Analyze symptom responses"""
    data = request.json
    symptom = data.get('symptom', '')
    responses = data.get('responses', {})
    
    checker = get_symptom_checker()
    analysis = checker.analyze_responses(symptom, responses)
    red_flags = checker.get_red_flags(symptom)
    self_care = checker.get_self_care_tips(symptom)
    
    return jsonify({
        "analysis": analysis,
        "red_flags": red_flags,
        "self_care_tips": self_care
    })

@app.route('/api/first_aid')
def first_aid():
    return jsonify(load_json('modules/first_aid.json'))

@app.route('/api/health_tips')
def health_tips():
    return jsonify(load_json('modules/health_tips.json'))

@app.route('/api/emergency_contacts')
def emergency_contacts():
    return jsonify(load_json('modules/emergency_contacts.json'))

@app.route('/api/appointments', methods=['GET', 'POST'])
def appointments():
    """Handle appointment requests"""
    if request.method == 'POST':
        data = request.json
        # In production, save to database
        appointment = {
            "id": random.randint(1000, 9999),
            "name": data.get('name'),
            "phone": data.get('phone'),
            "date": data.get('date'),
            "time": data.get('time'),
            "reason": data.get('reason'),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        return jsonify({
            "success": True,
            "appointment": appointment,
            "message": "Appointment request submitted successfully"
        })
    else:
        # Return sample appointments
        return jsonify({
            "upcoming": [
                {"time": "09:00 AM", "patient": "John Doe", "reason": "Check-up"},
                {"time": "10:30 AM", "patient": "Jane Smith", "reason": "Consultation"},
                {"time": "02:00 PM", "patient": "Bob Johnson", "reason": "Follow-up"}
            ]
        })

@app.route('/api/health_records', methods=['GET'])
def health_records():
    """Get sample health records"""
    return jsonify({
        "records": [
            {
                "date": "2026-01-28",
                "type": "Consultation",
                "doctor": "Dr. Smith",
                "diagnosis": "Common Cold",
                "prescription": "Rest, fluids, paracetamol"
            },
            {
                "date": "2026-01-15",
                "type": "Check-up",
                "doctor": "Dr. Johnson",
                "diagnosis": "Routine examination",
                "prescription": "None"
            }
        ]
    })

@app.route('/api/search', methods=['POST'])
def search():
    """Search medical information"""
    query = request.json.get('query', '').lower()
    
    # Simple search through knowledge base
    from chatbot.rule_engine import get_chatbot
    chatbot = get_chatbot()
    
    results = []
    for rule in chatbot.knowledge_base['rules']:
        if any(kw in query for kw in rule['keywords']):
            results.append({
                "category": rule.get('category', 'general'),
                "keywords": rule['keywords'][:3],  # First 3 keywords
                "severity": rule.get('severity', 'information')
            })
    
    return jsonify({
        "query": query,
        "results": results[:10],  # Top 10 results
        "count": len(results)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)