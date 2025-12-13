"""
Lightweight Vercel Serverless Function for Chatbot
Simple chatbot responses - Works entirely on Vercel
"""
import json
import os
from http.server import BaseHTTPRequestHandler

# Simple response templates (can be enhanced with AI API)
RESPONSES = {
    'greeting': [
        "Hello! How can I help you today?",
        "Hi there! What can I assist you with?",
        "Greetings! I'm here to help."
    ],
    'health': [
        "I can help with general health information. For medical advice, please consult a healthcare professional.",
        "I'm here to provide general health information. Remember to consult a doctor for medical concerns.",
        "I can assist with health-related questions, but always consult a professional for medical advice."
    ],
    'default': [
        "I understand. Can you tell me more?",
        "That's interesting. How can I help further?",
        "I'm here to assist. What would you like to know?"
    ]
}

def get_simple_response(user_input):
    """Generate a simple response based on user input"""
    user_lower = user_input.lower()
    
    # Check for greetings
    if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return RESPONSES['greeting'][0]
    
    # Check for health-related queries
    if any(word in user_lower for word in ['health', 'symptom', 'disease', 'medical', 'doctor', 'treatment', 'pain', 'fever', 'cough']):
        return RESPONSES['health'][0]
    
    # Check for questions
    if '?' in user_input:
        return "That's a good question! I can provide general information. For specific medical advice, please consult a healthcare professional."
    
    # Default response
    return RESPONSES['default'][0]

# Vercel serverless function handler
class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Parse JSON body
            try:
                body = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                body = {}
            
            user_input = body.get('input', '').strip()
            chat_id = body.get('chat_id', 1)
            
            if not user_input:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No input provided'}).encode('utf-8'))
                return
            
            # Generate response
            response = get_simple_response(user_input)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'response': response,
                'message': 'Simple chatbot is active. For advanced AI features, consider integrating with OpenAI or Google Gemini API.'
            }).encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = str(e)
            print(f"ERROR in chatbot handler: {error_details}")
            print(f"Traceback: {traceback.format_exc()}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'Server error: {error_details}'
            }).encode('utf-8'))
