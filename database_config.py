
"""
Database Configuration Module
Handles all database setup and configuration
"""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db_config(app):
    """Initialize database configuration"""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Modify URL for PostgreSQL
        database_url = database_url.replace('postgres://', 'postgresql://')
        if '?' not in database_url:
            database_url += '?sslmode=prefer'

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,    # check connection before using
        "pool_recycle": 280,      # recycle connections every ~4.5 minutes
        "pool_timeout": 10,       # timeout for getting a connection
        "max_overflow": 15        # extra connections beyond pool size
    }

    # Initialize database with app
    db.init_app(app)

class Admin(UserMixin, db.Model):
    """Admin model for system administrators"""
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Set encrypted password"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)

class Character(db.Model):
    """Model for player characters"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    character_class = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    mental = db.Column(db.Integer, default=10)
    physical = db.Column(db.Integer, default=10)
    spiritual = db.Column(db.Integer, default=10)
    max_health = db.Column(db.Integer, default=100)
    current_health = db.Column(db.Integer, default=100)
    inventory = db.Column(db.Text)  # JSON string
    special_abilities = db.Column(db.Text)  # JSON string
    current_node = db.Column(db.String(100), default='start')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_played = db.Column(db.DateTime, default=datetime.utcnow)

class NodeVisit(db.Model):
    """Model for recording story node visits"""
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(100), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    character = db.relationship('Character', backref=db.backref('node_visits', lazy=True))
