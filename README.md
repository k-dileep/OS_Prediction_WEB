# Oxidative Stress Prediction Web Application

This web application predicts oxidative stress based on radiation and fibrinogen levels. It consists of a React frontend and a Flask backend with a machine learning model.

## Project Structure

```
OS_Prediction_WEB/
├── backend/             # Flask backend
│   ├── app.py           # Main application file
│   ├── model.h5         # Trained model
│   ├── poly.pkl         # Polynomial features transformer
│   ├── requirements.txt # Python dependencies
│   ├── scaler.pkl       # Scaler for data normalization
│   └── wsgi.py          # WSGI entry point
└── frontend/            # React frontend
```

## Setup and Running

### Backend Setup

1. Ensure you have Python 3.8+ installed (Python 3.11 recommended)
2. Navigate to the backend directory:
   ```
   cd backend
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   If you experience SSL certificate verification issues:
   ```
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```
   
   Alternatively, you can install the key packages individually:
   ```
   pip install flask flask-cors numpy==1.23.5 tensorflow-cpu scikit-learn
   ```

4. Run the Flask backend:
   ```
   python app.py or py -3.11 app.py
   ```
   
   The backend will start on `http://localhost:5000`

### Frontend Setup

1. Ensure you have Node.js and npm installed
2. Navigate to the frontend directory:
   ```
   cd frontend
   ```
3. Install the dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm run dev 
   ```
   
   The frontend will start on `http://localhost:3000`

5. To connect to a deployed backend instead of localhost, set the API URL using one of these methods:

   **Method 1: Create a `.env.local` file in the frontend directory:**
   ```
   NEXT_PUBLIC_API_URL=https://your-deployed-backend-url.com
   ```

   **Method 2: Set environment variable during deployment:**
   
   On platforms like Vercel or Netlify, set the `NEXT_PUBLIC_API_URL` environment variable in your deployment settings.

   **Method 3: Edit the code directly:**
   
   In `app/components/PredictionForm.tsx`, replace the localhost URL with your deployed backend URL:
   ```javascript
   setApiUrl(process.env.NEXT_PUBLIC_API_URL || 'https://your-deployed-backend-url.com');
   ```

## API Endpoints

- **POST** `/predict` - Submit radiation and fibrinogen values for prediction
  - Request body: `{ "radiation": float_value, "fibrinogen": float_value }`
  - Response: 
    ```
    {
      "success": true,
      "predicted_sod": float_value,
      "status": "Exposed to Oxidative Stress" | "Not Exposed to Oxidative Stress",
      "threshold": 3.5
    }
    ```

## Troubleshooting

### Backend Issues

1. **SSL Certificate Errors**:
   - Use the `--trusted-host` flag as mentioned above
   - Or update your certificate store

2. **Incompatible Numpy/TensorFlow Versions**:
   - Use the specific version of numpy (`numpy==1.23.5`) to avoid compatibility issues

3. **Port Already in Use**:
   - Change the port in `app.py` by modifying the line:
     ```python
     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
     ```

### Frontend Issues

1. **Connection to Backend**:
   - Ensure the backend URL in the frontend is correctly set to match your backend
   - Check that CORS is properly configured in the backend

## Production Deployment

For production deployment:

### Backend
- Use Gunicorn as a production server:
  ```
  gunicorn wsgi:app
  ```

### Frontend
- Build the production version:
  ```
  npm run build
  ```
- Serve using a web server like Nginx or deploy to a platform like Vercel or Netlify

## License

This project is proprietary and confidential.