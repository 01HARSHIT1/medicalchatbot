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
        image_size_kb = image_size / 1024
        image_size_mb = image_size_kb / 1024
        
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
        
        # Estimate dimensions (rough approximation based on file size and type)
        # This is a simple heuristic - not accurate but gives some variation
        if image_type == "JPEG":
            # JPEG compression varies, but we can estimate
            if image_size < 50000:
                estimated_size = "small"
                estimated_resolution = "low resolution"
            elif image_size < 200000:
                estimated_size = "medium"
                estimated_resolution = "medium resolution"
            elif image_size < 1000000:
                estimated_size = "large"
                estimated_resolution = "high resolution"
            else:
                estimated_size = "very large"
                estimated_resolution = "very high resolution"
        elif image_type == "PNG":
            # PNG is usually larger for same quality
            if image_size < 100000:
                estimated_size = "small"
                estimated_resolution = "low resolution"
            elif image_size < 500000:
                estimated_size = "medium"
                estimated_resolution = "medium resolution"
            elif image_size < 2000000:
                estimated_size = "large"
                estimated_resolution = "high resolution"
            else:
                estimated_size = "very large"
                estimated_resolution = "very high resolution"
        else:
            estimated_size = "medium"
            estimated_resolution = "standard resolution"
        
        # Analyze color complexity (rough estimate based on file size vs type)
        if image_type in ["JPEG", "PNG"]:
            if image_size > 500000:
                complexity = "detailed"
            elif image_size > 100000:
                complexity = "moderately detailed"
            else:
                complexity = "simple"
        else:
            complexity = "standard"
        
        return {
            'type': image_type,
            'size': estimated_size,
            'resolution': estimated_resolution,
            'complexity': complexity,
            'file_size': image_size,
            'file_size_kb': image_size_kb,
            'file_size_mb': image_size_mb
        }
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {
            'type': 'unknown',
            'size': 'unknown',
            'resolution': 'unknown',
            'complexity': 'unknown',
            'file_size': 0,
            'file_size_kb': 0,
            'file_size_mb': 0
        }

def generate_caption_from_properties(properties):
    """Generate a detailed caption based on image properties"""
    image_type = properties.get('type', 'unknown')
    size = properties.get('size', 'unknown')
    resolution = properties.get('resolution', 'unknown')
    complexity = properties.get('complexity', 'unknown')
    file_size_kb = properties.get('file_size_kb', 0)
    file_size_mb = properties.get('file_size_mb', 0)
    
    # Build caption parts
    caption_parts = []
    
    # Image type description
    type_descriptions = {
        'JPEG': 'A JPEG photograph',
        'PNG': 'A PNG image',
        'GIF': 'A GIF image',
        'BMP': 'A BMP image',
        'WEBP': 'A WebP image'
    }
    caption_parts.append(type_descriptions.get(image_type, 'An image'))
    
    # Size and resolution
    if resolution != 'unknown':
        caption_parts.append(f"with {resolution}")
    
    # Complexity
    if complexity != 'unknown':
        caption_parts.append(f"and {complexity} content")
    
    # File size
    if file_size_mb >= 1:
        caption_parts.append(f"(file size: {file_size_mb:.2f} MB)")
    elif file_size_kb >= 1:
        caption_parts.append(f"(file size: {file_size_kb:.1f} KB)")
    
    # Combine into caption
    caption = " ".join(caption_parts)
    
    # Add contextual note
    caption += ". This is a basic image analysis. For detailed ML-based captioning with object detection and scene understanding, consider integrating with advanced image recognition services like Google Vision API or AWS Rekognition."
    
    return caption

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
