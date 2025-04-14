from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import os
import pickle
import numpy as np
import warnings

# Suppress TensorFlow warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings('ignore')

# Get the absolute directory path for properly setting up templates
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, 
    template_folder=template_dir,
    static_folder=os.path.join(current_dir, 'static')
)

# Configure CORS to accept requests from your frontend domain
CORS(app, origins=[
    "http://localhost:3000",  # Development
    "https://your-frontend-domain.vercel.app",  # Production - update this with your actual domain
    "https://os-prediction-backend.onrender.com",  # Your deployed backend URL
    "*"  # Allow all origins for testing
])

# Initialize Flask-RestX API with documentation
api = Api(
    app,
    version='1.0',
    title='Oxidative Stress Prediction API',
    description='API for predicting oxidative stress levels based on radiation and fibrinogen inputs',
    doc='/swagger',  # Swagger UI will be available at /swagger URL
    default='Predictions',
    default_label='Prediction operations'
)

# Define the data model for input validation and Swagger documentation
prediction_input = api.model('PredictionInput', {
    'radiation': fields.Float(required=True, description='Radiation level'),
    'fibrinogen': fields.Float(required=True, description='Fibrinogen level')
})

# Define the response model for Swagger documentation
prediction_output = api.model('PredictionOutput', {
    'success': fields.Boolean(description='Success status of the prediction'),
    'predicted_sod': fields.Float(description='Predicted SOD activity value'),
    'status': fields.String(description='Oxidative stress status (exposed or not exposed)'),
    'threshold': fields.Float(description='Threshold value for classification')
})

# Create a namespace for the prediction endpoint
ns = api.namespace('predict', description='Prediction operations')

# Global variables for model components
model = None
poly = None
scaler = None
sod_threshold = 3.5

def load_model_if_needed():
    global model, poly, scaler
    
    if model is None or poly is None or scaler is None:
        try:
            print("Loading model and preprocessing components...")
            # Import TensorFlow only when needed
            import tensorflow as tf
            from sklearn.preprocessing import PolynomialFeatures
            
            # Load the ML model
            model = tf.keras.models.load_model('model.h5', compile=False)
            print("Model loaded successfully")
            
            # Create polynomial features transformer directly (degree=2 as in the notebook)
            poly = PolynomialFeatures(degree=2)
            print("Polynomial features created successfully")
            
            # Load the scaler from pickle
            scaler = pickle.load(open('scaler.pkl', 'rb'))
            print("Scaler loaded successfully")
            
            print("All components loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading components: {str(e)}")
            return False
    
    return True

def classify_oxidative_stress(radiation, fibrinogen):
    global model, poly, scaler, sod_threshold
    
    if not load_model_if_needed():
        raise Exception("Failed to load model components")
    
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

# Debug route to list all available routes
@app.route('/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': [method for method in rule.methods if method not in ['HEAD', 'OPTIONS']],
            'path': str(rule)
        })
    return jsonify(routes)

# Add a route to serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Add a route to render the HTML UI
@app.route('/')
def index():
    print(f"Rendering index.html from {template_dir}")
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering index.html: {str(e)}")
        return f"Error rendering template: {str(e)}", 500

# Add a route for health check
@app.route('/health')
def health_check():
    return jsonify({"status": "API is running"})

# Add a 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    # Add debugging information
    request_path = request.path
    available_routes = [str(rule) for rule in app.url_map.iter_rules()]
    
    print(f"404 Error: {request_path} not found")
    print(f"Available routes: {available_routes}")
    
    try:
        return render_template('404.html'), 404
    except Exception as exc:
        print(f"Error rendering 404.html: {str(exc)}")
        return f"404 Not Found: {request_path}", 404

# Add a simple home page route for the API information
@api.route('/api')
class ApiInfo(Resource):
    def get(self):
        """Get API information"""
        return {
            'name': 'Oxidative Stress Prediction API',
            'version': '1.0',
            'endpoints': [
                {
                    'path': '/predict',
                    'method': 'POST',
                    'description': 'Predict oxidative stress from radiation and fibrinogen values'
                }
            ]
        }

# Update the prediction endpoint to use Flask-RESTX
@ns.route('')
class PredictionResource(Resource):
    @api.expect(prediction_input)
    @api.response(200, 'Success', prediction_output)
    @api.response(400, 'Validation Error')
    def post(self):
        """Predict oxidative stress based on input values"""
        try:
            data = request.get_json()
            radiation = float(data.get('radiation'))
            fibrinogen = float(data.get('fibrinogen'))
            
            predicted_sod, status = classify_oxidative_stress(radiation, fibrinogen)
            
            return {
                'success': True,
                'predicted_sod': predicted_sod,
                'status': status,
                'threshold': sod_threshold
            }
        except Exception as e:
            print(f"Error in prediction endpoint: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }, 400

# For backwards compatibility, keep the original route
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
    print(f"Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule}")
    
    # Make sure the server runs on all available network interfaces
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 