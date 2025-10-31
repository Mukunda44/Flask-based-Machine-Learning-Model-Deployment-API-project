# Flask-based ML Model Deployment API

## Overview
This project demonstrates how to deploy a **Machine Learning model** as a **REST API** using Flask. It loads a pre-trained **Logistic Regression model** trained on the **Iris dataset**, validates incoming requests, and returns predictions through clean JSON responses. The project is designed to meet real-world API development standards, including: config-driven model loading, input validation and structured error handling, authentication and CORS, logging and testing with Flask test client, and containerization with Docker.

## 📁 Project Structure
flask-ml-api/
├── app/
│   ├── __init__.py          # Flask app factory (CORS, routes, model load)
│   ├── main.py              # Entry point (python -m app)
│   ├── auth.py              # API key authentication decorator
│   ├── config.py            # Loads settings.yaml config
│   ├── errors.py            # Global error handlers + structured logging
│   ├── model.py             # IrisModel: load + predict methods
│   ├── routes.py            # /health, /predict, /batch_predict endpoints
│   └── schemas.py           # Pydantic validation models
├── config/
│   └── settings.yaml        # Configuration (api_key, model path, CORS, etc.)
├── models/
│   └── iris_logreg.joblib   # Trained scikit-learn Logistic Regression model
├── notebooks/
│   └── train_model.ipynb    # Jupyter notebook to train and save the model
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_predict.py
│   └── test_batch.py
├── requirements.txt
├── Dockerfile
└── README.md

## 🚀 Features Implemented

- [x] Load pre-trained model at startup via configuration  
- [x] `/health` (GET), `/predict` (POST), `/batch_predict` (POST list) endpoints  
- [x] Pydantic-based request validation with clear 400 errors  
- [x] Global exception handling returning JSON error responses  
- [x] API key authentication and secure CORS configuration  
- [x] Structured JSON logging for all requests/responses  
- [x] Flask test client coverage for happy and edge paths  
- [x] Dockerfile for containerized deployment  


## ⚙️ Setup Instructions
### 1. Create and activate environment
conda create -p flaskml python=3.11 -y
conda activate ./flaskml

### 2. Install dependencies
pip install -r requirements.txt

### 3. Train the model
Open and run the notebook:
notebooks/train_model.ipynb

This will generate the file:
models/iris_logreg.joblib

### 4. Run the API
python -m app

You should see:
 * Running on http://127.0.0.1:5000/

## 🔑 API Authentication
All endpoints (except `/health`) require an API key.
The key is defined in `config/settings.yaml`:
api_key: CHANGE_ME

Pass it in the request header:
x-api-key: CHANGE_ME

## 🧩 Endpoints

### 1. GET `/health`
Check app and model status
curl http://localhost:5000/health

Response:
{
  "status": "ok",
  "model": "logreg-iris",
  "model_version": "1.0"
}

### 2. POST `/predict`
Predict class for a single sample
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -H "x-api-key: CHANGE_ME" \
  -d "{\"id\":\"r1\", \"features\":[5.1,3.5,1.4,0.2]}"

Response:
{
  "id": "r1",
  "label": "setosa",
  "probability": 0.9821,
  "model_version": "1.0"
}

### 3. POST `/batch_predict`
Predict for multiple samples
curl -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -H "x-api-key: CHANGE_ME" \
  -d "{\"items\": [
        {\"id\": \"r1\", \"features\": [5.1,3.5,1.4,0.2]},
        {\"id\": \"r2\", \"features\": [6.2,2.8,4.8,1.8]}
      ]}"

Response:
{
  "results": [
    {"id": "r1", "label": "setosa", "probability": 0.9821, "model_version": "1.0"},
    {"id": "r2", "label": "virginica", "probability": 0.8743, "model_version": "1.0"}
  ]
}

## 🧠 Model Details
Dataset: Iris
Algorithm: Logistic Regression (multi-class)
Accuracy: ~96% on test data
Features: sepal length, sepal width, petal length, petal width
Classes: setosa, versicolor, virginica
Saved model: models/iris_logreg.joblib

## 🧪 Run Tests
pytest -q

Expected output:
.....                                                           [100%]
5 passed in 1.3s

## 🐳 Docker Instructions
Build image:
docker build -t flask-ml-api .

Run container:
docker run -p 5000:5000 flask-ml-api

Access the app at:
http://localhost:5000/health

## 📸 Suggested Demo Screenshots
1. `/health` output in terminal
2. `/predict` output (JSON response)
3. `/batch_predict` output
4. `pytest` output showing “5 passed”

Include these in your slides or assignment submission.

## 🧾 Summary
This project demonstrates a complete ML model deployment workflow:
- Model training
- API development and validation
- Authentication and error handling
- Testing and Dockerization

It’s simple, modular, and production-style — suitable for an AI/ML intern assignment or as a base for larger ML services.

Author: Mukunda (AI & Data Science Student)
Tools Used: Python, Flask, scikit-learn, Pydantic, pytest, Docker
Environment: Python 3.11 (conda-based)
