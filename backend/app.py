from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime
from chatbot.rule_engine import get_response

app = Flask(__name__)
app.secret_key = 'medical_kiosk_secret_key_2026'

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    reply = get_response(user_msg)
    return jsonify({
        "reply": reply,
        "timestamp": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
