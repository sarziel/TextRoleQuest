
from flask_login import UserMixin

class Admin(UserMixin):
    def __init__(self, username, password_hash, created_at=None, last_login=None):
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login
        self.id = username
        self._is_authenticated = True
        self._is_active = True
        self._is_anonymous = False

    def get_id(self):
        return str(self.id)
        
    @property
    def is_authenticated(self):
        return self._is_authenticated
        
    @property
    def is_active(self):
        return True



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
    for file_name in [ADMIN_FILE, CHARACTER_FILE, NODE_VISITS_FILE]:
        if not os.path.exists(file_name):
            save_json(file_name, {} if file_name == ADMIN_FILE else [])

def load_json(file_path, default=None):
    """Load JSON data from file"""
    try:
        if not os.path.exists(file_path):
            return default if default is not None else {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error reading {file_path}, returning default value")
        return default if default is not None else {}

def save_json(file_path, data):
    """Save data to JSON file"""
    ensure_data_dir()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False

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
        admins[username]['last_login'] = datetime.utcnow().isoformat()
        save_json(ADMIN_FILE, admins)
        return True
    return False

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

def count_characters():
    """Count total number of characters"""
    characters = load_json(CHARACTER_FILE, [])
    return len(characters)

def count_node_visits():
    """Count total number of node visits"""
    visits = load_json(NODE_VISITS_FILE, [])
    return len(visits)

def count_node_visits_for_node(node_id):
    """Count visits for a specific node"""
    visits = load_json(NODE_VISITS_FILE, [])
    return len([v for v in visits if v['node_id'] == node_id])

def get_top_visited_nodes(limit=5):
    """Get most visited nodes"""
    visits = load_json(NODE_VISITS_FILE, [])
    node_counts = {}
    for visit in visits:
        node_id = visit['node_id']
        node_counts[node_id] = node_counts.get(node_id, 0) + 1
    
    sorted_nodes = sorted(node_counts.items(), key=lambda x: x[1], reverse=True)
    return [{'node_id': node_id, 'visit_count': count} for node_id, count in sorted_nodes[:limit]]

def get_recent_characters(limit=5):
    """Get most recently created characters"""
    characters = load_json(CHARACTER_FILE, [])
    sorted_chars = sorted(characters, key=lambda x: x.get('created_at', ''), reverse=True)
    return sorted_chars[:limit]

def get_characters_that_visited_node(node_id):
    """Get characters that visited a specific node"""
    visits = load_json(NODE_VISITS_FILE, [])
    char_ids = set(v['character_id'] for v in visits if v['node_id'] == node_id and v['character_id'] is not None)
    characters = load_json(CHARACTER_FILE, [])
    return [c for c in characters if c['id'] in char_ids]

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
