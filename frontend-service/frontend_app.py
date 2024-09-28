import requests
from nicegui import ui
from datetime import datetime

# API Endpoints
API_URL_USER = "http://user-service:5001"
API_URL_TODO = "http://todo-service:5002"

# Global variables to track current user and todos
current_user = None
todos = []

# Define a container for the main content (login screen or todo list)
main_container = ui.column()

# Unified CSS for all screens with standardized button widths
ui.add_head_html("""
    <style>
        .grid-row {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;  /* Three-column layout for all screens */
            align-items: center;  /* Align items in the center for consistency */
            gap: 10px;
            margin-bottom: 16px;
        }

        .card {
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .text-xl {
            font-size: 1.5rem;
            font-weight: bold;
        }

        .input-field {
            width: 100%;  /* Full width input for consistency */
        }

        .timestamp-label {
            width: 150px;  /* Consistent width for the timestamp column */
        }

        .description-label {
            width: 400px;  /* Consistent width for todo description */
        }

        .action-buttons {
            display: flex;
            justify-content: flex-start;
            gap: 10px;  /* Space between action buttons */
        }

        .button {
            padding: 5px 10px;  /* Standardized button size */
            font-size: 0.875rem;
            height: auto;  /* Make the buttons compact */
            flex: 0 1 auto;  /* Dynamic button width */
        }

        .logout-container {
            margin-top: 20px;
        }
    </style>
""")


# Helper Functions

def notify_action(message, color='green'):
    """
    Helper function to display notifications.

    Args:
        message (str): The message to display.
        color (str): The color of the notification.
    """
    ui.notify(message, color=color)


# User Management Functions

def login(username, password):
    """
    Logs in a user with the given username and password.

    Args:
        username (str): The user's username.
        password (str): The user's password.
    """
    global current_user
    response = requests.post(f"{API_URL_USER}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        current_user = response.json()
        notify_action('Login successful!', color='green')
        load_todos()
    else:
        notify_action('Login failed!', color='red')


def logout():
    """
    Logs out the current user and resets the application state.
    """
    global current_user, todos
    current_user = None
    todos = []
    show_login_screen()
    notify_action('Logged out successfully!', color='blue')


def create_account(username, password):
    """
    Creates a new user account.

    Args:
        username (str): The new user's username.
        password (str): The new user's password.
    """
    response = requests.post(f"{API_URL_USER}/create", json={"username": username, "password": password})
    if response.status_code == 201:
        notify_action('Account created successfully!', color='green')
    else:
        notify_action('Failed to create account.', color='red')


# Todo Management Functions

def load_todos():
    """
    Loads the todos for the current user from the API.
    """
    global todos
    if current_user:
        response = requests.get(f"{API_URL_TODO}/todos", params={"user_id": current_user['id']})
        if response.status_code == 200:
            todos = response.json()
            show_todo_screen()
        else:
            notify_action('Failed to load todos!', color='red')


def add_todo(description):
    """
    Adds a new todo for the current user.

    Args:
        description (str): The description of the new todo.
    """
    if current_user:
        response = requests.post(f"{API_URL_TODO}/todos", json={"description": description, "user_id": current_user['id']})
        if response.status_code == 201:
            notify_action('Todo added!', color='green')
            load_todos()
        else:
            notify_action('Failed to add todo!', color='red')


def delete_todo(todo_id):
    """
    Deletes a todo for the current user.

    Args:
        todo_id (int): The ID of the todo to delete.
    """
    response = requests.delete(f"{API_URL_TODO}/todos/{todo_id}")
    if response.status_code == 200:
        notify_action('Todo deleted!', color='green')
        load_todos()
    else:
        notify_action('Failed to delete todo!', color='red')


def edit_todo(todo_id, new_description):
    """
    Edits an existing todo's description.

    Args:
        todo_id (int): The ID of the todo to edit.
        new_description (str): The new description for the todo.
    """
    response = requests.put(f"{API_URL_TODO}/todos/{todo_id}", json={"description": new_description})
    if response.status_code == 200:
        notify_action('Todo edited!', color='green')
        load_todos()
    else:
        notify_action('Failed to edit todo!', color='red')


# UI Rendering Functions

def show_login_screen():
    """
    Displays the login screen where users can log in or create an account.
    """
    main_container.clear()

    with main_container:
        with ui.card().classes('card'):
            ui.label('Login').classes('text-xl mb-4')

            # Username Input
            with ui.element('div').classes('grid-row'):
                ui.label('').classes('timestamp-label')  # Empty first column for alignment
                username = ui.input(label='Username').classes('input-field description-label')
                ui.button('Create Account', on_click=lambda: create_account(username.value, password.value)).classes('button')

            # Password Input
            with ui.element('div').classes('grid-row'):
                ui.label('').classes('timestamp-label')  # Empty first column for alignment
                password = ui.input(label='Password', password=True).classes('input-field description-label')
                ui.button('Login', on_click=lambda: login(username.value, password.value)).classes('button')


def show_todo_screen():
    """
    Displays the todo list screen for the current user.
    """
    main_container.clear()

    username = current_user['username'] if current_user else 'Your'

    with main_container:
        with ui.card().classes('card'):
            ui.label(f"{username}'s Todo List").classes('text-xl mb-4')

            if todos:
                for todo in todos:
                    render_todo(todo)

            # Add New Todo Section
            with ui.element('div').classes('grid-row'):
                ui.label('').classes('timestamp-label')  # Empty column for timestamp
                new_todo_description = ui.input(placeholder='Add a new todo...').classes('input-field description-label')
                with ui.row().classes('action-buttons'):
                    ui.button('ADD', on_click=lambda: add_todo(new_todo_description.value)).classes('button')

        # Logout Button
        with ui.row().classes('logout-container'):
            ui.button('Logout', on_click=logout).classes('button')


def render_todo(todo):
    """
    Renders an individual todo item with Edit and Delete buttons.

    Args:
        todo (dict): The todo item to render.
    """
    todo_id = todo['id']

    with ui.element('div').classes('grid-row'):
        ui.label(todo['created_at']).classes('timestamp-label')
        ui.label(todo['description']).classes('input-field description-label')
        with ui.row().classes('action-buttons'):
            ui.button('Edit', on_click=lambda: start_edit(todo)).classes('button')
            ui.button('Delete', on_click=lambda: delete_todo(todo_id)).classes('button')


def show_edit_screen(todo):
    """
    Displays the edit screen for a specific todo.

    Args:
        todo (dict): The todo item to edit.
    """
    main_container.clear()

    with main_container:
        with ui.card().classes('card'):
            with ui.element('div').classes('grid-row'):
                ui.label(todo['created_at']).classes('timestamp-label')
                new_description = ui.input(value=todo['description']).classes('input-field description-label')
                with ui.row().classes('action-buttons'):
                    ui.button('Save', on_click=lambda: edit_todo(todo['id'], new_description.value)).classes('button')
                    ui.button('Cancel', on_click=lambda: [show_todo_screen(), notify_action('Edit canceled', color='blue')]).classes('button')


def start_edit(todo):
    """
    Starts the editing process for a specific todo.

    Args:
        todo (dict): The todo item to edit.
    """
    show_edit_screen(todo)


# Main Execution
if __name__ in {"__main__", "__mp_main__"}:
    ui.page('/')
    show_login_screen()
    ui.run(port=8080)
