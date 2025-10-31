# app/auth.py
# API key authentication for our Flask API

from flask import request,jsonify,current_app
from functools import wraps

def require_api_key(f):
    """
    Decorator to enforce API key authentication.
    Checks the 'x-api-key' header against the configured key in settings.yaml.
    """

    @wraps(f)
    def decorated(*args, **kwags):
        #Read key from request header
        provided_key= request.headers.get("x-api-key")

        #Get the expected key from the app config
        expected_key = current_app.config["APP_CONFIG"].api_key

        #If key missing or invalid, block the request
        if not provided_key or provided_key!=expected_key:
            response=jsonify({
                "error": "Unauthorized",
                "code": 401,
                "details": "Missing or invalid API key"
            })
            response.status_code = 401
            return response
        
        #Otherwise, call the original function
        return f(*args,**kwags)
    return decorated
