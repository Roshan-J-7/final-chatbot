# Medical Kiosk - Advanced Healthcare System

A comprehensive, professional medical kiosk application built with Flask, featuring an advanced rule-based chatbot, symptom checker, real-time analytics dashboard, and extensive medical information system.

## Features

### 1. Advanced Rule-Based Medical Chatbot
-  50+ Medical Conditions Covered : Comprehensive knowledge base covering respiratory, digestive, pain, skin, injury, allergy, mental health, chronic conditions, and more
-  Intelligent Pattern Matching : Sophisticated keyword matching with scoring algorithm
-  Context Awareness : Maintains conversation context and follow-up topics
-  Emergency Detection : Automatically identifies emergency situations and provides urgent guidance
-  Severity Assessment : Categorizes conditions by severity (mild, moderate, severe, emergency)

### 2. Symptom Checker Module
-  Multi-Step Assessment : Interactive symptom evaluation with targeted questions
-  Red Flag Detection : Identifies warning signs requiring immediate medical attention
-  Self-Care Recommendations : Provides actionable home care instructions
-  Severity Analysis : Evaluates symptom severity and urgency

### 3. Professional Dashboard
-  Real-Time Analytics : 
  - Today's visitors count
  - Total consultations
  - Active sessions
  - Patient satisfaction ratings
-  Interactive Charts :
  - Weekly patient admissions (line chart)
  - Symptom distribution (doughnut chart)
  - Hourly traffic patterns
-  Quick Actions : Direct access to symptom checker, chatbot, and emergency services

### 4. First Aid Guidelines
Comprehensive step-by-step instructions for:
- Burns
- Cuts and wounds
- Nosebleeds
- Choking
- Sprains and strains
- Insect stings
- Heat exhaustion
- Seizures

### 5. Health Tips
20+ evidence-based health recommendations covering:
- Hydration and nutrition
- Exercise and physical activity
- Sleep hygiene
- Preventive care
- Mental health
- Disease prevention

### 6. Emergency Contacts
Quick access to:
- Ambulance / Medical Emergency (108)
- Fire Department (101)
- Police (100)
- Women Helpline (1091)
- Child Helpline (1098)
- Poison Control (1066)
- Mental Health Support
- Local hospital contacts

### 7. Additional Features
-  Appointment System : Book and manage medical appointments
-  Health Records : View medical history and consultation records
-  Search Functionality : Search through medical knowledge base
-  Responsive Design : Works seamlessly on all devices
-  Professional UI : Modern, clean interface without distracting elements

## Technology Stack

### Backend
-  Flask : Python web framework
-  Python 3.x : Core programming language

### Frontend
-  HTML5/CSS3 : Structure and styling
-  JavaScript : Interactive functionality
-  Tailwind CSS : Utility-first CSS framework
-  Chart.js : Data visualization
-  Font Awesome : Icon library

### Design
-  Glass-morphism Effects : Modern translucent UI elements
-  Gradient Backgrounds : Professional purple/blue color scheme
-  Animations : Smooth transitions and hover effects
-  Responsive Grid : Adapts to all screen sizes

## Project Structure

```
Medical Kiosk/
├── backend/
│   ├── app.py                      # Main Flask application
│   ├── chatbot/
│   │   ├── ai_integration.py       # AI integration placeholder
│   │   ├── knowledge_base.json     # Comprehensive medical knowledge base
│   │   └── rule_engine.py          # Advanced chatbot logic
│   ├── modules/
│   │   ├── emergency_contacts.json # Emergency contact information
│   │   ├── first_aid.json          # First aid guidelines
│   │   ├── health_tips.json        # Health and wellness tips
│   │   └── symptom_checker.py      # Symptom assessment module
│   ├── templates/
│   │   ├── index.html              # Main dashboard
│   │   ├── intro.html              # Landing page
│   │   ├── admin.html              # Admin panel
│   │   └── chatbot.html            # Standalone chatbot page
│   ├── static/
│   │   ├── css/                    # Custom stylesheets
│   │   ├── js/                     # JavaScript files
│   │   └── images/                 # Image assets
│   ├── utils/
│   │   ├── helpers.py              # Utility functions
│   │   └── logger.py               # Chat logging system
│   └── database/
│       └── chat_logs.txt           # Chat history
└── deployment/
    ├── install_dependencies.sh     # Dependency installation script
    ├── run_kiosk.sh               # Startup script
    └── systemd_service.conf       # System service configuration
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1.  Navigate to project directory :
   ```bash
   cd "c:\Users\DELL\Desktop\rough\Medical Kiosk"
   ```

2.  Install dependencies :
   ```bash
   pip install flask
   ```

3.  Run the application :
   ```bash
   python backend/app.py
   ```

4.  Access the application :
   - Open browser and navigate to: `http://localhost:5000`
   - For network access: `http://0.0.0.0:5000`

## Usage

### Starting the Application
```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000` (or `http://0.0.0.0:5000`)

### Accessing Features

1.  Landing Page  (`/`): 
   - Overview of features
   - Quick start button
   - System statistics

2.  Dashboard  (`/dashboard`):
   - Real-time analytics
   - Navigation to all features
   - Interactive charts

3.  Chat with Medical Bot :
   - Click floating chat button (bottom-right)
   - Type symptoms or questions
   - Receive instant medical guidance

4.  Check Symptoms :
   - Navigate to Symptom Checker from sidebar
   - Enter primary symptom
   - Answer assessment questions
   - Review recommendations

5.  Access First Aid :
   - Click First Aid in sidebar
   - Browse emergency procedures
   - Follow step-by-step instructions

## API Endpoints

### Chat
- `POST /api/chat`: Send message to chatbot
  - Request: `{"message": "I have a fever"}`
  - Response: `{"reply": "...", "timestamp": "..."}`

### Analytics
- `GET /api/analytics`: Get dashboard statistics

### Symptom Checker
- `POST /api/symptom_check/start`: Start symptom assessment
- `POST /api/symptom_check/analyze`: Analyze symptom responses

### Information
- `GET /api/first_aid`: Get first aid guidelines
- `GET /api/health_tips`: Get health tips
- `GET /api/emergency_contacts`: Get emergency contacts

### Appointments
- `GET /api/appointments`: Get upcoming appointments
- `POST /api/appointments`: Book new appointment

### Health Records
- `GET /api/health_records`: Get health records

## Medical Knowledge Base

The chatbot's knowledge base includes:

### Categories
-  Respiratory : Cough, cold, flu, breathing difficulties
-  Fever : Temperature management, causes, treatment
-  Pain : Headache, chest pain, abdominal pain, back pain
-  Digestive : Nausea, vomiting, diarrhea, constipation
-  Skin : Rashes, burns, insect stings
-  Injury : Cuts, wounds, sprains, fractures
-  Allergy : Allergic reactions, anaphylaxis
-  Mental Health : Anxiety, depression, stress management
-  Chronic : Diabetes, hypertension, asthma
-  Preventive : Diet, exercise, sleep, vaccinations

### Severity Levels
-  Greeting : Welcome messages
-  Information : General medical information
-  Mild : Self-treatable at home
-  Moderate : May require medical consultation
-  Serious : Requires medical attention
-  Emergency : Immediate emergency services needed

## Safety Features

### Medical Disclaimer
Every medical response includes a disclaimer stating:
- Information is for educational purposes only
- Not a substitute for professional medical advice
- Always consult qualified healthcare providers
- In emergencies, call emergency services immediately

### Emergency Detection
The system automatically detects emergency keywords:
- Difficulty breathing
- Chest pain
- Severe bleeding
- Unconsciousness
- Stroke symptoms
- Heart attack symptoms
- Anaphylaxis

When detected, it immediately provides:
- Emergency contact numbers
- Critical first aid instructions
- Clear warning to seek immediate help

## Customization

### Adding New Medical Rules
Edit `backend/chatbot/knowledge_base.json`:
```json
{
  "category": "your_category",
  "keywords": ["keyword1", "keyword2"],
  "response": "Your medical guidance here",
  "severity": "mild|moderate|severe|emergency",
  "followup": ["topic1", "topic2"]
}
```

### Modifying Analytics
Edit the `get_analytics_data()` function in `backend/app.py`

### Styling Changes
- Main CSS: Inline styles in `backend/templates/index.html`
- Color scheme: Modify gradient colors in CSS variables
- Layout: Adjust Tailwind CSS classes

## Future Enhancements

### Planned Features
1.  AI Integration : Replace rule-based system with ML model
2.  Database : PostgreSQL/MySQL for data persistence
3.  User Authentication : Patient accounts and profiles
4.  Multilingual Support : Support for multiple languages
5.  Voice Interface : Voice-based symptom reporting
6.  Medication Tracker : Track prescriptions and reminders
7.  Telemedicine : Video consultation integration
8.  Wearable Integration : Sync with fitness trackers
9.  Prescription Management : Digital prescription handling
10.  Lab Results : View and track test results

### Technical Improvements
- Add unit tests
- Implement caching
- Add rate limiting
- Enhance security
- Deploy to cloud platform
- Mobile app development

## Troubleshooting

### Common Issues

1.  Port Already in Use :
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2.  Module Not Found :
   ```bash
   pip install flask
   ```

3.  JSON File Not Found :
   - Ensure you're running from the backend directory
   - Check file paths in code

## License

This project is intended for educational and demonstration purposes.

## Disclaimer

 IMPORTANT MEDICAL DISCLAIMER : 

This Medical Kiosk system is designed to provide general health information and should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. 

- Always seek the advice of your physician or other qualified healthcare provider with any questions you may have regarding a medical condition
- Never disregard professional medical advice or delay seeking it because of information provided by this system
- If you think you may have a medical emergency, call your doctor or emergency services immediately
- This system does not recommend or endorse any specific tests, physicians, products, procedures, opinions, or other information

The information provided is based on general medical knowledge and may not be applicable to individual cases. Every person's medical situation is unique.

## Contact & Support

For issues, suggestions, or contributions:
- Check documentation in this README
- Review code comments
- Test thoroughly before deployment

## Version History

 Version 2.0.0  (February 2026)
- Complete redesign with professional UI
- Advanced rule-based chatbot with 50+ conditions
- Symptom checker module
- Real-time analytics dashboard
- Comprehensive medical knowledge base
- Enhanced first aid guidelines
- Expanded health tips
- Emergency contact system
- Appointment management
- Health records viewer

 Version 1.0.0  (Initial Release)
- Basic chatbot functionality
- Simple dashboard
- Limited medical information

---

 Built with care for better healthcare accessibility  🏥💙
