"""
Vercel Serverless Function for Disease Details
"""
import sys
import os
import json
import pandas as pd

# Add backend-api to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

from main import load_dataset

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
        
        # Load symptoms dataset
        symptoms_df = load_dataset('symtoms_df.csv')
        disease_symptoms = symptoms_df[symptoms_df['Disease'] == disease_name]
        
        if disease_symptoms.empty:
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
        for _, row in disease_symptoms.iterrows():
            symptom_cols = [col for col in row.index if col.startswith('Symptom_')]
            for col in symptom_cols:
                symptom = row[col]
                if pd.notna(symptom) and str(symptom).strip():
                    all_symptoms.add(str(symptom).strip())
        
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
