from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load Linear Regression Model
MODEL_FILE = 'lin_reg.pkl'
model = None

print("Loading Linear Regression model...")
try:
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
        print(f"Successfully loaded model from {MODEL_FILE}")
    else:
        print(f"Error: {MODEL_FILE} not found")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        
        # Extract raw fields
        age = float(data.get("age"))
        sex = data.get("sex")
        bmi = float(data.get("bmi"))
        children = int(data.get("children"))
        smoker = data.get("smoker")
        region = data.get("region")
        
        # Preprocessing to match training data (One-Hot Encoding)
        # Expected columns based on error: 
        # age, bmi, children, sex_male, smoker_yes, region_northwest, region_southeast, region_southwest
        
        input_data = {
            "age": age,
            "bmi": bmi,
            "children": children,
            "sex_male": 1 if sex == "male" else 0,
            "smoker_yes": 1 if smoker == "yes" else 0,
            "region_northwest": 1 if region == "northwest" else 0,
            "region_southeast": 1 if region == "southeast" else 0,
            "region_southwest": 1 if region == "southwest" else 0
        }

        # Create DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Predict
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'model': 'linear',
            'prediction': float(prediction)
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
