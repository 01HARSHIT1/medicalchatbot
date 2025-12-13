"""
Lightweight Vercel Serverless Function for Image Recognition
Image analysis and caption generation - Works entirely on Vercel
"""
import json
import base64
import os
from http.server import BaseHTTPRequestHandler

def analyze_image_properties(image_base64):
    """Analyze basic image properties from base64 data"""
    try:
        # Decode base64 to get image data
        image_data = base64.b64decode(image_base64)
        
        # Get image size
        image_size = len(image_data)
        
        # Try to determine image type from header
        image_type = "unknown"
        if image_data[:2] == b'\xff\xd8':
            image_type = "JPEG"
        elif image_data[:8] == b'\x89PNG\r\n\x1a\n':
            image_type = "PNG"
        elif image_data[:6] in [b'GIF87a', b'GIF89a']:
            image_type = "GIF"
        elif image_data[:2] == b'BM':
            image_type = "BMP"
        elif image_data[:4] == b'RIFF' and image_data[8:12] == b'WEBP':
            image_type = "WEBP"
        
        # Estimate dimensions (rough approximation based on file size)
        # This is a simple heuristic - not accurate but gives some variation
        if image_size < 50000:
            estimated_size = "small"
        elif image_size < 200000:
            estimated_size = "medium"
        elif image_size < 1000000:
            estimated_size = "large"
        else:
            estimated_size = "very large"
        
        return {
            'type': image_type,
            'size': estimated_size,
            'file_size': image_size
        }
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {
            'type': 'unknown',
            'size': 'unknown',
            'file_size': 0
        }

def generate_caption_from_properties(properties):
    """Generate a caption based on image properties"""
    image_type = properties.get('type', 'unknown')
    size = properties.get('size', 'unknown')
    
    # Generate contextual captions based on properties
    captions = []
    
    # Based on image type
    if image_type == "JPEG":
        captions.append("A JPEG photograph")
    elif image_type == "PNG":
        captions.append("A PNG image")
    elif image_type == "GIF":
        captions.append("A GIF image")
    else:
        captions.append("An image")
    
    # Based on size
    if size == "small":
        captions.append("with compact dimensions")
    elif size == "large":
        captions.append("with high resolution")
    elif size == "very large":
        captions.append("with very high resolution")
    
    # Combine into a caption
    base_caption = " ".join(captions)
    
    # Add contextual information
    file_size_kb = properties.get('file_size', 0) / 1024
    if file_size_kb > 0:
        base_caption += f" (approximately {file_size_kb:.1f} KB)"
    
    # Add helpful note
    base_caption += ". For detailed image analysis and ML-based captioning, consider integrating with advanced image recognition services."
    
    return base_caption

def describe_image_simple(image_base64):
    """Analyze image and generate a description"""
    if not image_base64:
        return "No image data provided."
    
    try:
        # Analyze image properties
        properties = analyze_image_properties(image_base64)
        
        # Generate caption based on properties
        caption = generate_caption_from_properties(properties)
        
        return caption
    except Exception as e:
        return f"Image received. Error analyzing image: {str(e)}. For detailed analysis, please use an advanced image recognition service."

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
            
            # Generate description based on image analysis
            description = describe_image_simple(image_data)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'caption': description,
                'message': 'Image analyzed successfully. For advanced ML-based captioning, consider integrating with dedicated image recognition services.'
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
