"""
Models module - Define os modelos de banco de dados para o jogo
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    """Modelo para administradores do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Define a senha criptografada"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verifica a senha"""
        return check_password_hash(self.password_hash, password)

class Character(db.Model):
    """Modelo para personagens dos jogadores"""
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
    
    def __repr__(self):
        return f'<Character {self.name}>'

class NodeVisit(db.Model):
    """Modelo para registrar visitas a nós da história"""
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(100), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    character = db.relationship('Character', backref=db.backref('node_visits', lazy=True))
    
    def __repr__(self):
        return f'<NodeVisit {self.node_id}>'