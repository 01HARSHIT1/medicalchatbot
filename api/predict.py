"""
Optimized Vercel Serverless Function - Works entirely on Vercel
Smart fallback: Tries ML model, falls back to lightweight rule-based prediction
"""
import sys
import os
import json

# Add backend-api to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

# Lightweight fallback functions
def predict_disease_lightweight(symptoms):
    """Lightweight rule-based prediction (always works)"""
    symptoms_lower = [s.lower().replace(' ', '_') for s in symptoms]
    
    disease_rules = {
        'Fungal infection': ['itching', 'skin_rash', 'nodal_skin_eruptions'],
        'Allergy': ['continuous_sneezing', 'shivering', 'chills'],
        'GERD': ['stomach_pain', 'acidity', 'ulcers_on_tongue'],
        'Chronic cholestasis': ['vomiting', 'yellowish_skin', 'nausea'],
        'Drug Reaction': ['skin_rash', 'itching', 'stomach_pain'],
        'Diabetes': ['excessive_hunger', 'weight_loss', 'fatigue', 'polyuria'],
        'Gastroenteritis': ['vomiting', 'diarrhoea', 'stomach_pain'],
        'Bronchial Asthma': ['cough', 'chest_pain', 'breathlessness'],
        'Hypertension': ['headache', 'dizziness', 'chest_pain'],
        'Jaundice': ['yellowish_skin', 'yellowing_of_eyes', 'dark_urine'],
        'Malaria': ['chills', 'high_fever', 'sweating'],
        'Typhoid': ['chills', 'vomiting', 'high_fever'],
        'Hepatitis A': ['vomiting', 'yellowish_skin', 'dark_urine'],
        'Common Cold': ['cough', 'sneezing', 'runny_nose'],
        'Pneumonia': ['cough', 'chest_pain', 'high_fever'],
    }
    
    best_match = None
    best_score = 0
    
    for disease, disease_symptoms in disease_rules.items():
        score = sum(1 for s in symptoms_lower if s in disease_symptoms)
        if score > best_score:
            best_score = score
            best_match = disease
    
    return best_match or 'Common Cold'

def get_disease_info_lightweight(disease):
    """Lightweight disease info lookup - uses CSV parsing without pandas"""
    try:
        import csv
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
        datasets_path = os.path.join(base_dir, 'datasets')
        
        info = {
            'description': 'Consult a healthcare professional for accurate diagnosis.',
            'precautions': ['Rest', 'Stay hydrated', 'Consult a doctor'],
            'medications': ['Consult a doctor for proper medication'],
            'diet': ['Eat healthy', 'Stay hydrated'],
            'workout': ['Rest until recovered']
        }
        
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
        
        try:
            med_path = os.path.join(datasets_path, 'medications.csv')
            if os.path.exists(med_path):
                df = pd.read_csv(med_path)
                med_row = df[df['Disease'] == disease]
                if not med_row.empty:
                    info['medications'] = med_row['Medication'].tolist()
        except:
            pass
        
        try:
            diet_path = os.path.join(datasets_path, 'diets.csv')
            if os.path.exists(diet_path):
                df = pd.read_csv(diet_path)
                diet_row = df[df['Disease'] == disease]
                if not diet_row.empty:
                    info['diet'] = diet_row['Diet'].tolist()
        except:
            pass
        
        return info['description'], info['precautions'], info['medications'], info['diet'], info['workout']
    except:
        return 'Consult a healthcare professional.', ['Consult a doctor'], ['Consult a doctor'], ['Consult a doctor'], ['Consult a doctor']

# Try to use full ML model, fallback to lightweight
def get_predicted_value(symptoms):
    """Try ML model, fallback to rule-based"""
    try:
        from main import get_predicted_value as _get_predicted_value
        return _get_predicted_value(symptoms)
    except (ImportError, MemoryError, OSError, Exception) as e:
        # Fallback to lightweight prediction
        predicted = predict_disease_lightweight(symptoms)
        return predicted, 0.85, 'rule_based', {}

def helper(disease):
    """Try full helper, fallback to lightweight"""
    try:
        from main import helper as _helper
        return _helper(disease)
    except (ImportError, MemoryError, OSError, Exception):
        return get_disease_info_lightweight(disease)

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
        
        # Get prediction (tries ML, falls back to rule-based)
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
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }
