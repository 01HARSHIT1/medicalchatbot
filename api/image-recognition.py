"""
Lightweight Vercel Serverless Function for Image Recognition
Real image captioning using Hugging Face Inference API - Works entirely on Vercel
"""
import json
import base64
import os
from http.server import BaseHTTPRequestHandler

# Hugging Face Inference API endpoints (free, no API key needed for public models)
# Try multiple models for better reliability
HUGGINGFACE_MODELS = [
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
    "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning",
    "https://api-inference.huggingface.co/models/microsoft/git-base"
]

def get_image_caption_from_hf(image_base64, model_url=None):
    """Get real image caption from Hugging Face Inference API"""
    models_to_try = [model_url] if model_url else HUGGINGFACE_MODELS
    
    for api_url in models_to_try:
        try:
            import urllib.request
            import urllib.error
            
            # Decode base64 to get image bytes
            image_bytes = base64.b64decode(image_base64)
            
            # Create request to Hugging Face API
            req = urllib.request.Request(
                api_url,
                data=image_bytes,
                headers={
                    'Content-Type': 'application/octet-stream',
                    'Accept': 'application/json'
                }
            )
            
            # Make request with timeout
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    result_data = response.read().decode('utf-8')
                    result = json.loads(result_data)
                    
                    # Handle different response formats
                    caption = None
                    
                    # Format 1: List with dict containing 'generated_text'
                    if isinstance(result, list) and len(result) > 0:
                        if isinstance(result[0], dict):
                            caption = result[0].get('generated_text') or result[0].get('caption')
                    
                    # Format 2: Dict with 'generated_text' or 'caption'
                    elif isinstance(result, dict):
                        caption = result.get('generated_text') or result.get('caption')
                    
                    # Format 3: Direct string
                    elif isinstance(result, str):
                        caption = result
                    
                    # Format 4: List of strings
                    elif isinstance(result, list) and len(result) > 0 and isinstance(result[0], str):
                        caption = result[0]
                    
                    if caption:
                        # Clean up the caption
                        caption = str(caption).strip()
                        # Remove any unwanted prefixes
                        if caption.lower().startswith('caption:'):
                            caption = caption[8:].strip()
                        # Capitalize first letter
                        if caption:
                            caption = caption[0].upper() + caption[1:] if len(caption) > 1 else caption.upper()
                        return caption
                    
                    # If we got a response but no caption, log it
                    print(f"Unexpected response format from {api_url}: {result}")
                    
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
                print(f"Hugging Face API error ({api_url}): {e.code} - {error_body}")
                
                # If model is loading (503), try next model
                if e.code == 503:
                    print(f"Model {api_url} is loading, trying next model...")
                    continue
                # If rate limit (429), try next model
                elif e.code == 429:
                    print(f"Rate limit on {api_url}, trying next model...")
                    continue
                # For other errors, try next model
                else:
                    continue
                    
            except urllib.error.URLError as e:
                print(f"URL error for {api_url}: {e}")
                continue
                
            except Exception as e:
                print(f"Error calling Hugging Face API ({api_url}): {e}")
                continue
                
        except Exception as e:
            print(f"Error in get_image_caption_from_hf for {api_url}: {e}")
            continue
    
    # If all models failed, return None
    return None

def describe_image_simple(image_base64):
    """Analyze image and generate a detailed, image-specific caption"""
    if not image_base64:
        return "No image data provided."
    
    try:
        # Try to get real caption from Hugging Face API
        print("Attempting to get caption from Hugging Face API...")
        caption = get_image_caption_from_hf(image_base64)
        
        if caption and caption.strip():
            print(f"Successfully got caption: {caption}")
            return caption
        
        # If API failed, try one more time with a different approach
        print("First attempt failed, retrying with alternative model...")
        caption = get_image_caption_from_hf(image_base64, HUGGINGFACE_MODELS[1] if len(HUGGINGFACE_MODELS) > 1 else None)
        
        if caption and caption.strip():
            print(f"Successfully got caption on retry: {caption}")
            return caption
        
        # If still failed, return a helpful message
        print("All Hugging Face API attempts failed")
        return "Unable to generate detailed caption at this time. The image recognition service is temporarily unavailable. Please try again in a few moments."
        
    except Exception as e:
        print(f"Error in describe_image_simple: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return f"Error analyzing image: {str(e)}. Please try again."

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
            
            # Get image data (base64)
            image_data = body.get('image', '')
            
            if not image_data:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No image provided'}).encode('utf-8'))
                return
            
            # Generate description using real image captioning
            description = describe_image_simple(image_data)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'caption': description,
                'message': 'Image analyzed successfully using AI-powered captioning.'
            }).encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = str(e)
            print(f"ERROR in image-recognition handler: {error_details}")
            print(f"Traceback: {traceback.format_exc()}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'Server error: {error_details}'
            }).encode('utf-8'))
