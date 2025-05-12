"""
Player Module - Handles player character creation and attributes
"""

class Player:
    def __init__(self, name, character_class, gender):
        """
        Initialize a new player character
        
        Args:
            name (str): The player's name
            character_class (str): Either "Cientista" or "Arqueólogo"
            gender (str): Either "Homem" or "Mulher"
        """
        self.name = name
        self.character_class = character_class
        self.gender = gender
        
        # Set base attributes based on class and gender
        if character_class == "Cientista":
            self.mental = 10
            self.physical = 6
            self.spiritual = 5
            
            # Women scientists have slightly better mental, men have better physical
            if gender == "Mulher":
                self.mental += 1
                self.physical -= 1
            else:  # Homem
                self.physical += 1
        else:  # Arqueólogo
            self.mental = 8
            self.physical = 7
            self.spiritual = 6
            
            # Women archaeologists have better spiritual, men have better physical
            if gender == "Mulher":
                self.spiritual += 1
            else:  # Homem
                self.physical += 1
        
        # Health and other stats
        self.max_health = 20 + self.physical
        self.current_health = self.max_health
        self.inventory = []
        self.special_abilities = []
        
        # Track important choices and progress
        self.choices_made = {}
        self.orisha_favor = {}  # Track favor with different Òrìṣà
        self.achievements = set()
        
    def modify_attribute(self, attribute, amount):
        """
        Modify a player attribute
        
        Args:
            attribute (str): The attribute to modify (mental, physical, spiritual)
            amount (int): The amount to change the attribute (positive or negative)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if attribute == "mental":
            self.mental += amount
            return True
        elif attribute == "physical":
            self.physical += amount
            return True
        elif attribute == "spiritual":
            self.spiritual += amount
            return True
        else:
            return False
    
    def change_health(self, amount):
        """
        Change the player's current health
        
        Args:
            amount (int): The amount to change health by (positive or negative)
        
        Returns:
            bool: True if alive, False if health <= 0
        """
        self.current_health += amount
        
        # Cap health at max
        if self.current_health > self.max_health:
            self.current_health = self.max_health
            
        # Check if player is dead
        if self.current_health <= 0:
            self.current_health = 0
            return False
            
        return True
    
    def heal(self, amount):
        """
        Heal the player by a certain amount
        
        Args:
            amount (int): The amount to heal
        """
        self.current_health = min(self.current_health + amount, self.max_health)
    
    def add_to_inventory(self, item):
        """
        Add an item to the player's inventory
        
        Args:
            item (str): The item to add
        """
        self.inventory.append(item)
    
    def has_item(self, item):
        """
        Check if the player has a specific item
        
        Args:
            item (str): The item to check for
            
        Returns:
            bool: True if the player has the item, False otherwise
        """
        return item in self.inventory
    
    def add_special_ability(self, ability):
        """
        Add a special ability to the player
        
        Args:
            ability (str): The special ability to add
        """
        if ability not in self.special_abilities:
            self.special_abilities.append(ability)
    
    def has_ability(self, ability):
        """
        Check if the player has a specific ability
        
        Args:
            ability (str): The ability to check for
            
        Returns:
            bool: True if the player has the ability, False otherwise
        """
        return ability in self.special_abilities
    
    def record_choice(self, node_id, choice_index):
        """
        Record a choice the player has made
        
        Args:
            node_id (str): The ID of the node where the choice was made
            choice_index (int): The index of the choice made
        """
        self.choices_made[node_id] = choice_index
    
    def change_orisha_favor(self, orisha, amount):
        """
        Change the player's favor with a particular Òrìṣà
        
        Args:
            orisha (str): The Òrìṣà's name
            amount (int): The amount to change favor by
        """
        self.orisha_favor[orisha] = self.orisha_favor.get(orisha, 0) + amount
    
    def get_orisha_favor(self, orisha):
        """
        Get the player's current favor with a particular Òrìṣà
        
        Args:
            orisha (str): The Òrìṣà's name
            
        Returns:
            int: The current favor value
        """
        return self.orisha_favor.get(orisha, 0)
    
    def add_achievement(self, achievement):
        """
        Add an achievement to the player's achievements
        
        Args:
            achievement (str): The achievement to add
        """
        self.achievements.add(achievement)
    
    def get_achievement_count(self):
        """
        Get the number of achievements the player has earned
        
        Returns:
            int: The number of achievements
        """
        return len(self.achievements)
    
    def get_strength(self, attribute_type="physical"):
        """
        Calculate the player's strength for a particular type of challenge
        
        Args:
            attribute_type (str): The type of attribute to use (mental, physical, spiritual)
            
        Returns:
            int: The calculated strength value
        """
        if attribute_type == "mental":
            return self.mental
        elif attribute_type == "physical":
            return self.physical
        elif attribute_type == "spiritual":
            return self.spiritual
        else:
            return 0
