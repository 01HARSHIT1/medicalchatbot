"""
Lightweight Vercel Serverless Function for Chatbot
Simple chatbot responses - Can be enhanced with OpenAI API
"""
import json
import os

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
    if any(word in user_lower for word in ['health', 'symptom', 'disease', 'medical', 'doctor', 'treatment']):
        return RESPONSES['health'][0]
    
    # Default response
    return RESPONSES['default'][0]

# Vercel serverless function handler
def handler(request):
    """Vercel serverless function handler"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        body = {}
        if hasattr(request, 'json') and request.json:
            body = request.json
        elif hasattr(request, 'body'):
            if isinstance(request.body, str):
                body = json.loads(request.body)
            elif isinstance(request.body, dict):
                body = request.body
        
        user_input = body.get('input', '').strip()
        chat_id = body.get('chat_id', 1)
        
        if not user_input:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No input provided'})
            }
        
        # Generate response
        response = get_simple_response(user_input)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'response': response,
                'message': 'Simple chatbot is active. For advanced AI features, consider integrating with OpenAI or Google Gemini API.'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }

