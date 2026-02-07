import json
import os
import re
import random
from datetime import datetime

class MedicalChatbot:
    def __init__(self):
        kb_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.knowledge_base = json.load(f)
        self.conversation_context = {}
        self.conversation_history = {}
        self.stopwords = {
            'the', 'is', 'are', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'about',
            'please', 'tell', 'me', 'what', 'why', 'how', 'does', 'do', 'can', 'could', 'should', 'would',
            'explain', 'describe', 'give', 'learn', 'know', 'information', 'detail', 'details', 'my', 'your'
        }
        self.synonyms = {
            'tummy': 'stomach',
            'belly': 'stomach',
            'pee': 'urine',
            'peeing': 'urine',
            'urination': 'urine',
            'poop': 'bowel',
            'pooping': 'bowel',
            'heartburn': 'reflux',
            'flu': 'influenza',
            'sugar': 'glucose',
            'bp': 'pressure',
            'bloodpressure': 'pressure',
            'covid': 'covid',
            'covid19': 'covid'
        }
        
    def preprocess_input(self, user_input):
        """Clean and normalize user input"""
        user_input = user_input.lower().strip()
        # Remove extra spaces
        user_input = re.sub(r'\s+', ' ', user_input)
        # Remove punctuation but keep question marks for intent detection
        user_input = re.sub(r'[^\w\s?]', '', user_input)
        return user_input

    def normalize_token(self, token):
        token = re.sub(r'[^a-z0-9]', '', token.lower())
        for suffix in ['ing', 'ed', 'es', 's']:
            if token.endswith(suffix) and len(token) > 3:
                token = token[:-len(suffix)]
                break
        return token

    def tokenize(self, text):
        tokens = []
        for raw in text.split():
            token = self.normalize_token(raw)
            if not token or token in self.stopwords:
                continue
            token = self.synonyms.get(token, token)
            tokens.append(token)
        return tokens

    def strip_explain_phrases(self, text):
        phrases = self.knowledge_base.get('intents', {}).get('explain', [])
        cleaned = text
        for phrase in phrases:
            cleaned = cleaned.replace(phrase, '').strip()
        return cleaned
    
    def detect_intent(self, user_input):
        """Detect user intent from input using intent patterns"""
        intents = self.knowledge_base.get('intents', {})
        
        for intent_name, patterns in intents.items():
            for pattern in patterns:
                if pattern in user_input:
                    return intent_name
        return None
    
    def check_emergency(self, user_input):
        """Check if input contains emergency keywords"""
        emergency_keywords = self.knowledge_base.get('emergency_keywords', [])
        for keyword in emergency_keywords:
            if keyword in user_input:
                return True
        return False
    
    def get_template_response(self, intent):
        """Get a varied response template based on intent"""
        templates = self.knowledge_base.get('response_templates', {})
        if intent in templates:
            responses = templates[intent]
            return random.choice(responses)
        return None
    
    def get_conversational_prefix(self):
        """Get a natural conversational prefix"""
        prefixes = self.knowledge_base.get('conversational_responses', {}).get('understanding', [])
        if prefixes and random.random() > 0.5:  # 50% chance to add prefix
            return random.choice(prefixes) + " "
        return ""

    def get_help_response(self):
        topics = [rule.get('category', '').replace('_', ' ') for rule in self.knowledge_base.get('rules', [])]
        topics = [t for t in topics if t]
        sample = ', '.join(sorted(set(topics))[:10])
        return (
            "I can help with anatomy, diseases, symptoms, nutrition, medications, prevention, and biology basics. "
            f"Some topics include: {sample}. Ask in your own words, like 'Why do I feel dizzy?' or 'Explain the immune system.'"
        )
    
    def add_natural_followup(self, rule):
        """Add natural follow-up suggestions"""
        followup = rule.get('followup', [])
        if followup:
            conversational = self.knowledge_base.get('conversational_responses', {})
            followup_phrases = conversational.get('followup', [])
            if followup_phrases:
                phrase = random.choice(followup_phrases)
                suggestions = ', '.join(followup[:3])  # Limit to 3 suggestions
                return f"\n\n{phrase} {suggestions}?"
        return ""
    
    def extract_entities(self, user_input):
        """Extract key entities/topics from user input"""
        entities = []
        # Look for medical terms, body parts, symptoms
        medical_terms = set()
        for rule in self.knowledge_base.get('rules', []):
            medical_terms.update(rule.get('keywords', []))
        
        for term in medical_terms:
            if term in user_input:
                entities.append(term)
        
        return entities
    
    def find_best_match(self, user_input, user_id='default'):
        """Find the best matching rule using intent and keyword matching"""
        processed_input = self.preprocess_input(user_input)
        
        # First, check for intent-based responses (greetings, thanks, etc.)
        intent = self.detect_intent(processed_input)
        if intent in ['greeting', 'farewell', 'thanks', 'how_are_you']:
            template_response = self.get_template_response(intent)
            if template_response:
                return {
                    'response': template_response,
                    'intent': intent,
                    'type': 'template',
                    'severity': 'greeting'
                }

        if intent in ['help', 'what_can_you_do']:
            # Only return help if no other meaningful keywords found
            entities = self.extract_entities(processed_input)
            if not entities:
                return {
                    'response': self.get_help_response(),
                    'intent': intent,
                    'type': 'template',
                    'severity': 'information'
                }

        if intent == 'explain':
            processed_input = self.strip_explain_phrases(processed_input)
        
        # Check for emergency first
        if self.check_emergency(processed_input):
            for rule in self.knowledge_base.get('rules', []):
                if rule.get('severity') == 'emergency' and any(kw in processed_input for kw in rule.get('keywords', [])):
                    return {
                        'response': rule['response'],
                        'rule': rule,
                        'type': 'emergency'
                    }
        
        # Extract entities for better matching
        entities = self.extract_entities(processed_input)
        
        # Score each rule based on keyword matches
        rule_scores = []
        for rule in self.knowledge_base.get('rules', []):
            score = 0
            matched_keywords = []
            
            for keyword in rule.get('keywords', []):
                if keyword in processed_input:
                    # Higher score for longer keyword matches
                    score += len(keyword.split()) + 1
                    matched_keywords.append(keyword)
                    
                    # Bonus for exact phrase match
                    if keyword == processed_input:
                        score += 5
                    
                    # Bonus for keyword at start of input
                    if processed_input.startswith(keyword):
                        score += 2
            
            # Context-based scoring - boost if related to previous topic
            if user_id in self.conversation_context:
                last_category = self.conversation_context[user_id].get('last_category', '')
                if last_category and rule.get('category', '').startswith(last_category.split('_')[0]):
                    score += 1
            
            if score > 0:
                rule_scores.append({
                    'rule': rule,
                    'score': score,
                    'matched_keywords': matched_keywords
                })

        # If no direct keyword match, use token overlap for broader coverage
        if not rule_scores:
            input_tokens = set(self.tokenize(processed_input))
            for rule in self.knowledge_base.get('rules', []):
                keyword_tokens = set()
                for keyword in rule.get('keywords', []):
                    keyword_tokens.update(self.tokenize(keyword))
                category_tokens = set(self.tokenize(rule.get('category', '').replace('_', ' ')))
                overlap = input_tokens & (keyword_tokens | category_tokens)
                if overlap:
                    rule_scores.append({
                        'rule': rule,
                        'score': len(overlap),
                        'matched_keywords': list(overlap)
                    })
        
        # Sort by score and return best match
        if rule_scores:
            rule_scores.sort(key=lambda x: x['score'], reverse=True)
            return {
                'response': rule_scores[0]['rule']['response'],
                'rule': rule_scores[0]['rule'],
                'type': 'knowledge',
                'matched_keywords': rule_scores[0]['matched_keywords']
            }
        
        return None
    
    def generate_natural_response(self, match_result, user_id='default'):
        """Generate a natural, conversational response"""
        if not match_result:
            return None
        
        response_type = match_result.get('type')
        response = match_result.get('response', '')
        
        # For template responses (greetings, etc.), return as is
        if response_type == 'template':
            return response
        
        # For knowledge-based responses, add natural language elements
        if response_type in ['knowledge', 'emergency']:
            rule = match_result.get('rule', {})
            
            # Add conversational prefix occasionally
            if response_type != 'emergency' and random.random() > 0.6:
                prefix = self.get_conversational_prefix()
                response = prefix + response
            
            # Add natural variations if available
            natural_variations = rule.get('natural_variations', [])
            if natural_variations and random.random() > 0.7:
                intro = random.choice(natural_variations)
                response = intro + " " + response
            
            # Add follow-up suggestions naturally
            followup = self.add_natural_followup(rule)
            response += followup
            
            return response
        
        return response
    
    def get_response(self, user_input, user_id='default'):
        """Generate response based on user input with NLP-like conversation"""
        # Initialize conversation history for this user
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Store user input
        self.conversation_history[user_id].append({
            'type': 'user',
            'message': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Find best match
        match_result = self.find_best_match(user_input, user_id)
        
        if match_result:
            # Generate natural response
            response = self.generate_natural_response(match_result, user_id)
            
            # Add disclaimer for medical advice (but not for greetings/info)
            rule = match_result.get('rule', {})
            severity = rule.get('severity') or match_result.get('severity', 'information')
            
            if severity not in ['greeting', 'information', 'prevention']:
                response += "\n\n" + self.knowledge_base.get('disclaimer', '')
            
            # Store context for follow-up
            self.conversation_context[user_id] = {
                'last_category': rule.get('category', ''),
                'last_severity': severity,
                'followup_topics': rule.get('followup', []),
                'timestamp': datetime.now().isoformat(),
                'last_intent': match_result.get('intent', '')
            }
            
            # Store bot response
            self.conversation_history[user_id].append({
                'type': 'bot',
                'message': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
        else:
            # More helpful fallback response
            conversational = self.knowledge_base.get('conversational_responses', {})
            uncertainty = conversational.get('uncertainty', [])
            
            if uncertainty:
                fallback = random.choice(uncertainty)
                fallback += " I can answer questions on symptoms, anatomy, conditions, nutrition, medications, prevention, and wellness. Try a full sentence like: 'What causes chest pain?' or 'Explain the immune system.'"
            else:
                fallback = ("I don't have specific information about that yet. For accurate medical advice, please consult a qualified healthcare professional. "
                           "I can help with symptoms, anatomy systems, diseases, nutrition, hormones, medications, and prevention. "
                           "Try asking in natural language, like 'Why do I feel dizzy?' or 'How does digestion work?'")
            
            self.conversation_history[user_id].append({
                'type': 'bot',
                'message': fallback,
                'timestamp': datetime.now().isoformat()
            })
            
            return fallback

# Global instance
_chatbot_instance = None

def get_chatbot():
    """Get or create chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = MedicalChatbot()
    return _chatbot_instance

def get_response(user_input, user_id='default'):
    """Wrapper function for backward compatibility"""
    chatbot = get_chatbot()
    return chatbot.get_response(user_input, user_id)