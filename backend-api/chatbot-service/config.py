# Configuration file for the AI Chatbot
# This file contains your API key and other settings

# OpenAI API Key
# Get your API key from: https://platform.openai.com/api-keys
# IMPORTANT: Never commit your actual API key to GitHub!
# Use environment variables instead (see below)
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# Alternative: Use environment variable
# Set this in your system: export OPENAI_API_KEY="your_actual_key"
# Or in Windows: set OPENAI_API_KEY=your_actual_key

# Model configuration
OPENAI_MODEL = "gpt-3.5-turbo"

# Server configuration
FLASK_PORT = 5001
FLASK_DEBUG = True
