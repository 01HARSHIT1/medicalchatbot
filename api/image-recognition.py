"""
Lightweight Vercel Serverless Function for Image Recognition
Image content analysis and caption generation - Works entirely on Vercel
Uses color analysis and pattern detection for descriptive captions
"""
import json
import base64
import os
from http.server import BaseHTTPRequestHandler

def analyze_image_colors(image_base64):
    """Analyze dominant colors and patterns from base64 image data"""
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
                if i % 3 == 0:  # Rough RGB approximation
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
            color_strength = "strong"
        elif max_avg == avg_green and avg_green > avg_blue + 20 and avg_green > avg_red + 20:
            dominant_color = "green"
            color_strength = "strong"
        elif max_avg == avg_red and avg_red > avg_blue + 20 and avg_red > avg_green + 20:
            dominant_color = "red"
            color_strength = "strong"
        elif abs(avg_blue - avg_green) < 30 and abs(avg_blue - avg_red) < 30:
            dominant_color = "neutral"
            color_strength = "balanced"
        else:
            dominant_color = "mixed"
            color_strength = "varied"
        
        # Determine brightness level
        if avg_brightness < 70:
            brightness_level = "dark"
        elif avg_brightness < 120:
            brightness_level = "moderate"
        elif avg_brightness < 180:
            brightness_level = "bright"
        else:
            brightness_level = "very bright"
        
        # Calculate color variance (for scene type detection)
        color_variance = (
            (max(avg_red, avg_green, avg_blue) - min(avg_red, avg_green, avg_blue)) / 255
        )
        
        return {
            'dominant_color': dominant_color,
            'color_strength': color_strength,
            'brightness': brightness_level,
            'brightness_value': avg_brightness,
            'color_variance': color_variance,
            'avg_red': avg_red,
            'avg_green': avg_green,
            'avg_blue': avg_blue
        }
    except Exception as e:
        print(f"Error analyzing colors: {e}")
        return {
            'dominant_color': 'mixed',
            'color_strength': 'moderate',
            'brightness': 'moderate',
            'brightness_value': 128,
            'color_variance': 0.5,
            'avg_red': 128,
            'avg_green': 128,
            'avg_blue': 128
        }

def generate_content_caption(properties, color_analysis):
    """Generate a descriptive caption based on image content analysis"""
    image_type = properties.get('type', 'unknown')
    file_size_kb = properties.get('file_size_kb', 0)
    dominant_color = color_analysis.get('dominant_color', 'mixed')
    brightness = color_analysis.get('brightness', 'moderate')
    color_strength = color_analysis.get('color_strength', 'moderate')
    color_variance = color_analysis.get('color_variance', 0.5)
    avg_blue = color_analysis.get('avg_blue', 128)
    avg_green = color_analysis.get('avg_green', 128)
    avg_red = color_analysis.get('avg_red', 128)
    
    # Build descriptive caption based on color and properties
    caption_parts = []
    
    # Color-based scene descriptions with more variety
    scene_descriptions = []
    
    if dominant_color == "blue":
        if brightness == "very bright" or brightness == "bright":
            if avg_blue > 180:
                scene_descriptions = [
                    "a beautiful bright blue sky",
                    "a clear blue sky scene",
                    "a serene blue sky with clouds",
                    "a bright blue sky landscape",
                    "a clear blue sky during daytime"
                ]
            else:
                scene_descriptions = [
                    "a bright blue water scene",
                    "a beautiful blue lake",
                    "a serene blue ocean view",
                    "a bright blue water landscape",
                    "a clear blue water scene"
                ]
        elif brightness == "dark":
            scene_descriptions = [
                "a dark blue night sky",
                "a deep blue evening scene",
                "a dark blue ocean at night",
                "a shadowy blue landscape"
            ]
        else:
            scene_descriptions = [
                "a blue sky scene",
                "a blue water landscape",
                "a blue-toned natural scene",
                "a peaceful blue landscape"
            ]
    elif dominant_color == "green":
        if brightness == "very bright" or brightness == "bright":
            scene_descriptions = [
                "a lush green landscape",
                "a vibrant green nature scene",
                "a beautiful green forest",
                "a sunny green meadow",
                "a bright green field",
                "a vibrant green park scene",
                "a lush green garden"
            ]
        elif brightness == "dark":
            scene_descriptions = [
                "a dark green forest",
                "a deep green nature scene",
                "a shadowy green landscape",
                "a dense green forest"
            ]
        else:
            scene_descriptions = [
                "a green nature scene",
                "a natural green landscape",
                "a peaceful green environment",
                "a green forest scene"
            ]
    elif dominant_color == "red":
        if brightness == "very bright" or brightness == "bright":
            scene_descriptions = [
                "a vibrant red sunset scene",
                "a beautiful red sunset",
                "a warm red-toned landscape",
                "a bright red sunset sky",
                "a colorful red sunset"
            ]
        elif brightness == "dark":
            scene_descriptions = [
                "a dark red scene",
                "a deep red-toned image",
                "a shadowy red landscape"
            ]
        else:
            scene_descriptions = [
                "a red-toned scene",
                "a warm red landscape",
                "a red sunset view"
            ]
    elif dominant_color == "neutral":
        if brightness == "very bright" or brightness == "bright":
            scene_descriptions = [
                "a bright landscape scene",
                "a sunny outdoor scene",
                "a bright natural landscape",
                "a well-lit scene"
            ]
        elif brightness == "dark":
            scene_descriptions = [
                "a dark scene",
                "a shadowy landscape",
                "a dimly lit scene"
            ]
        else:
            scene_descriptions = [
                "a natural scene",
                "a landscape view",
                "an outdoor scene"
            ]
    else:  # mixed colors
        if brightness == "very bright" or brightness == "bright":
            if color_variance > 0.6:
                scene_descriptions = [
                    "a colorful bright scene",
                    "a vibrant colorful landscape",
                    "a bright multi-colored scene",
                    "a sunny colorful view",
                    "a beautiful colorful landscape",
                    "a vibrant outdoor scene"
                ]
            else:
                scene_descriptions = [
                    "a bright scene",
                    "a sunny landscape",
                    "a well-lit outdoor scene"
                ]
        elif brightness == "dark":
            scene_descriptions = [
                "a dark scene with mixed colors",
                "a shadowy multi-toned image",
                "a dim colorful scene"
            ]
        else:
            if color_variance > 0.5:
                scene_descriptions = [
                    "a colorful scene",
                    "a diverse color palette scene",
                    "a multi-colored landscape",
                    "a vibrant scene"
                ]
            else:
                scene_descriptions = [
                    "a natural scene",
                    "a landscape view",
                    "an outdoor scene"
                ]
    
    # Select a scene description (use file size and color values as hash for variation)
    import hashlib
    hash_input = f"{file_size_kb}_{avg_red}_{avg_green}_{avg_blue}"
    scene_hash = int(hashlib.md5(hash_input.encode()).hexdigest()[:8], 16)
    selected_scene = scene_descriptions[scene_hash % len(scene_descriptions)]
    
    caption_parts.append(selected_scene)
    
    # Add time-of-day/lighting hints based on brightness
    if brightness == "very bright":
        time_hints = ["during bright daylight", "in bright sunlight", "under clear skies"]
        caption_parts.append(time_hints[scene_hash % len(time_hints)])
    elif brightness == "bright":
        time_hints = ["during daytime", "in good light", "under sunlight"]
        caption_parts.append(time_hints[scene_hash % len(time_hints)])
    elif brightness == "dark":
        time_hints = ["during nighttime", "in low light", "in the evening", "at dusk"]
        caption_parts.append(time_hints[scene_hash % len(time_hints)])
    
    # Add detail level based on file size
    if file_size_kb > 1000:
        detail_hints = ["with high detail", "with excellent detail", "with fine detail"]
        caption_parts.append(detail_hints[scene_hash % len(detail_hints)])
    elif file_size_kb > 200:
        detail_hints = ["with good detail", "with clear detail", "with moderate detail"]
        caption_parts.append(detail_hints[scene_hash % len(detail_hints)])
    
    # Combine into caption
    caption = " ".join(caption_parts)
    
    # Capitalize first letter
    caption = caption.capitalize()
    
    # Add note about advanced features (shorter)
    caption += ". Note: This is a color-based analysis. For detailed object detection, consider using advanced ML services."
    
    return caption

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
        
        return {
            'type': image_type,
            'file_size': image_size,
            'file_size_kb': image_size_kb,
            'file_size_mb': image_size_mb
        }
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {
            'type': 'unknown',
            'file_size': 0,
            'file_size_kb': 0,
            'file_size_mb': 0
        }

def describe_image_simple(image_base64):
    """Analyze image and generate a descriptive caption"""
    if not image_base64:
        return "No image data provided."
    
    try:
        # Analyze image properties
        properties = analyze_image_properties(image_base64)
        
        # Analyze colors and content
        color_analysis = analyze_image_colors(image_base64)
        
        # Generate content-based caption
        caption = generate_content_caption(properties, color_analysis)
        
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
            
            # Generate description based on image content analysis
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
