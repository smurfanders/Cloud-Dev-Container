from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy for ORM
db = SQLAlchemy(app)


# Database Model

class Todo(db.Model):
    """
    Todo model representing a task.
    Attributes:
        id (int): The primary key of the todo item.
        description (str): The description of the todo item.
        user_id (int): The ID of the user associated with the todo.
        created_at (datetime): The timestamp when the todo was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation


# Database Initialization

@app.before_first_request
def create_tables():
    """
    Creates all database tables before the first request is handled.
    This ensures the database schema is set up before interacting with the API.
    """
    db.create_all()


# API Endpoints

@app.route('/todos', methods=['GET'])
def get_todos():
    """
    Fetches all todos for a specific user based on user_id query parameter.
    
    Query Parameters:
        user_id (int): The ID of the user for whom to fetch todos.
        
    Returns:
        List of todo objects in JSON format.
    """
    user_id = request.args.get('user_id')
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': todo.id,
        'description': todo.description,
        'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for todo in todos])


@app.route('/todos', methods=['POST'])
def create_todo():
    """
    Creates a new todo item for a specific user.
    
    Request Body (JSON):
        - description (str): The description of the new todo.
        - user_id (int): The ID of the user creating the todo.
    
    Returns:
        The created todo object in JSON format along with HTTP 201 status.
    """
    data = request.json
    new_todo = Todo(description=data['description'], user_id=data['user_id'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({
        'id': new_todo.id,
        'description': new_todo.description,
        'created_at': new_todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 201


@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """
    Updates the description of an existing todo item.
    
    Path Parameters:
        todo_id (int): The ID of the todo item to update.
        
    Request Body (JSON):
        - description (str): The new description for the todo.
    
    Returns:
        The updated todo object in JSON format.
    """
    data = request.json
    todo = Todo.query.get_or_404(todo_id)
    todo.description = data['description']
    db.session.commit()
    return jsonify({
        'id': todo.id,
        'description': todo.description,
        'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    Deletes a todo item based on its ID.
    
    Path Parameters:
        todo_id (int): The ID of the todo item to delete.
    
    Returns:
        An empty response with HTTP 200 status upon successful deletion.
    """
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 200


# Application Entry Point

if __name__ == '__main__':
    """
    The main entry point of the application. Ensures that the 'data' directory 
    exists and starts the Flask application.
    """
    os.makedirs('data', exist_ok=True)
    app.run(host='0.0.0.0', port=5002)
