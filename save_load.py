"""
Save/Load Module - Handles saving and loading game state
"""

import os
import json
import time
from player import Player

# Define the save file path
SAVE_FILE = "yorubaland_save.json"

def save_game(player, current_node, turn_counter):
    """
    Save the current game state to a file
    
    Args:
        player: Player object
        current_node: Current story node ID
        turn_counter: Current turn counter
        
    Returns:
        bool: True if save was successful, False otherwise
    """
    try:
        # Create a dictionary with all important game state
        save_data = {
            "player": {
                "name": player["name"],
                "class": player["class"],
                "gender": player["gender"],
                "mental": player["mental"],
                "physical": player["physical"],
                "spiritual": player["spiritual"],
                "max_health": player["max_health"],
                "current_health": player["current_health"],
                "inventory": player["inventory"],
                "special_abilities": player["special_abilities"]
            },
            "game_state": {
                "current_node": current_node,
                "turn_counter": turn_counter,
                "timestamp": int(time.time())
            }
        }
        
        # Write to file
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f, indent=2)
            
        return True
    
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game():
    """
    Load a game from the save file
    
    Returns:
        dict: Dictionary containing player data and game state
    """
    try:
        # Check if save file exists
        if not os.path.exists(SAVE_FILE):
            return None
        
        # Read save file
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
        
        # Extract player data and game state
        player_data = save_data["player"]
        game_state = save_data["game_state"]
        
        # Return the data as a dictionary
        return {
            "player": {
                "name": player_data["name"],
                "class": player_data["class"],
                "gender": player_data["gender"],
                "mental": player_data["mental"],
                "physical": player_data["physical"],
                "spiritual": player_data["spiritual"],
                "max_health": player_data["max_health"],
                "current_health": player_data["current_health"],
                "inventory": player_data["inventory"],
                "special_abilities": player_data["special_abilities"]
            },
            "current_node": game_state["current_node"],
            "turn_counter": game_state["turn_counter"]
        }
    
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

def save_exists():
    """
    Check if a save file exists
    
    Returns:
        bool: True if a save file exists, False otherwise
    """
    return os.path.exists(SAVE_FILE)

def get_save_info():
    """
    Get information about the existing save
    
    Returns:
        dict: Save information or None if no save exists
    """
    if not save_exists():
        return None
    
    try:
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
        
        player_data = save_data["player"]
        game_state = save_data["game_state"]
        
        # Format timestamp
        timestamp = game_state["timestamp"]
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        
        return {
            "player_name": player_data["name"],
            "player_class": player_data["class"],
            "player_gender": player_data["gender"],
            "save_time": time_str,
            "turn_counter": game_state["turn_counter"]
        }
    
    except Exception:
        return None

def delete_save():
    """
    Delete the save file
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        return True
    except Exception:
        return False
