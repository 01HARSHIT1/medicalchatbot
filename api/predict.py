"""
Vercel Serverless Function for Medical Prediction
No Railway needed - runs directly on Vercel!
"""
import sys
import os
import json
import pandas as pd

# Add backend-api to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

# Import the prediction logic
try:
    from main import get_predicted_value, helper
except ImportError:
    # Fallback if import fails
    def get_predicted_value(symptoms):
        return "Error: Backend not configured", 0.0, "error", {}
    def helper(disease):
        return "Error", ["Error"], ["Error"], ["Error"], ["Error"]

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
    
    # Only allow POST
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
        # Get request body
        if hasattr(request, 'json'):
            body = request.json
        elif hasattr(request, 'body'):
            body = json.loads(request.body) if isinstance(request.body, str) else request.body
        else:
            body = {}
        
        symptoms_input = body.get('symptoms', [])
        
        # Process symptoms
        if isinstance(symptoms_input, list):
            symptoms_list = [str(s).strip() for s in symptoms_input if s and str(s).strip()]
        else:
            symptoms_list = [s.strip() for s in str(symptoms_input).split(',') if s.strip()]
        
        if not symptoms_list:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Please enter at least one symptom'})
            }
        
        # Get prediction
        predicted_disease, confidence, method, individual_predictions = get_predicted_value(symptoms_list)
        
        if method == 'error':
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': f'Prediction error: {predicted_disease}'})
            }
        
        # Get disease information
        description, precautions, medications, diets, workouts = helper(predicted_disease)
        
        # Prepare result
        result_data = {
            'predicted_disease': predicted_disease,
            'disease': predicted_disease,
            'confidence': confidence,
            'method': method,
            'symptoms': symptoms_list,
            'description': description,
            'precautions': precautions,
            'medications': medications,
            'diet': diets,
            'workout': workouts,
            'diets': diets,
            'workouts': workouts,
            'individual_predictions': individual_predictions
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result_data)
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': f'An error occurred: {str(e)}', 'details': error_details})
        }
