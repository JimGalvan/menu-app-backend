# Menu Management System

This project is a Django-based application for managing menus, categories, and menu items. It includes user authentication and provides RESTful APIs for interacting with the data.

## Features

- User registration and authentication
- CRUD operations for menus, categories, and menu items
- Search and ordering functionality
- Pagination support

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/menu-management-system.git
    cd menu-management-system
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## API Endpoints

### Authentication

- **Register**: `POST /register/`
- **Login**: `POST /login/`

### Users

- **List Users**: `GET /users/`
- **Retrieve User**: `GET /users/{id}/`
- **Create User**: `POST /users/`
- **Update User**: `PUT /users/{id}/`
- **Delete User**: `DELETE /users/{id}/`
- **User Menus**: `GET /users/{id}/menus/`

### Menus

- **List Menus**: `GET /menus/`
- **Retrieve Menu**: `GET /menus/{id}/`
- **Create Menu**: `POST /menus/`
- **Update Menu**: `PUT /menus/{id}/`
- **Delete Menu**: `DELETE /menus/{id}/`
- **Menu Items**: `GET /menus/{id}/menu_items/`
- **Menu Categories**: `GET /menus/{id}/categories/`

### Categories

- **List Categories**: `GET /categories/`
- **Retrieve Category**: `GET /categories/{id}/`
- **Create Category**: `POST /categories/`
- **Update Category**: `PUT /categories/{id}/`
- **Delete Category**: `DELETE /categories/{id}/`
- **Category Menu Items**: `GET /categories/{id}/menu_items/`

### Menu Items

- **List Menu Items**: `GET /menu_items/`
- **Retrieve Menu Item**: `GET /menu_items/{id}/`
- **Create Menu Item**: `POST /menu_items/`
- **Update Menu Item**: `PUT /menu_items/{id}/`
- **Delete Menu Item**: `DELETE /menu_items/{id}/`

## Pagination

All list endpoints support pagination. Use the `page` query parameter to navigate through pages.

## Search and Ordering

- **Search**: Use the `search` query parameter to search by name or description.
- **Ordering**: Use the `ordering` query parameter to order results by specific fields.
