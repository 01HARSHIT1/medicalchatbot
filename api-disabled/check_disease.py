"""
Vercel Serverless Function for Disease Details - Lightweight version
"""
import sys
import os
import json
import csv

# Add backend-api to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

def load_dataset_lightweight(filename):
    """Lightweight CSV loader without pandas"""
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
    datasets_path = os.path.join(base_dir, 'datasets')
    file_path = os.path.join(datasets_path, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {filename}")
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

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
        if hasattr(request, 'json'):
            body = request.json
        elif hasattr(request, 'body'):
            body = json.loads(request.body) if isinstance(request.body, str) else request.body
        else:
            body = {}
        
        disease_name = body.get('disease_name', '')
        
        if not disease_name:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'No disease name provided'})
            }
        
        # Load symptoms dataset (lightweight CSV parsing)
        try:
            symptoms_data = load_dataset_lightweight('symtoms_df.csv')
            disease_symptoms = [row for row in symptoms_data if row.get('Disease', '').strip() == disease_name]
            
            if not disease_symptoms:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({'error': 'Disease not found'})
                }
            
            # Extract all unique symptoms
            all_symptoms = set()
            for row in disease_symptoms:
                for key, value in row.items():
                    if key.startswith('Symptom_') and value and str(value).strip():
                        all_symptoms.add(str(value).strip())
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': f'Error loading dataset: {str(e)}'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'disease_name': disease_name,
                'all_symptoms': list(all_symptoms),
                'symptom_count': len(all_symptoms)
            })
        }
        
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }
