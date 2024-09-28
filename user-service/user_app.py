from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database path for user management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy for ORM
db = SQLAlchemy(app)


# Database Model

class User(db.Model):
    """
    User model representing a user in the system.
    
    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user, must be unique.
        password (str): The password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# Database Initialization

@app.before_first_request
def create_tables():
    """
    Creates the database tables before handling the first request.
    Ensures the database schema is created and ready for use.
    """
    db.create_all()


# API Endpoints

@app.route('/create', methods=['POST'])
def create_user():
    """
    Creates a new user in the system.
    
    Request Body (JSON):
        - username (str): The new user's username.
        - password (str): The new user's password.
    
    Returns:
        JSON object containing the new user's ID and username, or an error message
        if the username already exists.
    """
    data = request.json
    # Check if the user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'User already exists'}), 409
    
    # Create and save the new user
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    # Return the created user with status 201
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user based on username and password.
    
    Request Body (JSON):
        - username (str): The user's username.
        - password (str): The user's password.
    
    Returns:
        JSON object containing the user's ID and username if authentication is successful,
        or HTTP 401 status if the credentials are incorrect.
    """
    data = request.json
    # Attempt to find the user with matching credentials
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({'id': user.id, 'username': user.username}), 200
    else:
        return '', 401


# Application Entry Point

if __name__ == '__main__':
    """
    The main entry point of the application. Ensures that the 'data' directory
    exists and starts the Flask application.
    """
    # Ensure the data folder exists for SQLite database
    os.makedirs('data', exist_ok=True)
    
    # Start the Flask app on port 5001, accessible on all network interfaces
    app.run(host='0.0.0.0', port=5001)
