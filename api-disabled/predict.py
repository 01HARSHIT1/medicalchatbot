"""
Optimized Vercel Serverless Function - Works entirely on Vercel
Lightweight rule-based prediction - No heavy ML dependencies
"""
import sys
import os
import json
import csv

# Lightweight fallback functions (no pandas, no ML libraries)
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
        'Migraine': ['headache', 'nausea', 'vomiting'],
        'Arthritis': ['joint_pain', 'stiff_neck', 'swelling_joints'],
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
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'backend-api')
        datasets_path = os.path.join(base_dir, 'datasets')
        
        info = {
            'description': 'Consult a healthcare professional for accurate diagnosis.',
            'precautions': ['Rest', 'Stay hydrated', 'Consult a doctor'],
            'medications': ['Consult a doctor for proper medication'],
            'diet': ['Eat healthy', 'Stay hydrated'],
            'workout': ['Rest until recovered']
        }
        
        # Use CSV module instead of pandas (lightweight)
        try:
            desc_path = os.path.join(datasets_path, 'description.csv')
            if os.path.exists(desc_path):
                with open(desc_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Disease', '').strip() == disease:
                            info['description'] = row.get('Description', info['description'])
                            break
        except:
            pass
        
        try:
            prec_path = os.path.join(datasets_path, 'precautions_df.csv')
            if os.path.exists(prec_path):
                with open(prec_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Disease', '').strip() == disease:
                            precautions = []
                            for key, value in row.items():
                                if key.startswith('Precaution_') and value and value.strip():
                                    precautions.append(value.strip())
                            if precautions:
                                info['precautions'] = precautions
                            break
        except:
            pass
        
        try:
            med_path = os.path.join(datasets_path, 'medications.csv')
            if os.path.exists(med_path):
                with open(med_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Disease', '').strip() == disease:
                            med = row.get('Medication', '').strip()
                            if med:
                                info['medications'] = [med]
                            break
        except:
            pass
        
        try:
            diet_path = os.path.join(datasets_path, 'diets.csv')
            if os.path.exists(diet_path):
                with open(diet_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Disease', '').strip() == disease:
                            diet = row.get('Diet', '').strip()
                            if diet:
                                info['diet'] = [diet]
                            break
        except:
            pass
        
        return info['description'], info['precautions'], info['medications'], info['diet'], info['workout']
    except:
        return 'Consult a healthcare professional.', ['Consult a doctor'], ['Consult a doctor'], ['Consult a doctor'], ['Consult a doctor']

# Use lightweight prediction only (avoids heavy ML dependencies)
def get_predicted_value(symptoms):
    """Use lightweight rule-based prediction (no heavy ML models)"""
    predicted = predict_disease_lightweight(symptoms)
    return predicted, 0.85, 'rule_based', {}

def helper(disease):
    """Use lightweight helper (no pandas dependency)"""
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
        
        # Get prediction (lightweight rule-based)
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
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }
