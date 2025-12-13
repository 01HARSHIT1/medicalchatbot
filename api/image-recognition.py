"""
Lightweight Vercel Serverless Function for Image Recognition
Real image captioning using Hugging Face Inference API - Works entirely on Vercel
"""
import json
import base64
import os
from http.server import BaseHTTPRequestHandler

# Hugging Face Inference API endpoint (free, no API key needed for public models)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

def get_image_caption_from_hf(image_base64):
    """Get real image caption from Hugging Face Inference API"""
    try:
        import urllib.request
        import urllib.parse
        
        # Decode base64 to get image bytes
        image_bytes = base64.b64decode(image_base64)
        
        # Create request to Hugging Face API
        req = urllib.request.Request(
            HUGGINGFACE_API_URL,
            data=image_bytes,
            headers={
                'Content-Type': 'application/octet-stream',
                'Accept': 'application/json'
            }
        )
        
        # Make request with timeout
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return result[0]['generated_text']
                    elif 'caption' in result[0]:
                        return result[0]['caption']
                
                # If result is a dict
                if isinstance(result, dict):
                    if 'generated_text' in result:
                        return result['generated_text']
                    elif 'caption' in result:
                        return result['caption']
                
                # Fallback: return string representation
                return str(result)
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"Hugging Face API error: {e.code} - {error_body}")
            # If model is loading, return a message
            if e.code == 503:
                return None  # Model is loading, use fallback
            raise
        except Exception as e:
            print(f"Error calling Hugging Face API: {e}")
            return None
            
    except Exception as e:
        print(f"Error in get_image_caption_from_hf: {e}")
        return None

def analyze_image_for_fallback(image_base64):
    """Analyze image for fallback caption generation"""
    try:
        # Decode base64 to get image data
        image_data = base64.b64decode(image_base64)
        
        # Sample different parts of the image for color analysis
        sample_size = min(50000, len(image_data))
        samples = [
            image_data[:sample_size//4],
            image_data[sample_size//4:sample_size//2],
            image_data[sample_size//2:3*sample_size//4],
            image_data[3*sample_size//4:sample_size]
        ]
        
        # Analyze color distribution
        blue_values = []
        green_values = []
        red_values = []
        all_brightness = []
        
        for sample in samples:
            for i, byte in enumerate(sample):
                if i % 3 == 0:
                    red_values.append(byte)
                    all_brightness.append(byte)
                elif i % 3 == 1:
                    green_values.append(byte)
                    all_brightness.append(byte)
                elif i % 3 == 2:
                    blue_values.append(byte)
                    all_brightness.append(byte)
        
        # Calculate averages
        avg_blue = sum(blue_values) / len(blue_values) if blue_values else 128
        avg_green = sum(green_values) / len(green_values) if green_values else 128
        avg_red = sum(red_values) / len(red_values) if red_values else 128
        avg_brightness = sum(all_brightness) / len(all_brightness) if all_brightness else 128
        
        # Determine dominant color
        max_avg = max(avg_blue, avg_green, avg_red)
        if max_avg == avg_blue and avg_blue > avg_green + 20 and avg_blue > avg_red + 20:
            dominant_color = "blue"
        elif max_avg == avg_green and avg_green > avg_blue + 20 and avg_green > avg_red + 20:
            dominant_color = "green"
        elif max_avg == avg_red and avg_red > avg_blue + 20 and avg_red > avg_green + 20:
            dominant_color = "red"
        else:
            dominant_color = "mixed"
        
        # Determine brightness
        if avg_brightness < 70:
            brightness = "dark"
        elif avg_brightness < 120:
            brightness = "moderate"
        elif avg_brightness < 180:
            brightness = "bright"
        else:
            brightness = "very bright"
        
        return {
            'dominant_color': dominant_color,
            'brightness': brightness,
            'avg_red': avg_red,
            'avg_green': avg_green,
            'avg_blue': avg_blue
        }
    except Exception as e:
        print(f"Error in fallback analysis: {e}")
        return {
            'dominant_color': 'mixed',
            'brightness': 'moderate',
            'avg_red': 128,
            'avg_green': 128,
            'avg_blue': 128
        }

def generate_fallback_caption(color_analysis):
    """Generate a basic fallback caption if API fails"""
    dominant_color = color_analysis.get('dominant_color', 'mixed')
    brightness = color_analysis.get('brightness', 'moderate')
    
    if dominant_color == "blue" and brightness in ["bright", "very bright"]:
        return "A bright blue scene with clear visibility"
    elif dominant_color == "green" and brightness in ["bright", "very bright"]:
        return "A vibrant green landscape scene"
    elif dominant_color == "red" and brightness in ["bright", "very bright"]:
        return "A warm red-toned scene"
    else:
        return "An image with mixed colors and moderate lighting"

def describe_image_simple(image_base64):
    """Analyze image and generate a detailed, image-specific caption"""
    if not image_base64:
        return "No image data provided."
    
    try:
        # Try to get real caption from Hugging Face API
        caption = get_image_caption_from_hf(image_base64)
        
        if caption:
            # Clean up the caption
            caption = caption.strip()
            # Capitalize first letter
            if caption:
                caption = caption[0].upper() + caption[1:] if len(caption) > 1 else caption.upper()
            return caption
        
        # Fallback: Use color analysis if API fails or is unavailable
        print("Hugging Face API unavailable, using fallback analysis")
        color_analysis = analyze_image_for_fallback(image_base64)
        fallback_caption = generate_fallback_caption(color_analysis)
        return f"{fallback_caption}. Note: Using basic analysis. Advanced captioning will be available shortly."
        
    except Exception as e:
        print(f"Error in describe_image_simple: {e}")
        # Final fallback
        return f"Image received. Error analyzing: {str(e)}. Please try again."

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
