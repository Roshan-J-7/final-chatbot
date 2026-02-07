"""
Advanced Symptom Checker Module
Provides multi-step symptom assessment with severity analysis
"""

class SymptomChecker:
    def __init__(self):
        self.symptoms_database = {
            "fever": {
                "severity_levels": {
                    "mild": {"temp": (99, 101), "duration": "< 3 days"},
                    "moderate": {"temp": (101, 103), "duration": "3-5 days"},
                    "severe": {"temp": (103, 105), "duration": "> 5 days"}
                },
                "related_conditions": ["flu", "infection", "covid-19", "malaria"],
                "questions": [
                    "What is your current temperature?",
                    "How long have you had the fever?",
                    "Do you have any other symptoms (cough, headache, body aches)?",
                    "Have you recently traveled?"
                ]
            },
            "chest_pain": {
                "severity": "emergency",
                "immediate_action": "Call emergency services immediately",
                "questions": [
                    "Is the pain radiating to your arm or jaw?",
                    "Do you have shortness of breath?",
                    "Are you experiencing sweating or nausea?"
                ],
                "warning": "SEEK IMMEDIATE MEDICAL ATTENTION"
            },
            "headache": {
                "types": ["tension", "migraine", "cluster", "sinus"],
                "severity_indicators": {
                    "mild": "Manageable with OTC medication",
                    "moderate": "Interferes with daily activities",
                    "severe": "Sudden, severe ('thunderclap'), worst headache ever"
                },
                "questions": [
                    "Where is the pain located?",
                    "Is the pain throbbing or constant?",
                    "Are you sensitive to light or sound?",
                    "Do you have nausea or vision changes?"
                ]
            },
            "abdominal_pain": {
                "locations": {
                    "upper_right": ["gallbladder", "liver"],
                    "upper_left": ["stomach", "spleen"],
                    "lower_right": ["appendix", "ovary"],
                    "lower_left": ["colon", "ovary"],
                    "center": ["stomach", "intestines"]
                },
                "questions": [
                    "Where exactly is the pain located?",
                    "Is it sharp or dull?",
                    "Does it worsen with movement or eating?",
                    "Do you have nausea, vomiting, or changes in bowel movements?"
                ]
            },
            "cough": {
                "types": ["dry", "productive", "whooping"],
                "duration_analysis": {
                    "acute": "< 3 weeks",
                    "subacute": "3-8 weeks",
                    "chronic": "> 8 weeks"
                },
                "questions": [
                    "Is the cough dry or producing mucus?",
                    "What color is the mucus (if any)?",
                    "How long have you been coughing?",
                    "Do you have difficulty breathing?"
                ]
            },
            "shortness_of_breath": {
                "severity": "urgent",
                "immediate_action": "Seek immediate medical attention",
                "questions": [
                    "When did it start?",
                    "Does it occur at rest or with exertion?",
                    "Do you have chest pain?",
                    "Do you have a history of heart or lung disease?"
                ]
            }
        }
        
        self.assessment_results = {}
    
    def start_assessment(self, primary_symptom):
        """Initialize symptom assessment"""
        primary_symptom = primary_symptom.lower()
        
        # Find matching symptom
        for symptom, data in self.symptoms_database.items():
            if symptom in primary_symptom or primary_symptom in symptom:
                return {
                    "symptom": symptom,
                    "questions": data.get("questions", []),
                    "severity": data.get("severity", "assessment_required"),
                    "immediate_action": data.get("immediate_action"),
                    "warning": data.get("warning")
                }
        
        return {
            "symptom": "unknown",
            "message": "Please describe your main symptom",
            "suggestions": list(self.symptoms_database.keys())
        }
    
    def analyze_responses(self, symptom, responses):
        """Analyze user responses to determine severity and recommendations"""
        
        # Emergency symptoms
        emergency_symptoms = ["chest_pain", "shortness_of_breath"]
        if symptom in emergency_symptoms:
            return {
                "severity": "EMERGENCY",
                "recommendation": "CALL EMERGENCY SERVICES (108) IMMEDIATELY",
                "actions": [
                    "Do not drive yourself",
                    "Stay calm",
                    "Sit in comfortable position",
                    "If prescribed, take emergency medication"
                ]
            }
        
        # Analyze based on symptom type
        if symptom == "fever":
            try:
                temp = float(responses.get("temperature", 99))
                duration = responses.get("duration", "").lower()
                
                if temp >= 103:
                    severity = "HIGH"
                    recommendation = "Consult doctor today"
                elif temp >= 101:
                    severity = "MODERATE"
                    recommendation = "Monitor closely, see doctor if persists 3+ days"
                else:
                    severity = "MILD"
                    recommendation = "Home care with rest and fluids"
                
                return {
                    "severity": severity,
                    "recommendation": recommendation,
                    "home_care": [
                        "Rest adequately",
                        "Drink plenty of fluids",
                        "Take paracetamol as directed",
                        "Monitor temperature every 4 hours",
                        "Watch for worsening symptoms"
                    ]
                }
            except:
                pass
        
        # Default assessment
        return {
            "severity": "ASSESSMENT REQUIRED",
            "recommendation": "Consult healthcare provider for proper evaluation",
            "general_advice": [
                "Keep track of symptoms",
                "Note any changes or new symptoms",
                "Avoid self-medication without guidance",
                "Seek medical care if symptoms worsen"
            ]
        }
    
    def get_red_flags(self, symptom):
        """Get red flag symptoms that require immediate medical attention"""
        red_flags = {
            "fever": [
                "Temperature above 103°F (39.4°C)",
                "Fever lasting more than 5 days",
                "Severe headache with stiff neck",
                "Difficulty breathing",
                "Confusion or altered mental state",
                "Seizures",
                "Persistent vomiting"
            ],
            "headache": [
                "Sudden severe headache ('worst ever')",
                "Headache with fever and stiff neck",
                "Headache after head injury",
                "Headache with vision changes",
                "Headache with weakness or numbness",
                "New headache pattern after age 50"
            ],
            "abdominal_pain": [
                "Severe, sudden pain",
                "Pain with fever",
                "Vomiting blood",
                "Black or bloody stools",
                "Hard, swollen abdomen",
                "Pregnant with abdominal pain"
            ],
            "cough": [
                "Coughing up blood",
                "Difficulty breathing",
                "High fever with cough",
                "Cough lasting more than 3 weeks",
                "Chest pain with cough",
                "Wheezing or stridor"
            ]
        }
        
        return red_flags.get(symptom, [
            "Severe or worsening symptoms",
            "Symptoms lasting longer than expected",
            "New concerning symptoms",
            "Difficulty performing daily activities"
        ])
    
    def get_self_care_tips(self, symptom):
        """Get self-care recommendations for common symptoms"""
        self_care = {
            "fever": [
                "Rest in comfortable environment",
                "Drink 8-10 glasses of fluids daily",
                "Take paracetamol as directed (500-1000mg every 4-6 hours)",
                "Use cool compresses on forehead",
                "Wear light clothing",
                "Monitor temperature regularly"
            ],
            "headache": [
                "Rest in quiet, dark room",
                "Apply cold or warm compress",
                "Stay well hydrated",
                "Practice relaxation techniques",
                "Avoid trigger foods",
                "Maintain regular sleep schedule"
            ],
            "abdominal_pain": [
                "Rest and avoid strenuous activity",
                "Eat bland, easily digestible foods",
                "Stay hydrated with clear fluids",
                "Avoid spicy, fatty, or acidic foods",
                "Use heating pad on low setting",
                "Monitor symptoms closely"
            ],
            "cough": [
                "Drink warm liquids (honey and lemon tea)",
                "Use humidifier in room",
                "Avoid irritants (smoke, dust)",
                "Stay hydrated",
                "Rest adequately",
                "Elevate head while sleeping"
            ]
        }
        
        return self_care.get(symptom, [
            "Rest adequately",
            "Stay hydrated",
            "Avoid known triggers",
            "Monitor symptoms",
            "Seek medical care if needed"
        ])

# Global instance
_checker_instance = None

def get_symptom_checker():
    """Get or create symptom checker instance"""
    global _checker_instance
    if _checker_instance is None:
        _checker_instance = SymptomChecker()
    return _checker_instance
