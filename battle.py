"""
Battle Module - Handles the battle system
"""

import random
import time
from rich.panel import Panel
from rich.progress import Progress
from rich import box

def start_battle(console, player, enemy_id):
    """
    Start a battle with an enemy
    
    Args:
        console: Rich console object for display
        player: Player object
        enemy_id: ID of the enemy to battle
        
    Returns:
        bool: True if player wins, False if player loses
    """
    # Get enemy data from game_data (dummy implementation)
    enemy = get_enemy_data(enemy_id)
    
    # Display battle start
    console.print(Panel(
        f"[bold red]Você encontrou um {enemy['name']}![/bold red]\n\n{enemy['description']}",
        title="BATALHA INICIADA",
        border_style="red",
        box=box.HEAVY
    ))
    
    # Enemy stats
    enemy_health = enemy["health"]
    enemy_max_health = enemy["health"]
    
    # Battle loop
    while player.current_health > 0 and enemy_health > 0:
        # Display health bars
        display_health_bars(console, player.current_health, player.max_health, 
                           enemy_health, enemy_max_health, enemy["name"])
        
        # Player turn
        console.print("\n[bold cyan]Sua vez! O que deseja fazer?[/bold cyan]")
        console.print("[1] [bold red]Atacar[/bold red] (Atributo Físico)")
        console.print("[2] [bold blue]Defender[/bold blue] (Reduz dano do próximo ataque)")
        console.print("[3] [bold magenta]Espírito[/bold magenta] (Atributo Espiritual)")
        
        defending = False
        
        # Get player input
        valid_input = False
        while not valid_input:
            action = console.input("\n[bold green]> [/bold green]").strip().lower()
            
            if action in ["1", "atacar"]:
                result = player_attack(console, player, enemy)
                enemy_health -= result
                valid_input = True
                
            elif action in ["2", "defender"]:
                defending = True
                console.print("[bold blue]Você assume uma postura defensiva![/bold blue]")
                valid_input = True
                
            elif action in ["3", "espirito", "espírito"]:
                result = player_spirit(console, player, enemy)
                enemy_health -= result
                valid_input = True
                
            elif action in ["status"]:
                display_player_stats(console, player)
                continue
                
            elif action in ["ajuda", "help"]:
                display_battle_help(console)
                continue
                
            else:
                console.print("[bold red]Comando inválido! Tente novamente.[/bold red]")
        
        # Check if enemy is defeated
        if enemy_health <= 0:
            console.print(f"\n[bold green]Você derrotou o {enemy['name']}![/bold green]")
            
            # Award rewards
            award_rewards(console, player, enemy)
            
            time.sleep(2)
            return True
        
        # Enemy turn
        console.print(f"\n[bold red]O {enemy['name']} ataca![/bold red]")
        time.sleep(1)
        
        # Calculate damage
        base_damage = enemy["attack"]
        if defending:
            damage = max(1, base_damage - player.physical - random.randint(2, 5))
            console.print(f"[blue]Sua defesa reduziu o dano![/blue]")
        else:
            damage = max(1, base_damage - random.randint(0, 2))
        
        # Apply damage
        player.change_health(-damage)
        console.print(f"[red]Você recebeu {damage} pontos de dano![/red]")
        time.sleep(1)
        
        # Check if player is defeated
        if player.current_health <= 0:
            console.print(f"\n[bold red]Você foi derrotado pelo {enemy['name']}![/bold red]")
            time.sleep(2)
            return False
    
    # Should never reach here but just in case
    return player.current_health > 0

def player_attack(console, player, enemy):
    """
    Handle player's physical attack
    
    Args:
        console: Rich console object
        player: Player object
        enemy: Enemy data dictionary
        
    Returns:
        int: Amount of damage dealt
    """
    console.print("\n[bold]Testando seu atributo [red]Físico[/red]...[/bold]")
    time.sleep(0.5)
    
    # Roll dice and add physical attribute
    roll = roll_battle_dice(console)
    attack_value = roll + player.physical
    
    console.print(f"Seu Físico: [bold red]{player.physical}[/bold red]")
    console.print(f"Total do ataque: [bold magenta]{attack_value}[/bold magenta]")
    
    # Calculate damage
    if roll == 20:  # Critical hit
        damage = (player.physical * 2) + random.randint(3, 6)
        console.print("[bold bright_green]Acerto crítico![/bold bright_green]")
    elif roll == 1:  # Critical miss
        damage = 0
        console.print("[bold bright_red]Erro crítico! Você tropeça e erra o ataque![/bold bright_red]")
    elif attack_value >= enemy["defense"] + 5:  # Strong hit
        damage = player.physical + random.randint(2, 5)
        console.print("[bold green]Ótimo golpe![/bold green]")
    elif attack_value >= enemy["defense"]:  # Normal hit
        damage = max(1, player.physical + random.randint(0, 3) - enemy["defense"] // 2)
        console.print("[green]Você acerta o golpe.[/green]")
    else:  # Miss
        damage = 0
        console.print("[red]Seu ataque foi bloqueado ou desviado.[/red]")
    
    if damage > 0:
        console.print(f"[bold red]Você causou {damage} pontos de dano![/bold red]")
    
    time.sleep(1)
    return damage

def player_spirit(console, player, enemy):
    """
    Handle player's spiritual attack
    
    Args:
        console: Rich console object
        player: Player object
        enemy: Enemy data dictionary
        
    Returns:
        int: Amount of damage or healing done
    """
    console.print("\n[bold]Canalizando seu atributo [magenta]Espiritual[/magenta]...[/bold]")
    time.sleep(0.5)
    
    # Roll dice and add spiritual attribute
    roll = roll_battle_dice(console)
    spirit_value = roll + player.spiritual
    
    console.print(f"Seu Espiritual: [bold magenta]{player.spiritual}[/bold magenta]")
    console.print(f"Total espiritual: [bold cyan]{spirit_value}[/bold cyan]")
    
    # Special effects based on roll
    if roll == 20:  # Critical success
        if random.random() < 0.5:  # 50% chance for damage
            damage = player.spiritual * 2 + random.randint(2, 8)
            console.print("[bold bright_cyan]Os Òrìṣà atendem seu chamado com poder imenso![/bold bright_cyan]")
            console.print(f"[bold magenta]Você causa {damage} pontos de dano espiritual![/bold magenta]")
            return damage
        else:  # 50% chance for healing
            heal_amount = player.spiritual + random.randint(3, 8)
            player.heal(heal_amount)
            console.print("[bold bright_green]Os Òrìṣà renovam sua força vital![/bold bright_green]")
            console.print(f"[bold green]Você recupera {heal_amount} pontos de vida![/bold green]")
            return 0
    
    elif roll == 1:  # Critical failure
        backfire = random.randint(1, 4)
        player.change_health(-backfire)
        console.print("[bold bright_red]A energia espiritual se descontrola![/bold bright_red]")
        console.print(f"[bold red]Você sofre {backfire} pontos de dano![/bold red]")
        return 0
    
    elif spirit_value >= enemy.get("spirit_resistance", 10) + 5:  # Strong spiritual effect
        damage = player.spiritual + random.randint(2, 5)
        console.print("[bold cyan]A energia espiritual afeta profundamente o inimigo![/bold cyan]")
        console.print(f"[bold magenta]Você causa {damage} pontos de dano espiritual![/bold magenta]")
        return damage
    
    elif spirit_value >= enemy.get("spirit_resistance", 10):  # Normal spiritual effect
        damage = max(1, player.spiritual - enemy.get("spirit_resistance", 0) // 3)
        heal_amount = random.randint(1, 3)
        player.heal(heal_amount)
        console.print("[cyan]Você canaliza energia espiritual.[/cyan]")
        console.print(f"[magenta]Você causa {damage} pontos de dano espiritual![/magenta]")
        console.print(f"[green]Você recupera {heal_amount} pontos de vida![/green]")
        return damage
    
    else:  # Failure
        console.print("[red]Você tenta canalizar energia espiritual, mas falha.[/red]")
        return 0

def roll_battle_dice(console):
    """
    Roll a d20 for battle and display the result
    
    Args:
        console: Rich console object
        
    Returns:
        int: The dice roll result
    """
    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Rolando dado...", total=100)
        
        for i in range(10):
            progress.update(task, advance=10)
            time.sleep(0.05)
    
    result = random.randint(1, 20)
    
    if result == 20:
        console.print(f"[bold bright_green]Rolagem: {result}[/bold bright_green] [bright_green]Sucesso crítico![/bright_green]")
    elif result == 1:
        console.print(f"[bold bright_red]Rolagem: {result}[/bold bright_red] [bright_red]Falha crítica![/bright_red]")
    elif result >= 15:
        console.print(f"[bold green]Rolagem: {result}[/bold green] [green]Ótimo resultado![/green]")
    elif result >= 10:
        console.print(f"[bold yellow]Rolagem: {result}[/bold yellow] [yellow]Resultado médio[/yellow]")
    else:
        console.print(f"[bold red]Rolagem: {result}[/bold red] [red]Resultado baixo[/red]")
    
    return result

def display_health_bars(console, player_health, player_max, enemy_health, enemy_max, enemy_name):
    """
    Display health bars for player and enemy
    
    Args:
        console: Rich console object
        player_health: Current player health
        player_max: Maximum player health
        enemy_health: Current enemy health
        enemy_max: Maximum enemy health
        enemy_name: Name of the enemy
    """
    player_bar = create_health_bar(player_health, player_max)
    enemy_bar = create_health_bar(enemy_health, enemy_max)
    
    console.print("\n[bold]Status de Batalha:[/bold]")
    console.print(f"Você: {player_bar} {player_health}/{player_max}")
    console.print(f"{enemy_name}: {enemy_bar} {enemy_health}/{enemy_max}")

def create_health_bar(current, maximum, width=20):
    """
    Create a visual health bar
    
    Args:
        current: Current health
        maximum: Maximum health
        width: Width of the health bar
        
    Returns:
        str: A string representing the health bar
    """
    filled = int(width * (current / maximum))
    empty = width - filled
    
    if current / maximum > 0.7:  # High health
        bar = "[bold green]" + "█" * filled + "[/bold green]" + "[red]" + "░" * empty + "[/red]"
    elif current / maximum > 0.3:  # Medium health
        bar = "[bold yellow]" + "█" * filled + "[/bold yellow]" + "[red]" + "░" * empty + "[/red]"
    else:  # Low health
        bar = "[bold red]" + "█" * filled + "[/bold red]" + "[red]" + "░" * empty + "[/red]"
    
    return bar

def display_player_stats(console, player):
    """
    Display player stats during battle
    
    Args:
        console: Rich console object
        player: Player object
    """
    console.print("\n[bold yellow]Seus Atributos:[/bold yellow]")
    console.print(f"Mental: [cyan]{player.mental}[/cyan]")
    console.print(f"Físico: [red]{player.physical}[/red]")
    console.print(f"Espiritual: [magenta]{player.spiritual}[/magenta]")
    console.print(f"Vida: [green]{player.current_health}[/green]/[green]{player.max_health}[/green]")

def display_battle_help(console):
    """
    Display help information during battle
    
    Args:
        console: Rich console object
    """
    help_text = """
    [bold yellow]Comandos de Batalha:[/bold yellow]
    
    [bold red]atacar[/bold red] ou [bold red]1[/bold red] - Usa seu atributo Físico para atacar o inimigo
    [bold blue]defender[/bold blue] ou [bold blue]2[/bold blue] - Reduz o dano do próximo ataque inimigo
    [bold magenta]espírito[/bold magenta] ou [bold magenta]3[/bold magenta] - Usa seu atributo Espiritual para efeitos diversos
    [bold cyan]status[/bold cyan] - Mostra seus atributos atuais
    [bold green]ajuda[/bold green] - Mostra esta mensagem
    """
    console.print(Panel(help_text, title="Ajuda de Batalha", border_style="green"))

def award_rewards(console, player, enemy):
    """
    Award rewards to player after defeating an enemy
    
    Args:
        console: Rich console object
        player: Player object
        enemy: Enemy data dictionary
    """
    # Award attribute points
    if "rewards" in enemy:
        rewards = enemy["rewards"]
        
        if "attribute" in rewards:
            attr_type = rewards["attribute"]["type"]
            attr_amount = rewards["attribute"]["amount"]
            
            player.modify_attribute(attr_type, attr_amount)
            console.print(f"[bold green]Seu atributo [cyan]{attr_type.capitalize()}[/cyan] aumentou em {attr_amount}![/bold green]")
        
        if "item" in rewards:
            item = rewards["item"]
            player.add_to_inventory(item)
            console.print(f"[bold green]Você encontrou: [yellow]{item}[/yellow][/bold green]")
        
        if "health" in rewards:
            health_amount = rewards["health"]
            player.heal(health_amount)
            console.print(f"[bold green]Você recuperou [red]{health_amount}[/red] pontos de vida![/bold green]")
    
    # Random reward chance
    if random.random() < 0.3:  # 30% chance for random reward
        reward_type = random.choice(["mental", "physical", "spiritual"])
        reward_amount = random.randint(1, 2)
        
        player.modify_attribute(reward_type, reward_amount)
        console.print(f"[bold cyan]Prêmio adicional! Seu [yellow]{reward_type.capitalize()}[/yellow] aumentou em {reward_amount}![/bold cyan]")

def get_enemy_data(enemy_id):
    """
    Get enemy data from game data
    
    Args:
        enemy_id: ID of the enemy
        
    Returns:
        dict: Enemy data dictionary
    """
    # This is a placeholder implementation. The actual data would come from game_data
    enemies = {
        "guard": {
            "name": "Guarda Real",
            "description": "Um guarda forte e disciplinado, protegendo o palácio com lança e escudo.",
            "health": 15,
            "attack": 4,
            "defense": 8,
            "spirit_resistance": 5,
            "rewards": {
                "attribute": {"type": "physical", "amount": 1},
                "item": "Amuleto de Proteção"
            }
        },
        "wolf": {
            "name": "Lobo Espiritual",
            "description": "Um lobo de pelagem brilhante, seus olhos revelam inteligência sobrenatural.",
            "health": 12,
            "attack": 5,
            "defense": 6,
            "spirit_resistance": 8,
            "rewards": {
                "attribute": {"type": "spiritual", "amount": 1},
                "health": 3
            }
        },
        "shaman": {
            "name": "Xamã Hostil",
            "description": "Um praticante de magia antiga que vê você como uma ameaça às tradições.",
            "health": 10,
            "attack": 3,
            "defense": 4,
            "spirit_resistance": 12,
            "rewards": {
                "attribute": {"type": "mental", "amount": 1},
                "item": "Ervas Medicinais"
            }
        },
        "snake": {
            "name": "Serpente Gigante",
            "description": "Uma serpente enorme, possivelmente um mensageiro do Òrìṣà Oxumaré.",
            "health": 18,
            "attack": 6,
            "defense": 5,
            "spirit_resistance": 7,
            "rewards": {
                "attribute": {"type": "physical", "amount": 1},
                "health": 5
            }
        },
        "spirit": {
            "name": "Espírito Ancestral",
            "description": "Uma figura etérea que parece testar sua dignidade espiritual.",
            "health": 14,
            "attack": 4,
            "defense": 9,
            "spirit_resistance": 15,
            "rewards": {
                "attribute": {"type": "spiritual", "amount": 2},
                "item": "Símbolo Sagrado"
            }
        }
    }
    
    # Return the enemy data or a default if not found
    return enemies.get(enemy_id, {
        "name": "Inimigo Desconhecido",
        "description": "Um ser misterioso bloqueia seu caminho.",
        "health": 10,
        "attack": 3,
        "defense": 5,
        "spirit_resistance": 5
    })
