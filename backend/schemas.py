from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import User

class UserSchema(SQLAlchemyAutoSchema):
    """Marshmallow schema for User model serialization and deserialization"""
    class Meta:
        model = User
        load_instance = True  # Create model instances directly from validated data
        include_relationships = True
        
    # Optional: Add custom validation
    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError("Username must be at least 3 characters long")
        return value