"""
Lightweight Vercel Serverless Function for Disease Details
Pure Python - No heavy dependencies
"""
import json
import csv
import os

def load_disease_symptoms(disease_name):
    """Load all symptoms for a disease from CSV (lightweight)"""
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'backend-api', 'datasets')
    symptoms_path = os.path.join(base_dir, 'symtoms_df.csv')
    
    all_symptoms = set()
    
    try:
        if os.path.exists(symptoms_path):
            with open(symptoms_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Disease', '').strip() == disease_name:
                        # Extract all symptom columns
                        for col_name, symptom_value in row.items():
                            if col_name.startswith('Symptom_') and symptom_value and str(symptom_value).strip():
                                all_symptoms.add(str(symptom_value).strip())
    except Exception as e:
        print(f"Error loading symptoms: {e}")
    
    return list(all_symptoms)

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
        # Get request body
        if hasattr(request, 'json'):
            body = request.json
        elif hasattr(request, 'body'):
            body = json.loads(request.body) if isinstance(request.body, str) else request.body
        else:
            body = {}
        
        disease_name = body.get('disease_name', '').strip()
        
        if not disease_name:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No disease name provided'})
            }
        
        # Load symptoms
        all_symptoms = load_disease_symptoms(disease_name)
        
        if not all_symptoms:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Disease not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'disease_name': disease_name,
                'all_symptoms': all_symptoms,
                'symptom_count': len(all_symptoms)
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
