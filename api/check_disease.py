"""
Lightweight Vercel Serverless Function for Disease Details
Pure Python - No heavy dependencies
"""
import json
import csv
import os
from http.server import BaseHTTPRequestHandler

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
            
            disease_name = body.get('disease_name', '').strip()
            
            if not disease_name:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No disease name provided'}).encode('utf-8'))
                return
            
            # Load symptoms
            all_symptoms = load_disease_symptoms(disease_name)
            
            if not all_symptoms:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Disease not found'}).encode('utf-8'))
                return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'disease_name': disease_name,
                'all_symptoms': all_symptoms,
                'symptom_count': len(all_symptoms)
            }).encode('utf-8'))
            
        except Exception as e:
            import traceback
            error_details = str(e)
            print(f"ERROR in check_disease handler: {error_details}")
            print(f"Traceback: {traceback.format_exc()}")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'Server error: {error_details}'
            }).encode('utf-8'))
