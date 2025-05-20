from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlalchemy

# Fix for SQLAlchemy 2.0 compatibility
if not hasattr(sqlalchemy, '__all__'):
    sqlalchemy.__all__ = []  # Add empty __all__ attribute if it doesn't exist

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User account model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Store user text generation history
    generations = db.relationship('TextGeneration', backref='user', lazy=True)
    
    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class TextGeneration(db.Model):
    """Model for storing text generation history"""
    __tablename__ = 'text_generations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    generated_text = db.Column(db.Text, nullable=False)
    model_type = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TextGeneration {self.id}>'