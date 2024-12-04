from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

# Local imports
from models import db, User, init_db

# Configuration and app setup
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
    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "User Management App"}
    )
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # Routes
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([
            {
                'id': user.id, 
                'username': user.username, 
                'email': user.email
            } for user in users
        ]), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        
        # Validate input
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and email are required'}), 400

        # Check for existing user
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        # Create new user
        new_user = User(
            username=data['username'], 
            email=data['email']
        )
        
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

    return app

# Main entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)