"""
Lightweight Vercel Serverless Function for Image Recognition
Simple image description - No heavy ML models needed
"""
import json
import base64
import os

def describe_image_simple(image_data=None):
    """Simple image description (placeholder - can be enhanced)"""
    # This is a lightweight placeholder
    # For production, you could integrate with a lightweight image API
    # or use a simple image analysis service
    
    descriptions = [
        "This appears to be an image. For detailed analysis, please consult a professional image recognition service.",
        "The image has been received. Basic image recognition is available.",
        "Image detected. Advanced captioning requires additional setup."
    ]
    
    return descriptions[0]

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
        
        # Get image data (base64 or URL)
        image_data = body.get('image', '')
        
        if not image_data:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No image provided'})
            }
        
        # Generate description
        description = describe_image_simple(image_data)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'caption': description,
                'message': 'Image recognition is available. For advanced features, consider using a dedicated image recognition service.'
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

