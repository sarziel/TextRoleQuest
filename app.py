"""
Yorùbáland RPG Web Application
A Flask web interface for the text-based RPG
"""

import os
import random
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import local_database as db

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-for-testing")

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_admin_by_username(user_id)

# Função para criar usuário admin
def create_admin_user():
    """Cria o usuário administrador se não existir"""
    try:
        # Verificar se o usuário admin já existe
        admin_user = db.get_admin_by_username('admin')
        if not admin_user:
            # Criar novo usuário admin
            admin_user = {'username': 'admin', 'password_hash': generate_password_hash('admin123')}
            db.create_admin(admin_user)
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe.")
    except Exception as e:
        print(f"Erro ao criar usuário admin: {e}")

# Registrar comando para criar o usuário admin
@app.cli.command('create-admin')
def create_admin_command():
    """Comando para criar usuário admin"""
    create_admin_user()

# Em versões mais recentes do Flask, before_first_request foi removido
# Vamos usar uma função que será chamada na primeira requisição
try:
    with app.app_context():
        # Tentar criar o banco de dados e o usuário admin na inicialização
        create_admin_user()
except Exception as e:
    print(f"Erro na inicialização do banco de dados: {e}")
    # Não vamos interromper a aplicação por causa disso

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username != 'admin':
            flash('Acesso negado. Você precisa fazer login como administrador.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main index page"""
    try:
        return render_template('index.html')
    except Exception as e:
        # Log error but still return the page to avoid breaking navigation
        print(f"Erro na página inicial: {e}")
        return render_template('index.html')

@app.route('/admin-info')
def admin_info():
    """Informações de diagnóstico do admin"""
    # Verificar estado do banco de dados
    db_status = "Conectado"
    admin_exists = "Não encontrado"
    table_info = []

    try:
        # Verificar se o usuário admin existe
        admin = db.get_admin_by_username('admin')
        if admin:
            admin_exists = "Encontrado (ID: {})".format(admin['id'])
        else:
            admin_exists = "Não encontrado"


        table_info = ["Admins", "Characters", "NodeVisits"]
    except Exception as e:
        db_status = "Erro: {}".format(str(e))

    # Obter informações dos nós
    node_count = node_map.count_nodes()
    node_examples = list(node_map.nodes.keys())[:5]  # Primeiros 5 nós

    return render_template(
        'admin_info.html',
        db_status=db_status,
        admin_exists=admin_exists,
        table_info=table_info,
        node_count=node_count,
        node_examples=node_examples
    )

# Import the game modules so we can use them in our routes
import player
import battle
import save_load
import node_map
import game_data

@app.route('/play')
def play_game():
    """Play the RPG game page"""
    try:
        return render_template('play.html')
    except Exception as e:
        print(f"Erro na página de jogo: {e}")
        # Falhar de maneira resiliente, tentar renderizar uma versão simplificada
        return render_template('index.html')

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

    return render_template('game.html', node=node_data, node_id=current_node_id, player=session['player'])

@app.route('/make_choice', methods=['POST'])
def make_choice():
    """Process a player's choice"""
    if 'player' not in session:
        return redirect(url_for('create_character'))

    node_id = request.form.get('node_id')
    choice_index = int(request.form.get('choice_index', 0))

    # Get the node and choice
    node = node_map.get_node(node_id)
    if 'choices' in node and len(node['choices']) > choice_index:
        choice = node['choices'][choice_index]

        # Check if this is a test/challenge
        if 'test' in choice:
            test_type = choice['test']
            difficulty = choice.get('difficulty', 10)

            # Get player attribute
            player_attr = session['player'].get(test_type, 0)

            # Roll dice (1-20)
            roll = random.randint(1, 20)
            total = roll + player_attr

            # Determine success or failure
            if total >= difficulty:
                # Success
                session['current_node'] = choice['success_node']
                flash(f'Teste de {test_type} bem sucedido! Rolagem: {roll}, Total: {total}', 'success')
            else:
                # Failure
                session['current_node'] = choice['failure_node']
                flash(f'Teste de {test_type} falhou! Rolagem: {roll}, Total: {total}', 'danger')

        # Check if this is a battle
        elif 'battle' in choice:
            enemy = choice['battle']
            session['battle_enemy'] = enemy
            session['victory_node'] = choice.get('victory_node')
            session['defeat_node'] = choice.get('defeat_node')

            # Redirect to battle
            return redirect(url_for('battle_start'))

        # Direct navigation
        else:
            session['current_node'] = choice['next_node']

    return redirect(url_for('game'))

@app.route('/continue', methods=['POST'])
def continue_story():
    """Continue to the next node when there are no choices"""
    if 'player' not in session:
        return redirect(url_for('create_character'))

    node_id = request.form.get('node_id')
    node = node_map.get_node(node_id)

    if 'next_node' in node:
        session['current_node'] = node['next_node']

    return redirect(url_for('game'))

@app.route('/command', methods=['POST'])
def process_command():
    """Process special commands entered by the player"""
    if 'player' not in session:
        return redirect(url_for('create_character'))

    command = request.form.get('command', '').strip().lower()

    if command == 'status':
        flash('Seus atributos e status são mostrados no painel lateral.', 'info')
    elif command in ['ajuda', 'help']:
        help_text = """
        Comandos disponíveis:
        - status: Ver seus atributos e status
        - ajuda ou help: Mostrar esta ajuda
        - salvar: Salvar manualmente seu progresso

        Durante batalhas:
        - atacar: Usar seu atributo físico para atacar
        - defender: Adotar postura defensiva
        - espirito: Usar seu atributo espiritual
        """
        flash(help_text, 'info')
    elif command in ['salvar', 'save']:
        # We'll implement this in the save_game route
        return redirect(url_for('save_game'))
    else:
        flash(f'Comando desconhecido: {command}', 'warning')

    return redirect(url_for('game'))

@app.route('/save_game', methods=['GET', 'POST'])
def save_game():
    """Save the current game state"""
    if 'player' not in session:
        return redirect(url_for('create_character'))

    # Get current turn counter
    turn_counter = session.get('turn_counter', 0)

    # Save game using the save_load module
    success = save_load.save_game(session['player'], session['current_node'], turn_counter)

    if success:
        flash('Jogo salvo com sucesso!', 'success')
    else:
        flash('Erro ao salvar o jogo.', 'danger')

    return redirect(url_for('game'))

@app.route('/load_game')
def load_game():
    """Load a saved game"""
    # Check if save exists
    if not save_load.save_exists():
        flash('Nenhum jogo salvo encontrado.', 'warning')
        return redirect(url_for('play_game'))

    # Load game
    loaded_game = save_load.load_game()
    if loaded_game:
        # Store in session
        session['player'] = loaded_game['player']
        session['current_node'] = loaded_game['current_node']
        session['turn_counter'] = loaded_game['turn_counter']

        flash('Jogo carregado com sucesso!', 'success')
        return redirect(url_for('game'))
    else:
        flash('Erro ao carregar o jogo.', 'danger')
        return redirect(url_for('play_game'))

@app.route('/battle_start')
def battle_start():
    """Start a battle with an enemy"""
    if 'player' not in session or 'battle_enemy' not in session:
        return redirect(url_for('game'))

    # Get enemy data
    enemy_id = session['battle_enemy']
    enemy_data = battle.get_enemy_data(enemy_id)

    if not enemy_data:
        flash('Erro ao iniciar batalha: inimigo não encontrado.', 'danger')
        return redirect(url_for('game'))

    # Initialize battle session
    session['enemy'] = {
        'id': enemy_id,
        'name': enemy_data['name'],
        'description': enemy_data['description'],
        'max_health': enemy_data['health'],
        'current_health': enemy_data['health'],
        'attack': enemy_data['attack'],
        'defense': enemy_data['defense'],
        'spirit_resistance': enemy_data.get('spirit_resistance', 10)
    }

    session['battle_log'] = [f"Você encontrou um {enemy_data['name']}!"]

    return render_template('battle.html', 
                          player=session['player'],
                          enemy=session['enemy'],
                          battle_log=session['battle_log'])

@app.route('/battle_action', methods=['POST'])
def battle_action():
    """Process a battle action"""
    if 'player' not in session or 'enemy' not in session:
        return redirect(url_for('game'))

    action = request.form.get('action')

    # Get player and enemy data
    player_data = session['player']
    enemy_data = session['enemy']

    # Initialize battle variables
    dice_roll = random.randint(1, 20)
    battle_message = ""
    battle_success = False
    player_damage_taken = 0
    enemy_damage_taken = 0

    # Process player action
    if action == 'attack':
        # Physical attack
        attack_total = dice_roll + player_data['physical']

        if dice_roll == 20:  # Critical hit
            enemy_damage_taken = (player_data['physical'] * 2) + random.randint(3, 6)
            battle_message = f"Acerto crítico! Você causou {enemy_damage_taken} pontos de dano!"
            battle_success = True
        elif dice_roll == 1:  # Critical miss
            enemy_damage_taken = 0
            battle_message = "Erro crítico! Você tropeça e erra o ataque!"
            battle_success = False
        elif attack_total >= enemy_data['defense'] + 5:  # Strong hit
            enemy_damage_taken = player_data['physical'] + random.randint(2, 5)
            battle_message = f"Ótimo golpe! Você causou {enemy_damage_taken} pontos de dano!"
            battle_success = True
        elif attack_total >= enemy_data['defense']:  # Normal hit
            enemy_damage_taken = max(1, player_data['physical'] + random.randint(0, 3) - enemy_data['defense'] // 2)
            battle_message = f"Você acerta o golpe e causa {enemy_damage_taken} pontos de dano."
            battle_success = True
        else:  # Miss
            enemy_damage_taken = 0
            battle_message = "Seu ataque foi bloqueado ou desviado."
            battle_success = False

    elif action == 'defend':
        # Defensive stance
        session['defending'] = True
        battle_message = "Você assume uma postura defensiva!"
        battle_success = True

    elif action == 'spirit':
        # Spiritual attack/action
        spirit_total = dice_roll + player_data['spiritual']

        if dice_roll == 20:  # Critical success
            if random.random() < 0.5:  # 50% chance for damage
                enemy_damage_taken = player_data['spiritual'] * 2 + random.randint(2, 8)
                battle_message = f"Os Òrìṣà atendem seu chamado com poder imenso! Você causa {enemy_damage_taken} pontos de dano espiritual!"
                battle_success = True
            else:  # 50% chance for healing
                heal_amount = player_data['spiritual'] + random.randint(3, 8)
                player_data['current_health'] = min(player_data['current_health'] + heal_amount, player_data['max_health'])
                battle_message = f"Os Òrìṣà renovam sua força vital! Você recupera {heal_amount} pontos de vida!"
                battle_success = True
        elif dice_roll == 1:  # Critical failure
            backfire = random.randint(1, 4)
            player_data['current_health'] -= backfire
            battle_message = f"A energia espiritual se descontrola! Você sofre {backfire} pontos de dano!"
            battle_success = False
        elif spirit_total >= enemy_data['spirit_resistance'] + 5:  # Strong spiritual effect
            enemy_damage_taken = player_data['spiritual'] + random.randint(2, 5)
            battle_message = f"A energia espiritual afeta profundamente o inimigo! Você causa {enemy_damage_taken} pontos de dano espiritual!"
            battle_success = True
        elif spirit_total >= enemy_data['spirit_resistance']:  # Normal spiritual effect
            enemy_damage_taken = max(1, player_data['spiritual'] - enemy_data['spirit_resistance'] // 3)
            heal_amount = random.randint(1, 3)
            player_data['current_health'] = min(player_data['current_health'] + heal_amount, player_data['max_health'])
            battle_message = f"Você canaliza energia espiritual e causa {enemy_damage_taken} pontos de dano! Também recupera {heal_amount} pontos de vida."
            battle_success = True
        else:  # Failure
            battle_message = "Você tenta canalizar energia espiritual, mas falha."
            battle_success = False

    # Apply damage to enemy
    enemy_data['current_health'] -= enemy_damage_taken

    # Log the action
    session['battle_log'].insert(0, battle_message)

    # If enemy still alive, process enemy attack
    if enemy_data['current_health'] > 0:
        # Enemy attacks
        enemy_message = f"O {enemy_data['name']} ataca!"
        session['battle_log'].insert(0, enemy_message)

        # Calculate damage
        base_damage = enemy_data['attack']
        if session.get('defending', False):
            player_damage_taken = max(1, base_damage - player_data['physical'] - random.randint(2, 5))
            enemy_message = f"Sua defesa reduziu o dano! Você recebe {player_damage_taken} pontos de dano."
        else:
            player_damage_taken = max(1, base_damage - random.randint(0, 2))
            enemy_message = f"Você recebe {player_damage_taken} pontos de dano!"

        # Apply damage to player
        player_data['current_health'] -= player_damage_taken

        # Log the enemy action
        session['battle_log'].insert(0, enemy_message)

        # Reset defending status
        session['defending'] = False

    # Update session data
    session['player'] = player_data
    session['enemy'] = enemy_data

    # Check if battle is over
    if enemy_data['current_health'] <= 0:
        # Player won
        enemy_rewards = battle.get_enemy_data(enemy_data['id']).get('rewards', {})
        session['battle_rewards'] = enemy_rewards

        # Process rewards
        reward_message = "Você ganhou: "

        if 'attribute' in enemy_rewards:
            attr_type = enemy_rewards['attribute']['type']
            attr_amount = enemy_rewards['attribute']['amount']
            player_data[attr_type] += attr_amount
            reward_message += f"+{attr_amount} {attr_type}, "

        if 'item' in enemy_rewards:
            item = enemy_rewards['item']
            if 'inventory' not in player_data:
                player_data['inventory'] = []
            player_data['inventory'].append(item)
            reward_message += f"{item}, "

        if 'health' in enemy_rewards:
            health_amount = enemy_rewards['health']
            player_data['current_health'] = min(player_data['current_health'] + health_amount, player_data['max_health'])
            reward_message += f"+{health_amount} de vida, "

        # Update session
        session['player'] = player_data
        session['battle_log'].insert(0, "Vitória! " + reward_message[:-2])

    elif player_data['current_health'] <= 0:
        # Player lost
        session['battle_log'].insert(0, f"Você foi derrotado pelo {enemy_data['name']}!")

    # Render the battle template with updated data
    return render_template('battle.html', 
                          player=session['player'],
                          enemy=session['enemy'],
                          battle_log=session['battle_log'],
                          dice_roll=dice_roll,
                          battle_message=battle_message,
                          battle_success=battle_success)

@app.route('/battle_end', methods=['POST'])
def battle_end():
    """End the battle and return to the game"""
    if 'player' not in session:
        return redirect(url_for('create_character'))

    result = request.form.get('result')

    if result == 'victory':
        # Go to victory node
        session['current_node'] = session.get('victory_node', 'start')
    else:
        # Go to defeat node
        session['current_node'] = session.get('defeat_node', 'start')

    # Clean up battle session data
    for key in ['enemy', 'battle_enemy', 'battle_log', 'battle_rewards', 'victory_node', 'defeat_node', 'defending']:
        if key in session:
            session.pop(key)

    return redirect(url_for('game'))

# ==============================================================================
# Admin routes
# ==============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor preencha todos os campos.', 'danger')
            return render_template('admin/login.html')

        admin = db.get_admin_by_username(username)
        
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            if db.update_admin_login(admin.username):
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('admin_dashboard'))
        
        flash('Usuário ou senha inválidos.', 'danger')
        return render_template('admin/login.html')

    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    # Count nodes and verify connections
    node_count = node_map.count_nodes()
    nodes_valid, node_issues = node_map.verify_node_connections()

    # Count characters
    character_count = db.count_characters()

    # Count node visits
    node_visit_count = db.count_node_visits()

    # Get most visited nodes
    top_nodes = db.get_top_visited_nodes(5)

    # Get recent characters
    recent_characters = db.get_recent_characters(5)

    return render_template(
        'admin/dashboard.html',
        node_count=node_count,
        character_count=character_count,
        node_visit_count=node_visit_count,
        top_nodes=top_nodes,
        recent_characters=recent_characters
    )

@app.route('/admin/nodes')
@admin_required
def admin_nodes():
    """Admin node list"""
    # Get all nodes
    all_nodes = {node_id: node_map.get_node(node_id) for node_id in node_map.nodes.keys()}

    return render_template('admin/nodes.html', nodes=all_nodes)

@app.route('/admin/flowchart')
@admin_required
def admin_flowchart():
    """Admin flowchart view"""
    # Get all nodes
    all_nodes = {node_id: node_map.get_node(node_id) for node_id in node_map.nodes.keys()}
    
    return render_template('admin/flowchart.html', nodes=all_nodes)

@app.route('/admin/node/<node_id>')
@admin_required
def admin_node_detail(node_id):
    """Admin node detail"""
    node = node_map.get_node(node_id)

    if 'text' not in node:
        flash('Nó não encontrado.', 'danger')
        return redirect(url_for('admin_nodes'))

@app.route('/admin/node/create', methods=['GET', 'POST'])
@admin_required
def admin_create_node():
    """Create a new node"""
    if request.method == 'POST':
        node_id = request.form.get('node_id')
        if node_id in node_map.nodes:
            flash('ID do nó já existe.', 'danger')
            return redirect(url_for('admin_create_node'))
        
        node_data = {
            'title': request.form.get('title'),
            'text': request.form.get('text'),
            'next_node': request.form.get('next_node')
        }
        
        node_map.nodes[node_id] = node_data
        node_map.save_nodes()
        flash('Nó criado com sucesso!', 'success')
        return redirect(url_for('admin_node_detail', node_id=node_id))
        
    return render_template('admin/node_form.html', node=None, action='create')

@app.route('/admin/node/<node_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_node(node_id):
    """Edit an existing node"""
    node = node_map.get_node(node_id)
    if not node:
        flash('Nó não encontrado.', 'danger')
        return redirect(url_for('admin_nodes'))
        
    if request.method == 'POST':
        node['title'] = request.form.get('title')
        node['text'] = request.form.get('text')
        node['next_node'] = request.form.get('next_node')
        
        node_map.nodes[node_id] = node
        node_map.save_nodes()
        flash('Nó atualizado com sucesso!', 'success')
        return redirect(url_for('admin_node_detail', node_id=node_id))
        
    return render_template('admin/node_form.html', node=node, node_id=node_id, action='edit')

@app.route('/admin/node/<node_id>/delete', methods=['POST'])
@admin_required
def admin_delete_node(node_id):
    """Delete a node"""
    if node_id in node_map.nodes:
        del node_map.nodes[node_id]
        node_map.save_nodes()
        flash('Nó excluído com sucesso!', 'success')
    else:
        flash('Nó não encontrado.', 'danger')
    return redirect(url_for('admin_nodes'))

    # Get node visit count
    visit_count = db.count_node_visits_for_node(node_id)

    # Get characters that visited this node
    characters = db.get_characters_that_visited_node(node_id)

    return render_template(
        'admin/node_detail.html',
        node_id=node_id,
        node=node,
        visit_count=visit_count,
        characters=characters
    )

@app.route('/admin/characters')
@admin_required
def admin_characters():
    """Admin character list"""
    characters = db.get_all_characters()
    return render_template('admin/characters.html', characters=characters)

@app.route('/admin/character/<int:character_id>')
@admin_required
def admin_character_detail(character_id):
    """Admin character detail"""
    character = db.get_character(character_id)

    if not character:
        flash('Personagem não encontrado.', 'danger')
        return redirect(url_for('admin_characters'))

    # Get visited nodes
    visited_nodes = db.get_node_visits_for_character(character_id)

    return render_template(
        'admin/character_detail.html',
        character=character,
        visited_nodes=visited_nodes,
        inventory=json.loads(character['inventory']) if character['inventory'] else [],
        abilities=json.loads(character['special_abilities']) if character['special_abilities'] else []
    )

# Utility function to record node visits
def record_node_visit(node_id):
    """Record a node visit in the database"""
    # Check if we have a character in the session
    if 'player' in session and 'id' in session['player']:
        character_id = session['player']['id']

        # Create a node visit record
        db.record_node_visit(node_id, character_id)

# Update the game route to record node visits
original_game = app.view_functions['game']

def game_with_tracking():
    """Wrapper for the game route that records node visits"""
    # Record the node visit
    if 'current_node' in session:
        record_node_visit(session['current_node'])

    # Call the original route
    return original_game()

app.view_functions['game'] = game_with_tracking

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)