
"""
Database Module - Handles all database operations for the game
"""

from datetime import datetime
from database_config import db, Admin, Character, NodeVisit

def init_db(app):
    """Initialize database with app context"""
    with app.app_context():
        db.create_all()

def create_admin(username, password):
    """Create a new admin user"""
    admin = Admin(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

def get_admin(username):
    """Get admin by username"""
    return Admin.query.filter_by(username=username).first()

def create_character(name, character_class, gender):
    """Create a new character"""
    character = Character(
        name=name,
        character_class=character_class,
        gender=gender
    )
    db.session.add(character)
    db.session.commit()
    return character

def get_character(character_id):
    """Get character by ID"""
    return Character.query.get(character_id)

def update_character(character):
    """Update character data"""
    db.session.commit()

def record_node_visit(node_id, character_id=None):
    """Record a visit to a story node"""
    visit = NodeVisit(
        node_id=node_id,
        character_id=character_id
    )
    db.session.add(visit)
    db.session.commit()

def get_node_visits(limit=5):
    """Get most recent node visits"""
    return NodeVisit.query.order_by(NodeVisit.visited_at.desc()).limit(limit).all()

def get_character_visits(character_id):
    """Get all node visits for a character"""
    return NodeVisit.query.filter_by(character_id=character_id).order_by(NodeVisit.visited_at.desc()).all()

def get_all_characters():
    """Get all characters"""
    return Character.query.order_by(Character.last_played.desc()).all()
