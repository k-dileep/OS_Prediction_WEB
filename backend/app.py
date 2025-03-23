from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import tensorflow as tf
from tensorflow.keras.optimizers import Adam

app = Flask(__name__)
# Configure CORS to accept requests from your frontend domain
CORS(app, origins=[
    "http://localhost:3000",  # Development
    "https://your-frontend-domain.vercel.app"  # Production - update this with your actual domain
])

try:
    print("Loading model and preprocessing components...")
    # Load the ML model
    model = tf.keras.models.load_model('model.h5', compile=False)
    print("Model loaded successfully")
    
    # Create polynomial features transformer directly (degree=2 as in the notebook)
    poly = PolynomialFeatures(degree=2)
    print("Polynomial features created successfully")
    
    # Load the scaler from pickle
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    print("Scaler loaded successfully")
    
    sod_threshold = 3.5
    print("All components loaded successfully!")

except Exception as e:
    print(f"Error loading components: {str(e)}")
    raise e

def classify_oxidative_stress(radiation, fibrinogen):
    try:
        # Prepare the input data with polynomial transformation and scaling
        input_data = np.array([[radiation, fibrinogen]])
        input_data_poly = poly.fit_transform(input_data)  # Using fit_transform instead of transform
        input_data_scaled = scaler.transform(input_data_poly)
        predicted_sod = float(model.predict(input_data_scaled)[0][0])

        # Classify based on threshold
        status = "Exposed to Oxidative Stress" if predicted_sod > sod_threshold else "Not Exposed to Oxidative Stress"
        return predicted_sod, status
    except Exception as e:
        print(f"Error in classification: {str(e)}")
        raise e

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        radiation = float(data.get('radiation'))
        fibrinogen = float(data.get('fibrinogen'))
        
        predicted_sod, status = classify_oxidative_stress(radiation, fibrinogen)
        
        return jsonify({
            'success': True,
            'predicted_sod': predicted_sod,
            'status': status,
            'threshold': sod_threshold
        })
    except Exception as e:
        print(f"Error in prediction endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 