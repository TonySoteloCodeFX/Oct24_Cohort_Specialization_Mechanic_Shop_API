from jose import jwt 
import jose
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import os


SECRET_KEY = os.environ.get('SECRET_KEY') or "super secret secrets"

def encode_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id) 
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({"error": "Missing Token"})
        
        try:
            data  = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            print(data)
            request.mechanic_id = int(data['sub'])

        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'error': "Token expired"})
        except jose.exceptions.JWTError:
            return jsonify({"error": "Invalid Token"})
        
        return f(*args, **kwargs)
    return decorated

