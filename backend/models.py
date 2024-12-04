from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Optional

# Initialize outside of create_app to avoid circular imports
db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

def init_db(app: Flask) -> None:
    """Initialize the database with the given Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()