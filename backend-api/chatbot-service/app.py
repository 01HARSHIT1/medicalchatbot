from openai import OpenAI
import os
from flask import Flask, render_template, request, jsonify

# Import configuration
try:
    from config import OPENAI_API_KEY, OPENAI_MODEL, FLASK_PORT, FLASK_DEBUG
except ImportError:
    # Fallback configuration if config.py doesn't exist
    OPENAI_API_KEY = "YOUR_API_KEY_HERE"
    OPENAI_MODEL = "gpt-3.5-turbo"
    FLASK_PORT = 5001
    FLASK_DEBUG = True

# Set your OpenAI API Key - Use environment variable or config file
# Option 1: Set environment variable (recommended)
# export OPENAI_API_KEY="your_api_key_here" (Linux/Mac)
# set OPENAI_API_KEY=your_api_key_here (Windows)

# Option 2: Update the config.py file with your API key
# Option 3: Set it directly here (replace with your valid API key)
FIXED_API_KEY = os.getenv("OPENAI_API_KEY", OPENAI_API_KEY)

# Check if API key is set
if FIXED_API_KEY == "YOUR_API_KEY_HERE":
    print("⚠️  WARNING: Please set your OpenAI API key!")
    print("   Option 1: Set environment variable OPENAI_API_KEY")
    print("   Option 2: Replace 'YOUR_API_KEY_HERE' with your actual API key")
    print("   Get your API key from: https://platform.openai.com/api-keys")
    print("   The chatbot will not work without a valid API key!")

try:
    # Initialize OpenAI client with modern API
    client = OpenAI(api_key=FIXED_API_KEY)
    print("✅ OpenAI API configured successfully!")
    print(f"   Using model: {OPENAI_MODEL}")
except Exception as e:
    print(f"❌ Error configuring OpenAI API: {str(e)}")
    client = None

# Flask app
app = Flask(__name__)

# Enable CORS
try:
    from flask_cors import CORS
    CORS(app)
except ImportError:
    # Fallback CORS headers if flask-cors is not available
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

# Store chats in memory
chats = [{'name': 'New Chat', 'id': 1, 'messages': []}]  # Default chat

# Generate AI response function
def AIResponse(prompt, chat_history=None):
    print(f"🤖 AIResponse called with prompt: '{prompt[:50]}...'")
    
    if not client:
        print("❌ OpenAI client not configured")
        return "❌ Error: OpenAI API not configured. Please check your API key."
    
    # Prepare messages for OpenAI
    messages = []
    
    # Add system message
    messages.append({
        "role": "system", 
        "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
    })
    
    # Add chat history
    if chat_history:
        for msg in chat_history:
            if msg['text'].startswith('User: '):
                messages.append({
                    "role": "user",
                    "content": msg['text'][6:]  # Remove "User: " prefix
                })
            elif msg['text'].startswith('AI: '):
                messages.append({
                    "role": "assistant", 
                    "content": msg['text'][4:]  # Remove "AI: " prefix
                })
    
    # Add current user message
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    print(f"📝 Messages prepared: {len(messages)} messages")

    try:
        print("🚀 Calling OpenAI API...")
        print(f"   API Key (first 10 chars): {FIXED_API_KEY[:10]}...")
        print(f"   Model: {OPENAI_MODEL}")
        print(f"   Messages count: {len(messages)}")
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        print(f"✅ OpenAI API response received: {type(response)}")

        # Extract the response text
        if response.choices and len(response.choices) > 0:
            result = response.choices[0].message.content
            print(f"📝 Response text length: {len(result)}")
            return result
        else:
            print("⚠️ No response choices received")
            return "Error: No response received from OpenAI."

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error in AIResponse: {error_msg}")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Full error details: {e}")
        
        if "invalid_api_key" in error_msg.lower() or "expired" in error_msg.lower():
            return "❌ Error: API key is invalid or expired. Please update your OpenAI API key."
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            return "❌ Error: API quota exceeded or billing issue. Please check your OpenAI account."
        elif "rate_limit" in error_msg.lower():
            return "❌ Error: Rate limit exceeded. Please wait a moment and try again."
        else:
            return f"❌ Error generating response: {error_msg}"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get_chats", methods=['GET'])
def get_chats():
    return jsonify({'chats': chats})

@app.route("/get_chat_history", methods=['GET'])
def get_chat_history():
    chat_id = int(request.args.get('chat_id'))
    chat = next((chat for chat in chats if chat['id'] == chat_id), None)
    if chat:
        return jsonify({'messages': chat['messages']})
    return jsonify({'messages': []})

@app.route('/generate', methods=['POST'])
def generate():
    try:
    data = request.get_json()
    user_input = data.get('input')
    chat_id = data.get('chat_id')
        
        print(f"🔍 Received request - Input: '{user_input}', Chat ID: {chat_id}")

    chat = next((chat for chat in chats if chat['id'] == chat_id), None)
    chat_history = chat['messages'] if chat else []
        
        print(f"📝 Chat history length: {len(chat_history)}")

    response = AIResponse(user_input, chat_history)
        print(f"🤖 AI Response: {response[:100]}...")  # Show first 100 chars

    if chat:
        chat['messages'].append({'text': f'User: {user_input}'})
        chat['messages'].append({'text': f'AI: {response}'})
            print(f"💾 Messages saved to chat {chat_id}")

    return jsonify({'response': response})
        
    except Exception as e:
        print(f"❌ Error in generate endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/new_chat', methods=['POST'])
def new_chat():
    data = request.get_json()
    chat_name = data.get('chat_name')
    new_chat_id = len(chats) + 1
    new_chat = {'name': chat_name, 'id': new_chat_id, 'messages': []}
    chats.append(new_chat)
    return jsonify({'status': 'Chat created successfully', 'chat_id': new_chat_id})

@app.route('/delete_chat', methods=['POST'])
def delete_chat():
    data = request.get_json()
    chat_id = data.get('chat_id')
    global chats
    chats = [chat for chat in chats if chat['id'] != chat_id]
    return jsonify({'status': f'Chat {chat_id} deleted successfully'})

if __name__ == '__main__':
    # Get port from environment variable (for Railway, Render, etc.)
    port = int(os.environ.get('PORT', FLASK_PORT))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', str(FLASK_DEBUG)).lower() == 'true'
    print(f"🚀 Starting AI Chatbot on {host}:{port}")
    print(f"   Debug mode: {debug}")
    app.run(host=host, port=port, debug=debug)
