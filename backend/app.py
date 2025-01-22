from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os

from models import db, User, init_db

def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    init_db(app)

    # Swagger Configuration
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "User Management API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Serve swagger.json
    @app.route('/static/swagger.json')
    def send_swagger_json():
        return send_from_directory('static', 'swagger.json')

    @app.route('/users', methods=['GET'])
    def get_users():
        """
        Get all users
        ---
        responses:
          200:
            description: List of users
        """
        users = User.query.all()
        return jsonify([{
            'id': user.id, 
            'username': user.username, 
            'email': user.email
        } for user in users]), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        """
        Create a new user
        ---
        parameters:
          - in: body
            name: body
            schema:
              id: UserInput
              required:
                - username
                - email
              properties:
                username:
                  type: string
                  description: The user's username
                email:
                  type: string
                  description: The user's email
        responses:
          201:
            description: User created successfully
          400:
            description: Invalid input
        """
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and email are required'}), 400

        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        new_user = User(username=data['username'], email=data['email'])
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                'id': new_user.id, 
                'username': new_user.username, 
                'email': new_user.email
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        """
        Update an existing user
        ---
        parameters:
          - name: user_id
            in: path
            type: integer
            required: true
            description: ID of the user to update
          - in: body
            name: body
            schema:
              id: UserInput
              properties:
                username:
                  type: string
                email:
                  type: string
        responses:
          200:
            description: User updated successfully
          404:
            description: User not found
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            if 'username' in data:
                existing_user = User.query.filter(
                    User.username == data['username'],
                    User.id != user_id
                ).first()
                if existing_user:
                    return jsonify({'error': 'Username already exists'}), 400
                user.username = data['username']

            if 'email' in data:
                existing_user = User.query.filter(
                    User.email == data['email'],
                    User.id != user_id
                ).first()
                if existing_user:
                    return jsonify({'error': 'Email already exists'}), 400
                user.email = data['email']

            db.session.commit()
            return jsonify({
                'id': user.id, 
                'username': user.username, 
                'email': user.email
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """
        Delete a user
        ---
        parameters:
          - name: user_id
            in: path
            type: integer
            required: true
            description: ID of the user to delete
        responses:
          200:
            description: User deleted successfully
          404:
            description: User not found
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)