"""
Lightweight Vercel Serverless Function for Medical Prediction
Pure Python - No heavy dependencies - Works entirely on Vercel
"""
import json
import csv
import os
from http.server import BaseHTTPRequestHandler

# Lightweight disease prediction rules (no ML models needed)
DISEASE_RULES = {
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
    'AIDS': ['muscle_wasting', 'patches_in_throat', 'high_fever'],
    'Chicken pox': ['itching', 'skin_rash', 'high_fever'],
    'Dengue': ['high_fever', 'skin_rash', 'headache'],
    'Tuberculosis': ['cough', 'chest_pain', 'breathlessness'],
}

# Default disease information
DEFAULT_INFO = {
    'description': 'Consult a healthcare professional for accurate diagnosis and treatment.',
    'precautions': ['Rest', 'Stay hydrated', 'Consult a doctor', 'Follow medical advice'],
    'medications': ['Consult a doctor for proper medication'],
    'diet': ['Eat healthy', 'Stay hydrated', 'Follow doctor\'s dietary recommendations'],
    'workout': ['Rest until recovered', 'Follow doctor\'s exercise recommendations']
}

def normalize_symptom(symptom):
    """Normalize symptom name for matching"""
    return symptom.lower().strip().replace(' ', '_').replace('-', '_')

def predict_disease(symptoms):
    """Lightweight rule-based prediction"""
    if not symptoms:
        return 'Common Cold', 0.5
    
    symptoms_normalized = [normalize_symptom(s) for s in symptoms]
    best_match = None
    best_score = 0
    
    for disease, disease_symptoms in DISEASE_RULES.items():
        score = sum(1 for s in symptoms_normalized if normalize_symptom(s) in disease_symptoms)
        if score > best_score:
            best_score = score
            best_match = disease
    
    # Calculate confidence (simple heuristic)
    confidence = min(0.95, 0.5 + (best_score / max(len(symptoms), 1)) * 0.3)
    
    return best_match or 'Common Cold', confidence

def load_disease_info(disease_name):
    """Load disease information from CSV files (lightweight)"""
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'backend-api', 'datasets')
    info = DEFAULT_INFO.copy()
    
    # Try to load from description.csv
    try:
        desc_path = os.path.join(base_dir, 'description.csv')
        if os.path.exists(desc_path):
            with open(desc_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Disease', '').strip() == disease_name:
                        info['description'] = row.get('Description', info['description'])
                        break
    except Exception:
        pass
    
    # Try to load from precautions_df.csv
    try:
        prec_path = os.path.join(base_dir, 'precautions_df.csv')
        if os.path.exists(prec_path):
            with open(prec_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Disease', '').strip() == disease_name:
                        precautions = []
                        for i in range(1, 5):
                            prec = row.get(f'Precaution_{i}', '').strip()
                            if prec:
                                precautions.append(prec)
                        if precautions:
                            info['precautions'] = precautions
                        break
    except Exception:
        pass
    
    # Try to load from medications.csv
    try:
        med_path = os.path.join(base_dir, 'medications.csv')
        if os.path.exists(med_path):
            with open(med_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Disease', '').strip() == disease_name:
                        med = row.get('Medication', '').strip()
                        if med:
                            info['medications'] = [med]
                        break
    except Exception:
        pass
    
    # Try to load from diets.csv
    try:
        diet_path = os.path.join(base_dir, 'diets.csv')
        if os.path.exists(diet_path):
            with open(diet_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Disease', '').strip() == disease_name:
                        diet = row.get('Diet', '').strip()
                        if diet:
                            info['diet'] = [diet]
                        break
    except Exception:
        pass
    
    return info

# Vercel serverless function handler - Correct format using BaseHTTPRequestHandler
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
            
            # Extract symptoms
            symptoms_input = body.get('symptoms', [])
            
            # Process symptoms
            if isinstance(symptoms_input, list):
                symptoms_list = [str(s).strip() for s in symptoms_input if s and str(s).strip()]
            else:
                symptoms_list = [s.strip() for s in str(symptoms_input).split(',') if s.strip()]
            
            if not symptoms_list:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Please enter at least one symptom'}).encode('utf-8'))
                return
            
            # Get prediction
            predicted_disease, confidence = predict_disease(symptoms_list)
            
            # Get disease information
            disease_info = load_disease_info(predicted_disease)
            
            # Prepare result
            result_data = {
                'predicted_disease': predicted_disease,
                'disease': predicted_disease,
                'confidence': confidence,
                'method': 'rule_based',
                'symptoms': symptoms_list,
                'description': disease_info['description'],
                'precautions': disease_info['precautions'],
                'medications': disease_info['medications'],
                'diet': disease_info['diet'],
                'workout': disease_info['workout'],
                'diets': disease_info['diet'],
                'workouts': disease_info['workout']
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result_data).encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = str(e)
            error_trace = traceback.format_exc()
            print(f"ERROR in predict handler: {error_details}")
            print(f"Traceback: {error_trace}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'Server error: {error_details}'
            }).encode('utf-8'))
