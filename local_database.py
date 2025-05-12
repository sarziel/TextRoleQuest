
from flask_login import UserMixin

class Admin(UserMixin):
    def __init__(self, username, password_hash, created_at=None, last_login=None):
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login
        self.id = username  # usando username como ID



"""
Local Database Module - Handles all database operations using local JSON files
"""

import os
import json
from datetime import datetime

# Define file paths
DATA_DIR = "data"
ADMIN_FILE = os.path.join(DATA_DIR, "admins.json")
CHARACTER_FILE = os.path.join(DATA_DIR, "characters.json")
NODE_VISITS_FILE = os.path.join(DATA_DIR, "node_visits.json")

def ensure_data_dir():
    """Ensure data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_json(file_path, default=None):
    """Load JSON data from file"""
    if not os.path.exists(file_path):
        return default if default is not None else {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    """Save data to JSON file"""
    ensure_data_dir()
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

# Admin operations
def create_admin(admin_data):
    """Create a new admin"""
    admins = load_json(ADMIN_FILE, {})
    username = admin_data['username']
    if username not in admins:
        admins[username] = {
            'password_hash': admin_data['password_hash'],
            'created_at': datetime.utcnow(),
            'last_login': None
        }
        save_json(ADMIN_FILE, admins)
        return True
    return False

def get_admin(username):
    """Get admin by username"""
    admins = load_json(ADMIN_FILE, {})
    return admins.get(username)

def get_admin_by_username(username):
    """Get admin by username"""
    admins = load_json(ADMIN_FILE, {})
    if username in admins:
        admin_data = admins[username]
        return Admin(
            username=username,
            password_hash=admin_data['password_hash'],
            created_at=admin_data.get('created_at'),
            last_login=admin_data.get('last_login')
        )
    return None

def update_admin_login(username):
    """Update admin's last login"""
    admins = load_json(ADMIN_FILE, {})
    if username in admins:
        admins[username]['last_login'] = datetime.utcnow()
        save_json(ADMIN_FILE, admins)

# Character operations
def create_character(data):
    """Create a new character"""
    characters = load_json(CHARACTER_FILE, [])
    char_id = len(characters) + 1
    data['id'] = char_id
    data['created_at'] = datetime.utcnow()
    data['last_played'] = datetime.utcnow()
    characters.append(data)
    save_json(CHARACTER_FILE, characters)
    return char_id

def get_character(char_id):
    """Get character by ID"""
    characters = load_json(CHARACTER_FILE, [])
    for char in characters:
        if char['id'] == char_id:
            return char
    return None

def update_character(char_id, data):
    """Update character data"""
    characters = load_json(CHARACTER_FILE, [])
    for i, char in enumerate(characters):
        if char['id'] == char_id:
            characters[i].update(data)
            characters[i]['last_played'] = datetime.utcnow()
            save_json(CHARACTER_FILE, characters)
            return True
    return False

def get_all_characters():
    """Get all characters"""
    return load_json(CHARACTER_FILE, [])

# Node visit operations
def record_node_visit(node_id, character_id=None):
    """Record a visit to a story node"""
    visits = load_json(NODE_VISITS_FILE, [])
    visit = {
        'id': len(visits) + 1,
        'node_id': node_id,
        'character_id': character_id,
        'visited_at': datetime.utcnow()
    }
    visits.append(visit)
    save_json(NODE_VISITS_FILE, visits)
    return visit['id']

def get_node_visits(limit=5):
    """Get most recent node visits"""
    visits = load_json(NODE_VISITS_FILE, [])
    return sorted(visits, key=lambda x: x['visited_at'], reverse=True)[:limit]

def get_character_visits(character_id):
    """Get all node visits for a character"""
    visits = load_json(NODE_VISITS_FILE, [])
    return [v for v in visits if v['character_id'] == character_id]
