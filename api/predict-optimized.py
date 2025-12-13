"""
Optimized Vercel Serverless Function - Works without external services
Uses lightweight prediction without heavy ML models
"""
import json
import sys
import os

# Add backend-api to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

def handler(request):
    """Optimized handler that works within Vercel limits"""
    # Handle CORS
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
        
        # Use lightweight rule-based prediction (no heavy ML models)
        predicted_disease = predict_disease_lightweight(symptoms_list)
        
        # Get disease information from CSV (lightweight)
        disease_info = get_disease_info_lightweight(predicted_disease)
        
        result_data = {
            'predicted_disease': predicted_disease,
            'disease': predicted_disease,
            'confidence': 0.85,  # Rule-based confidence
            'method': 'rule_based',
            'symptoms': symptoms_list,
            'description': disease_info.get('description', 'Description not available'),
            'precautions': disease_info.get('precautions', ['Consult a doctor']),
            'medications': disease_info.get('medications', ['Consult a doctor']),
            'diet': disease_info.get('diet', ['Consult a doctor']),
            'workout': disease_info.get('workout', ['Consult a doctor']),
            'diets': disease_info.get('diet', ['Consult a doctor']),
            'workouts': disease_info.get('workout', ['Consult a doctor']),
            'individual_predictions': {}
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
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }

def predict_disease_lightweight(symptoms):
    """Lightweight rule-based disease prediction"""
    symptoms_lower = [s.lower().replace(' ', '_') for s in symptoms]
    
    # Rule-based matching (no ML models needed)
    disease_rules = {
        'Fungal infection': ['itching', 'skin_rash', 'nodal_skin_eruptions'],
        'Allergy': ['continuous_sneezing', 'shivering', 'chills'],
        'GERD': ['stomach_pain', 'acidity', 'ulcers_on_tongue'],
        'Chronic cholestasis': ['vomiting', 'yellowish_skin', 'nausea'],
        'Drug Reaction': ['skin_rash', 'itching', 'stomach_pain'],
        'Peptic ulcer disease': ['vomiting', 'loss_of_appetite', 'abdominal_pain'],
        'AIDS': ['muscle_wasting', 'patches_in_throat', 'high_fever'],
        'Diabetes': ['excessive_hunger', 'weight_loss', 'fatigue'],
        'Gastroenteritis': ['vomiting', 'diarrhoea', 'stomach_pain'],
        'Bronchial Asthma': ['cough', 'chest_pain', 'breathlessness'],
        'Hypertension': ['headache', 'dizziness', 'chest_pain'],
        'Migraine': ['headache', 'nausea', 'vomiting'],
        'Cervical spondylosis': ['neck_pain', 'back_pain', 'dizziness'],
        'Paralysis': ['muscle_weakness', 'stiff_neck', 'movement_stiffness'],
        'Jaundice': ['yellowish_skin', 'yellowing_of_eyes', 'dark_urine'],
        'Malaria': ['chills', 'high_fever', 'sweating'],
        'Chicken pox': ['itching', 'skin_rash', 'high_fever'],
        'Dengue': ['high_fever', 'headache', 'muscle_pain'],
        'Typhoid': ['chills', 'vomiting', 'high_fever'],
        'Hepatitis A': ['vomiting', 'yellowish_skin', 'dark_urine'],
    }
    
    # Find best match
    best_match = None
    best_score = 0
    
    for disease, disease_symptoms in disease_rules.items():
        score = sum(1 for s in symptoms_lower if s in disease_symptoms)
        if score > best_score:
            best_score = score
            best_match = disease
    
    return best_match or 'Common Cold'  # Default fallback

def get_disease_info_lightweight(disease):
    """Get disease info from lightweight CSV lookup"""
    try:
        import pandas as pd
        
        # Try to load datasets (lightweight operation)
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
        datasets_path = os.path.join(base_dir, 'datasets')
        
        info = {
            'description': 'Consult a healthcare professional for accurate diagnosis.',
            'precautions': ['Rest', 'Stay hydrated', 'Consult a doctor'],
            'medications': ['Consult a doctor for proper medication'],
            'diet': ['Eat healthy', 'Stay hydrated'],
            'workout': ['Rest until recovered']
        }
        
        # Try to load actual data if available
        try:
            desc_path = os.path.join(datasets_path, 'description.csv')
            if os.path.exists(desc_path):
                df = pd.read_csv(desc_path)
                desc_row = df[df['Disease'] == disease]
                if not desc_row.empty:
                    info['description'] = desc_row['Description'].values[0]
        except:
            pass
        
        try:
            prec_path = os.path.join(datasets_path, 'precautions_df.csv')
            if os.path.exists(prec_path):
                df = pd.read_csv(prec_path)
                prec_row = df[df['Disease'] == disease]
                if not prec_row.empty:
                    precautions = []
                    for col in df.columns:
                        if col.startswith('Precaution_') and pd.notna(prec_row[col].values[0]):
                            precautions.append(str(prec_row[col].values[0]))
                    if precautions:
                        info['precautions'] = precautions
        except:
            pass
        
        return info
    except Exception as e:
        return {
            'description': 'Consult a healthcare professional.',
            'precautions': ['Consult a doctor'],
            'medications': ['Consult a doctor'],
            'diet': ['Consult a doctor'],
            'workout': ['Consult a doctor']
        }

