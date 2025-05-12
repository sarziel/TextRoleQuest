"""
Node Map Module - Defines the story structure and nodes
"""

import random
import game_data

# The story nodes are structured as a dictionary with the following format:
nodes = {
    "01_001": {
        "title": "O Portal Ancestral",
        "text": """Você é transportado em um redemoinho de luz e cor. Quando a visão retorna, você se encontra em um cenário completamente diferente...""",
        "choices": [
            {
                "text": "Examinar o amuleto que está no seu pescoço",
                "next_node": "01_002"
            },
            {
                "text": "Buscar a origem do som dos tambores",
                "next_node": "01_003"
            }
        ]
    },
    "01_002": {
        "title": "O Amuleto Misterioso",
        "text": """Você segura o amuleto com cuidado, examinando-o de perto...""",
        "next_node": "01_003"
    },
    "01_003": {
        "title": "O Vale dos Ferreiros",
        "text": """Você segue o caminho da esquerda, descendo por um vale rochoso...""",
        "battle": "iron_guardian",
        "victory_node": "01_004",
        "defeat_node": "04_001"
    },
    "02_001": {
        "title": "Confronto com o Guardião",
        "text": """Uma figura imponente de metal bloqueou seu caminho...""",
        "battle": "metal_guardian",
        "victory_node": "01_005",
        "defeat_node": "04_002"
    },
    "03_001": {
        "title": "A Passagem Direta",
        "text": """Um corredor estreito leva diretamente ao próximo local...""",
        "next_node": "01_006"
    },
    "04_001": {
        "title": "Fim da Jornada",
        "text": """Sua aventura chega a um fim prematuro...""",
        "end": True
    },
    "04_002": {
        "title": "Vitória Final",
        "text": """Você conseguiu completar sua missão...""",
        "end": True
    }
}

def get_node(node_id):
    """Get a story node by its ID"""
    return nodes.get(node_id, {
        "text": "Something went wrong. This node doesn't exist.",
        "next_node": "01_001"
    })

def get_random_node_id(node_type=None):
    """
    Get a random node ID, optionally of a specific type

    Args:
        node_type (str, optional): The type of node to retrieve

    Returns:
        str: A random node ID
    """
    valid_nodes = []

    for node_id, node_data in nodes.items():
        if node_type == "battle" and "battle" in node_data:
            valid_nodes.append(node_id)
        elif node_type == "choice" and "choices" in node_data:
            valid_nodes.append(node_id)
        elif node_type == "orisha" and node_data.get("orisha", False):
            valid_nodes.append(node_id)
        elif node_type is None:
            valid_nodes.append(node_id)

    if valid_nodes:
        return random.choice(valid_nodes)
    else:
        return "01_001"


def verify_node_connections():
    """Verify node connections"""
    issues = []
    reachable_nodes = set()
    all_nodes = set(nodes.keys())

    to_visit = ['01_001']
    reachable_nodes.add('01_001')

    while to_visit:
        current = to_visit.pop()
        node = nodes.get(current)

        if not node:
            issues.append(f"Node {current} is referenced but doesn't exist")
            continue

        if 'choices' in node:
            for choice in node['choices']:
                next_nodes = []
                if 'next_node' in choice:
                    next_nodes.append(choice['next_node'])
                if 'success_node' in choice:
                    next_nodes.append(choice['success_node'])
                if 'failure_node' in choice:
                    next_nodes.append(choice['failure_node'])

                for next_node in next_nodes:
                    if next_node not in nodes:
                        issues.append(f"Node {current} references non-existent node {next_node}")
                    elif next_node not in reachable_nodes:
                        reachable_nodes.add(next_node)
                        to_visit.append(next_node)

        if 'next_node' in node:
            next_node = node['next_node']
            if next_node not in nodes:
                issues.append(f"Node {current} references non-existent node {next_node}")
            elif next_node not in reachable_nodes:
                reachable_nodes.add(next_node)
                to_visit.append(next_node)

        # Check battle outcomes
        if 'victory_node' in node:
            next_node = node['victory_node']
            if next_node not in nodes:
                issues.append(f"Node {current} references non-existent victory node {next_node}")
            elif next_node not in reachable_nodes:
                reachable_nodes.add(next_node)
                to_visit.append(next_node)

        if 'defeat_node' in node:
            next_node = node['defeat_node']
            if next_node not in nodes:
                issues.append(f"Node {current} references non-existent defeat node {next_node}")
            elif next_node not in reachable_nodes:
                reachable_nodes.add(next_node)
                to_visit.append(next_node)

    unreachable = all_nodes - reachable_nodes
    if unreachable:
        issues.append(f"Unreachable nodes found: {', '.join(unreachable)}")

    return len(issues) == 0, issues

def count_nodes():
    """Count total nodes"""
    return len(nodes)

def save_nodes():
    """Save nodes (in-memory implementation)"""
    pass