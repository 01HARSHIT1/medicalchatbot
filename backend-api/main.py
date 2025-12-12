from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import warnings
import sys
import os
import json

# Add the models directory to the path
models_path = os.path.join(os.path.dirname(__file__), 'models')
if os.path.exists(models_path):
    sys.path.append(models_path)

# Try to import the improved enhanced model
try:
    from improved_enhanced_model import ImprovedEnhancedMedicalPredictor
except ImportError:
    ImprovedEnhancedMedicalPredictor = None
    print("Warning: improved_enhanced_model not found")

warnings.filterwarnings('ignore')

app = Flask(__name__)

# Enable CORS manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Global predictor instance
_predictor = None

def get_predictor():
    """Get or create the predictor instance"""
    global _predictor
    if _predictor is None:
        try:
            _predictor = ImprovedEnhancedMedicalPredictor()
            
            # Try to load pre-trained models with fallback paths
            base_dir = os.path.dirname(__file__)
            model_paths = [
                os.path.join(base_dir, 'models', 'improved_enhanced_models.pkl'),
                os.path.join(base_dir, '..', 'models', 'improved_enhanced_models.pkl'),
                'models/improved_enhanced_models.pkl'
            ]
            
            model_loaded = False
            for model_path in model_paths:
                if os.path.exists(model_path):
                    try:
                        with open(model_path, 'rb') as f:
                            data = pickle.load(f)
                            _predictor.models = data['models']
                            _predictor.label_encoder = data['label_encoder']
                            _predictor.feature_names = data['feature_names']
                        print(f"✅ Pre-trained models loaded successfully from {model_path}!")
                        model_loaded = True
                        break
                    except Exception as e:
                        print(f"Error loading model from {model_path}: {e}")
                        continue
            
            if not model_loaded:
                # Train new models if pre-trained ones don't exist
                print("Training new models...")
                try:
                    enhanced_data = _predictor.load_and_preprocess_data()
                    X_test, y_test = _predictor.train_models(enhanced_data)
                    print("✅ New models trained successfully!")
                except Exception as e:
                    print(f"Error training models: {e}")
                    _predictor = None
        except Exception as e:
            print(f"Error initializing predictor: {e}")
            _predictor = None
    return _predictor

# Load the datasets - try local first, then fallback to relative paths
def load_dataset(filename):
    """Load dataset with fallback paths"""
    base_dir = os.path.dirname(__file__)
    # Try local datasets folder first (for deployment)
    local_path = os.path.join(base_dir, 'datasets', filename)
    if os.path.exists(local_path):
        return pd.read_csv(local_path)
    # Try parent datasets folder
    parent_path = os.path.join(base_dir, '..', 'datasets', filename)
    if os.path.exists(parent_path):
        return pd.read_csv(parent_path)
    raise FileNotFoundError(f"Dataset not found: {filename}. Make sure datasets are in the backend-api/datasets folder.")

# Load datasets
try:
    description = load_dataset('description.csv')
    precautions = load_dataset('precautions_df.csv')
    medications = load_dataset('medications.csv')
    diets = load_dataset('diets.csv')
    workout = load_dataset('workout_df.csv')
except Exception as e:
    print(f"Error loading datasets: {e}")
    # Create empty dataframes as fallback
    description = pd.DataFrame()
    precautions = pd.DataFrame()
    medications = pd.DataFrame()
    diets = pd.DataFrame()
    workout = pd.DataFrame()

def helper(dis):
    """Helper function to get disease information"""
    try:
        # Clean disease name (remove extra spaces)
        clean_dis = dis.strip()
        
        # Get description
        desc = description[description['Disease'] == clean_dis]['Description'].values
        if len(desc) > 0:
            desc = desc[0]
        else:
            desc = "Description not available"
        
        # Get precautions
        prec_cols = [col for col in precautions.columns if col.startswith('Precaution_')]
        prec = []
        for col in prec_cols:
            val = precautions[precautions['Disease'] == clean_dis][col].values
            if len(val) > 0 and pd.notna(val[0]) and val[0].strip():
                prec.append(val[0])
        if not prec:
            prec = ["Precautions not available"]
        
        # Get medications
        med = medications[medications['Disease'] == clean_dis]['Medication'].values
        if len(med) > 0:
            med = med.tolist()
        else:
            med = ["Medications not available"]
        
        # Get diets
        diet = diets[diets['Disease'] == clean_dis]['Diet'].values
        if len(diet) > 0:
            diet = diet.tolist()
        else:
            diet = ["Diet information not available"]
        
        # Get workouts (note: workout dataset uses lowercase 'disease' column)
        work = workout[workout['disease'] == clean_dis]['workout'].values
        if len(work) > 0:
            work = work.tolist()
        else:
            work = ["Workout information not available"]
        
        return desc, prec, med, diet, work
    except Exception as e:
        print(f"Error in helper function: {e}")
        return "Error occurred", ["Error"], ["Error"], ["Error"], ["Error"]

def get_predicted_value(patient_symptoms):
    """Get predicted disease using the improved enhanced model directly"""
    try:
        predictor = get_predictor()
        if predictor is None:
            return "Error: Model not available", 0.0, "error", {}
        
        # Get prediction
        predicted_disease, predictions, probabilities = predictor.predict_disease(patient_symptoms)
        
        # Debug: Print what we're getting from the predictor
        print(f"DEBUG: predicted_disease = {predicted_disease}")
        print(f"DEBUG: predictions = {predictions}")
        print(f"DEBUG: probabilities = {probabilities}")
        
        # Load disease names mapping from the symptoms dataset
        try:
            symptoms_df = load_dataset('symtoms_df.csv')
            disease_names = symptoms_df['Disease'].unique().tolist()
            print(f"DEBUG: Available diseases = {disease_names}")
        except Exception as e:
            print(f"DEBUG: Error loading disease names: {e}")
            disease_names = []
        
        # Calculate confidence from probabilities
        max_confidence = 0
        individual_predictions = {}
        
        # Map model names to template keys
        model_mapping = {
            'random_forest': 'random_forest',
            'gradient_boosting': 'gradient_boosting', 
            'svm': 'svm',
            'neural_network': 'neural_network'
        }
        
        for name, prob in probabilities.items():
            max_prob = max(prob)
            if max_prob > max_confidence:
                max_confidence = max_prob
            
            # Store individual model predictions with standardized names
            if name in predictions:
                # Convert model name to lowercase and replace spaces/underscores
                clean_name = name.lower().replace(' ', '_').replace('-', '_')
                if clean_name in model_mapping:
                    # Convert numerical prediction to disease name
                    prediction_value = predictions[name]
                    disease_name = predicted_disease  # Default to main prediction
                    
                    # If prediction is a number, try to map it to disease name
                    if isinstance(prediction_value, (int, float)) and disease_names:
                        try:
                            prediction_index = int(prediction_value)
                            if 0 <= prediction_index < len(disease_names):
                                disease_name = disease_names[prediction_index]
                        except (ValueError, IndexError):
                            disease_name = predicted_disease
                    elif isinstance(prediction_value, str):
                        disease_name = prediction_value
                    
                    individual_predictions[model_mapping[clean_name]] = {
                        'disease': disease_name,
                        'confidence': max_prob
                    }
        
        print(f"DEBUG: individual_predictions = {individual_predictions}")
        
        # Check if any medical rules were applied
        rule_applied = check_rules_applied(patient_symptoms, predicted_disease)
        method = 'rule_validation' if rule_applied else 'ml_prediction'
        
        return predicted_disease, max_confidence, method, individual_predictions
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Error occurred during prediction", 0.0, "error", {}

def check_rules_applied(symptoms, predicted_disease):
    """Check if any medical rules were applied"""
    symptoms_lower = [s.lower() for s in symptoms]
    
    # Rule 1: Diabetes vs Hyperthyroidism
    if predicted_disease == 'Diabetes ':
        if ('irregular_sugar_level' in symptoms_lower or 'polyuria' in symptoms_lower) and 'mood_swings' not in symptoms_lower:
            return True
    
    # Rule 2: Typhoid
    if predicted_disease == 'Typhoid':
        if 'chills' in symptoms_lower and 'vomiting' in symptoms_lower and 'high_fever' in symptoms_lower:
            return True
    
    # Rule 3: Fungal infection
    if predicted_disease == 'Fungal infection':
        if 'itching' in symptoms_lower and 'skin_rash' in symptoms_lower and 'nodal_skin_eruptions' in symptoms_lower:
            return True
    
    return False

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Support both JSON and form data
        if request.is_json:
            data = request.get_json()
            symptoms_input = data.get('symptoms', [])
            if isinstance(symptoms_input, list):
                symptoms_list = [s.strip() for s in symptoms_input if s and s.strip()]
            else:
                symptoms_list = [s.strip() for s in str(symptoms_input).split(',') if s.strip()]
        else:
            user_symptoms = request.form.get('symptoms', '')
            symptoms_list = [symptom.strip() for symptom in user_symptoms.split(',') if symptom.strip()]
        
        if not symptoms_list:
            if request.is_json:
                return jsonify({'error': 'Please enter at least one symptom'}), 400
            return render_template('index.html', error="Please enter at least one symptom")
        
        # Get prediction using improved system
        predicted_disease, confidence, method, individual_predictions = get_predicted_value(symptoms_list)
        
        if method == 'error':
            if request.is_json:
                return jsonify({'error': f'Prediction error: {predicted_disease}'}), 500
            return render_template('index.html', error=f"Prediction error: {predicted_disease}")
        
        # Get disease information
        description, precautions, medications, diets, workouts = helper(predicted_disease)
        
        # Prepare result data
        result_data = {
            'predicted_disease': predicted_disease,
            'disease': predicted_disease,  # Support both keys
            'confidence': confidence,
            'method': method,
            'symptoms': symptoms_list,
            'description': description,
            'precautions': precautions,
            'medications': medications,
            'diet': diets,
            'workout': workouts,
            'diets': diets,  # Support both keys
            'workouts': workouts,  # Support both keys
            'individual_predictions': individual_predictions
        }
        
        # Return JSON for API requests, template for form submissions
        if request.is_json:
            return jsonify(result_data)
        return render_template('index.html', result=result_data)
        
    except Exception as e:
        print(f"Error in predict route: {e}")
        if request.is_json:
            return jsonify({'error': 'An error occurred during prediction'}), 500
        return render_template('index.html', error="An error occurred during prediction")

@app.route('/check_disease', methods=['POST'])
def check_disease():
    try:
        # Support both JSON and form data
        if request.is_json:
            data = request.get_json()
            disease_name = data.get('disease_name', '')
        else:
            disease_name = request.form.get('disease_name', '')
        
        if not disease_name:
            return jsonify({'error': 'No disease name provided'}), 400
        
        # Get all symptoms for the given disease from the symptoms dataset
        try:
            symptoms_df = load_dataset('symtoms_df.csv')
            disease_symptoms = symptoms_df[symptoms_df['Disease'] == disease_name]
            
            if disease_symptoms.empty:
                return jsonify({'error': 'Disease not found'}), 404
            
            # Extract all unique symptoms for this disease
            all_symptoms = set()
            for _, row in disease_symptoms.iterrows():
                # Check all symptom columns (Symptom_1, Symptom_2, Symptom_3, Symptom_4, etc.)
                symptom_cols = [col for col in row.index if col.startswith('Symptom_')]
                for col in symptom_cols:
                    symptom = row[col]
                    if pd.notna(symptom) and str(symptom).strip():
                        all_symptoms.add(str(symptom).strip())
            
            return jsonify({
                'disease_name': disease_name,
                'all_symptoms': list(all_symptoms),
                'symptom_count': len(all_symptoms)
            })
        except Exception as e:
            print(f"Error in check_disease route: {e}")
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
        
    except Exception as e:
        print(f"Error in check_disease route: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chatbot')
def chatbot():
    # Get disease data from URL parameters
    disease_name = request.args.get('disease', '')
    disease_data = request.args.get('data', '')
    
    # Parse the disease data if available
    parsed_data = {}
    if disease_data:
        try:
            parsed_data = json.loads(disease_data)
        except:
            parsed_data = {}
    
    # Pass the disease data to the chatbot template
    return render_template('chatbot.html', 
                         disease_name=disease_name, 
                         disease_data=parsed_data)

if __name__ == '__main__':
    # Get port from environment variable (for Railway, Render, etc.)
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host=host, port=port, debug=debug)