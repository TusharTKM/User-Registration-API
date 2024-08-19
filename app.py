#=================================================================
# Page name : app.py
# Author : Tushar Mishra
# Date Created : 19 Aug 2024
# Purpose : REST API for 
            # 1. User Registration
            # 2. Login and JWT token generation
            # 3. Access private resource through JWT verification
            # 4. Revoking JWT token from backend
            # 5. Renewing token by user before it expires
#=================================================================

# ------ Dependencies ---------
from flask import Flask, request, jsonify
import json
import re
import os
import jwt
import datetime

app = Flask(__name__)

# Secret key for encoding/decoding JWT tokens
SECRET_KEY = 'your_secret_key'

# Define the path for the users file
directory_path = 'data'
file_path = os.path.join(directory_path, 'users.json')

# Ensure the directory exists
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

#-------------------------------------
#------- User Defined Function -------
#-------------------------------------

# ------- UDF for email validation ---------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# -------- UDF for loading all the registered users ------------
def load_users():
    if os.path.exists('data/users.json'):
        with open('data/users.json', 'r') as file:
            return json.load(file)
    else:
        return {}

# -------- UDF for saving user details ------------
def save_users(users):
    with open('data/users.json', 'w') as file:
        json.dump(users, file, indent=4)

# -------- UDF for generating token based on email ----------
def create_jwt(email):
    # Set token expiry time
    expiry = datetime.datetime.now() + datetime.timedelta(hours=1)  
    payload = {
        'email': email,
        'exp': expiry
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token, expiry

# --------- UDF for checking valid token and expiry ----------
def is_token_valid(email, token):

    # get all the user details
    users = load_users()
    user = users.get(email)

    # if email does not match return false
    if user is None:
        return False
    
    # get the stored token and expiry time
    stored_token = user.get('Token')
    token_expiry = user.get('TokenExpiry')

    # if tokens do not match return false  
    if stored_token != token:
        return False
    
    try:
        # Decode the token to check validity
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        token_expiry_datetime = datetime.datetime.fromisoformat(token_expiry)
        return datetime.datetime.now() <= token_expiry_datetime

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

#--------------------------------
#------- REST API Routes -------
#--------------------------------

# -------- Default Route --------
@app.route('/')
def home():
    return ({
        "message" : "Welcome to the User-Registration REST API"
    })

# -------- Route for New User Registration --------
@app.route('/register', methods=['POST'])
def register():
    
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'message': 'Invalid JSON data'
        }), 400

    if not data:
        return jsonify({
            'message': 'No JSON data received'
        }), 400

    # Get input fields
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validate input fields
    if not name or not email or not password:
        return jsonify({
            'message': 'Name, email, and password are required'
        }), 400

    # Validate email address
    if not is_valid_email(email):
        return jsonify({
            'message': 'Invalid email address'
        }), 400
    
    # Load existing users
    users = load_users()

    # Check for already existing users
    if email in users:
        return jsonify({
            'message': 'Email Id is already registered'
        }), 400
    
    # Add new user
    users[email] = {'name': name, 'email' : email, 'password': password}

    # Save users to file
    with open('data/users.json', 'w') as file:
        json.dump(users, file, indent=4)

    return jsonify({
        'message': 'User registered successfully',
        "users" : users
    }), 201

# -------- Route for User Login --------
@app.route('/login', methods=['POST'])
def login():

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'message': 'Invalid JSON data'
        }), 400

    if not data:
        return jsonify({
            'message': 'No JSON data received'
        }), 400
    
    # get the email and password from request
    email = data.get('email')
    password = data.get('password')

    # validate the required field
    if not email or not password:
        return jsonify({
            'message': 'Email and password are required'
        }), 400

    # Validate the email address
    if not is_valid_email(email):
        return jsonify({
            'message': 'Invalid email address'
        }), 400
    
    # Load users
    users = load_users()

    # Check if email exists and password matches
    user = users.get(email)
    if not user or user.get('password') != password:
        return jsonify({
            'message': 'Invalid email or password'
        }), 401
    
    # Create JWT token
    token, expiry = create_jwt(email)

    # Update user details with new token and expiry time
    user['Token'] = token
    user['TokenExpiry'] = expiry.isoformat()  # Store expiry time as ISO 8601 string
    save_users(users)

    return jsonify({
        'message' : 'Login is successful',
        'token': token,
        'expiry_time': expiry.isoformat()
    }), 200

# --------- Route for private section ------------
@app.route('/private-resource', methods=['POST'])
def private_resource():

    # Validate the request data
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'message': 'Invalid JSON data'
        }), 400

    if not data:
        return jsonify({
            'message': 'No JSON data received'
        }), 400
    
    # extract the email and token from request 
    email = data.get('email')
    token = data.get('token')

    # Validate the email and token
    if not email or not token:
        return jsonify({
            'message': 'Email and token are required'
        }), 400

    # Check if the token is active
    if not is_token_valid(email, token):
        return jsonify({
            'message': 'Invalid or expired token'
        }), 403
    
    return jsonify({
        'message': 'Access granted to private resource'
        }), 200

# ---------- Route for revoking user token ---------
@app.route('/revoke-token', methods=['POST'])
def revoke_token():

    # Validate the request data
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'message': 'Invalid JSON data'
        }), 400

    if not data:
        return jsonify({
            'message': 'No JSON data received'
        }), 400
    
    # extract the email from request 
    email = data.get('email')

    # validate for email
    if not email:
        return jsonify({
            'message': 'Email is required'
        }), 400

    # Load users
    users = load_users()

    if email not in users:
        return jsonify({
            'message': 'User not found'
        }), 404
    
    # Revoke the token
    user = users[email]
    user['Token'] = ''  # Clear the token
    user['TokenExpiry'] = ''  # Clear the token expiry time

    # Save updated users
    save_users(users)

    return jsonify({
        'message': 'User Token has been revoked'
    }), 200

# ----------- Route for token renewal by client before it expires -----------
@app.route('/renew-token', methods=['POST'])
def renew_token():

    # Validate the request data
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'message': 'Invalid JSON data'
        }), 400

    if not data:
        return jsonify({
            'message': 'No JSON data received'
        }), 400
    
    # extract the email from request 
    email = data.get('email')

    # validate for email
    if not email:
        return jsonify({
            'message': 'Email is required'
        }), 400
    
    # Load users
    users = load_users()

    if email not in users:
        return jsonify({
            'message': 'User not found'
        }), 404

    # get user's current token
    user = users[email]
    current_token = user.get('Token')
    current_token_expiry = user.get('TokenExpiry')
    
    if not current_token or not current_token_expiry:
        return jsonify({
            'message': 'No token is found for this user'
        }), 400

    # Check if the token is active
    if not is_token_valid(email, current_token):
        return jsonify({
            'message': 'Token has expired. Can not renew.'
        }), 403
    
    # Increase the token expiry
    current_expiry_time = datetime.datetime.fromisoformat(current_token_expiry)
    new_expiry_time = current_expiry_time + datetime.timedelta(hours=1)

    # Update user data with new token and expiry        
    user['TokenExpiry'] = new_expiry_time.isoformat()
    save_users(users)

    return jsonify({
        'message': 'Token has been renewed successfully',  
        'Valid uptp': new_expiry_time.isoformat()
    }), 200
        

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)