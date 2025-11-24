from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load models
models = {}
model_files = {
    'lasso': 'Lasso.pkl',
    'linear': 'lin_reg.pkl',
    'polynomial': 'poly.pkl'
}

print("Loading models...")
for name, filename in model_files.items():
    try:
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                models[name] = pickle.load(f)
            print(f"Successfully loaded {name} model from {filename}")
        else:
            print(f"Warning: {filename} not found")
    except Exception as e:
        print(f"Error loading {name} model: {e}")

@app.route('/')
def home():
    return jsonify({
        "message": "ML Regression API is running!",
        "available_models": list(models.keys())
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
            
        model_type = data.get('model', 'linear')
        features = data.get('features')
        
        if features is None:
            return jsonify({'error': 'No features provided'}), 400
            
        if model_type not in models:
            return jsonify({'error': f'Model {model_type} not found. Available: {list(models.keys())}'}), 400
        
        model = models[model_type]
        
        # Convert features to numpy array
        # Reshape to (1, -1) for a single sample prediction
        features_arr = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features_arr)
        
        return jsonify({
            'model': model_type,
            'prediction': float(prediction[0])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
