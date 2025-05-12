"""
Yorùbáland RPG Web Application
A Flask web interface for the text-based RPG
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-for-testing")

@app.route('/')
def index():
    """Main index page"""
    return render_template('index.html')

# Import the game modules so we can use them in our routes
import player
import battle
import save_load
import node_map
import game_data

@app.route('/play')
def play_game():
    """Play the RPG game page"""
    return render_template('play.html')

@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    """Character creation page"""
    if request.method == 'POST':
        name = request.form.get('name')
        character_class = request.form.get('class')
        gender = request.form.get('gender')
        
        if name and character_class and gender:
            # Create new player character
            new_player = player.Player(name, character_class, gender)
            
            # Store in session
            session['player'] = {
                'name': new_player.name,
                'class': new_player.character_class,
                'gender': new_player.gender,
                'mental': new_player.mental,
                'physical': new_player.physical,
                'spiritual': new_player.spiritual,
                'max_health': new_player.max_health,
                'current_health': new_player.current_health,
                'inventory': new_player.inventory,
                'special_abilities': new_player.special_abilities
            }
            session['current_node'] = 'start'
            session['turn_counter'] = 0
            
            return redirect(url_for('game'))
    
    return render_template('create_character.html')

@app.route('/game')
def game():
    """Main game interface"""
    # Check if player exists in session
    if 'player' not in session:
        return redirect(url_for('create_character'))
    
    # Get current node
    current_node_id = session.get('current_node', 'start')
    node_data = node_map.get_node(current_node_id)
    
    return render_template('game.html', node=node_data, player=session['player'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)