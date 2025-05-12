"""
Node Map Module - Defines the story structure and nodes
"""

import random
import game_data

# The story nodes are structured as a dictionary with the following format:
# nodes = {
#     "node_id": {
#         "text": "The text to display for this node",
#         "title": "Optional title for the node",
#         "orisha": True/False,  # Whether this is dialogue from an Òrìṣà
#         "choices": [
#             {
#                 "text": "Choice 1 text",
#                 "next_node": "node_id_for_choice_1"
#                 # OR
#                 "test": "attribute",  # mental, physical, spiritual
#                 "difficulty": 10,
#                 "success_node": "node_id_on_success",
#                 "failure_node": "node_id_on_failure"
#             }
#         ],
#         # OR
#         "next_node": "next_node_id",  # For nodes with no choices
#         # OR
#         "battle": "enemy_id",  # ID of the enemy to battle
#         "victory_node": "node_after_victory",
#         "defeat_node": "node_after_defeat",
#         # For ending nodes
#         "end": True
#     }
# }

def get_node(node_id):
    """
    Get a story node by its ID

    Args:
        node_id (str): The ID of the node to retrieve

    Returns:
        dict: The node data
    """
    # Return the node from the pre-defined nodes dictionary
    # If not found, return a fallback node
    return nodes.get(node_id, {
        "text": "Something went wrong. This node doesn't exist.",
        "next_node": "start"
    })

def get_random_node_id(node_type=None):
    """
    Get a random node ID, optionally of a specific type

    Args:


def verify_node_connections():
    """
    Verify that all nodes are properly connected and reachable
    Returns a tuple of (is_valid, list of issues)
    """
    issues = []
    reachable_nodes = set()
    all_nodes = set(nodes.keys())
    
    # Start from the initial node
    to_visit = ['start']
    reachable_nodes.add('start')
    
    # Traverse all connected nodes
    while to_visit:
        current = to_visit.pop()
        node = nodes.get(current)
        
        if not node:
            issues.append(f"Node {current} is referenced but doesn't exist")
            continue
            
        # Check choices
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
                        
        # Check direct next node
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
    
    # Check for unreachable nodes
    unreachable = all_nodes - reachable_nodes
    if unreachable:
        issues.append(f"Unreachable nodes found: {', '.join(unreachable)}")
    
    return len(issues) == 0, issues

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
        return "start"  # Fallback to start node

def count_nodes():
    """
    Count the total number of nodes in the game

    Returns:
        int: The total number of nodes
    """
    return len(nodes)

# Define the story nodes
nodes = {
    "start": {
        "title": "O Portal Ancestral",
        "text": """Você é transportado em um redemoinho de luz e cor. Quando a visão retorna, você se encontra em um cenário completamente diferente.

Em vez das ruínas empoeiradas da escavação arqueológica, você está em uma floresta vibrante. O ar é úmido e cheio de aromas desconhecidos. Pássaros coloridos voam acima, e o som de tambores distantes ecoa pelas árvores.

Você olha para suas mãos e vê que ainda está com a mesma roupa, e sua mochila ainda está nas suas costas. O amuleto que você tocou nas ruínas agora pende do seu pescoço, brilhando levemente.

Por um momento, você se pergunta se está sonhando.""",
        "choices": [
            {
                "text": "Examinar o amuleto que está no seu pescoço",
                "next_node": "examine_amulet"
            },
            {
                "text": "Buscar a origem do som dos tambores",
                "next_node": "follow_drums"
            },
            {
                "text": "Procurar por sinais do portal que te trouxe aqui",
                "test": "mental",
                "difficulty": 8,
                "success_node": "find_portal_success",
                "failure_node": "find_portal_failure"
            }
        ]
    },

    "examine_amulet": {
        "title": "O Amuleto Misterioso",
        "text": """Você segura o amuleto com cuidado, examinando-o de perto. É feito de um metal dourado que não consegue identificar, com intrincados símbolos gravados em sua superfície.

No centro do amuleto há uma pedra azul profunda que parece pulsar com luz própria. Os símbolos ao redor dela se assemelham a figuras humanas em poses de dança ou adoração.

Enquanto você estuda o objeto, a pedra emite um brilho mais intenso, e você sente uma estranha conexão com ela, como se estivesse tentando comunicar algo.""",
        "choices": [
            {
                "text": "Concentrar-se na pedra, tentando entender sua mensagem",
                "test": "spiritual",
                "difficulty": 10,
                "success_node": "amulet_vision",
                "failure_node": "amulet_confusion"
            },
            {
                "text": "Guardar o amuleto e seguir em direção aos tambores",
                "next_node": "follow_drums"
            },
            {
                "text": "Tentar identificar os símbolos com seu conhecimento",
                "test": "mental",
                "difficulty": 12,
                "success_node": "identify_symbols",
                "failure_node": "cant_identify"
            }
        ]
    },

    "amulet_vision": {
        "title": "Visões do Passado",
        "text": """Ao se concentrar na pedra azul, sua visão fica turva e você é inundado por imagens que fluem rapidamente:

Vê homens e mulheres dançando em círculo, usando vestimentas coloridas... Um rei sentado em um trono dourado... Sacerdotes realizando rituais diante de estátuas... E figuras luminosas observando tudo do céu, com expressões serenas.

Em um instante, você compreende: está em Yorùbáland, no coração da antiga civilização Yorùbá, centenas de anos antes do seu tempo. E o amuleto é uma relíquia sagrada, um elo entre os mortais e os Òrìṣà - as divindades que supervisionam o mundo.

A visão se dissipa, mas você agora possui um entendimento instintivo do poder do amuleto.""",
        "choices": [
            {
                "text": "Seguir para os tambores, agora com novo conhecimento",
                "next_node": "follow_drums_informed"
            },
            {
                "text": "Tentar usar o amuleto para se comunicar com os Òrìṣà",
                "test": "spiritual",
                "difficulty": 15,
                "success_node": "orisha_contact",
                "failure_node": "failed_contact"
            }
        ]
    },

    "amulet_confusion": {
        "title": "Confusão Mental",
        "text": """Você se concentra na pedra, esperando algum tipo de revelação, mas nada acontece.

A pedra continua brilhando suavemente, mas parece que sua mente não consegue sintonizar com o que quer que o amuleto esteja tentando transmitir.

Após alguns minutos frustrados de tentativa, você suspira e desiste. Talvez precise de algum conhecimento adicional para entender este artefato.""",
        "next_node": "follow_drums"
    },

    "identify_symbols": {
        "title": "Símbolos Revelados",
        "text": """Observando atentamente os símbolos, você percebe padrões que remetem a suas pesquisas sobre culturas africanas antigas.

Os desenhos representam as divindades Yorùbá - os Òrìṣà. Você identifica representações de Ogun, o deus do ferro e da guerra; Yemoja, deusa dos oceanos; Sango, deus do trovão; e no centro, Olodumare, o criador supremo.

Sua formação acadêmica permitiu que você reconhecesse esses símbolos, mas vê-los aqui, neste artefato antigo, confirma que você realmente viajou no tempo para a época em que esses deuses eram ativamente adorados.""",
        "choices": [
            {
                "text": "Seguir o som dos tambores com seu novo conhecimento",
                "next_node": "follow_drums_informed"
            },
            {
                "text": "Invocar o nome de Ogun, deus da guerra, em busca de proteção",
                "next_node": "invoke_ogun"
            }
        ]
    },

    "cant_identify": {
        "title": "Símbolos Misteriosos",
        "text": """Você examina os símbolos com atenção, mas eles não se encaixam em nenhum padrão que você reconheça de seus estudos.

Claramente são importantes e carregados de significado, mas sem mais contexto ou conhecimento, não consegue decifrar o que representam.

Frustrado, você guarda o amuleto no bolso, decidindo que precisa aprender mais sobre onde está para entender o objeto.""",
        "next_node": "follow_drums"
    },

    "follow_drums": {
        "title": "Seguindo o Ritmo",
        "text": """Orientando-se pelo som dos tambores, você começa a caminhar pela floresta. O caminho não é claro, mas o ritmo se torna mais alto à medida que avança.

A vegetação é densa, com plantas que você nunca viu antes. O calor é intenso, e gotas de suor escorrem pelo seu rosto enquanto se esforça para atravessar o terreno acidentado.

Após cerca de vinte minutos, você chega a uma clareira e fica paralisado pela visão à sua frente: uma aldeia inteira, com cabanas de palha e barro dispostas em círculo. No centro, pessoas dançam ao som dos tambores, vestindo roupas coloridas e decoradas.

Você se esconde atrás de uma árvore, observando a cena com espanto.""",
        "choices": [
            {
                "text": "Observar cuidadosamente para entender o que está acontecendo",
                "test": "mental",
                "difficulty": 10,
                "success_node": "observe_ritual",
                "failure_node": "spotted_hiding"
            },
            {
                "text": "Aproximar-se abertamente da aldeia",
                "next_node": "approach_village"
            },
            {
                "text": "Contornar a aldeia e explorar outras direções",
                "next_node": "forest_path"
            }
        ]
    },

    "follow_drums_informed": {
        "title": "Rumo à Aldeia",
        "text": """Com seu novo entendimento sobre onde está, você segue o som dos tambores com confiança renovada.

Enquanto caminha, você toca o amuleto ocasionalmente, sentindo uma conexão mais forte com o ambiente ao seu redor. A floresta parece responder à sua presença, como se reconhecesse o artefato que você carrega.

Logo, você avista uma aldeia yorùbá tradicional na distância. Pessoas dançam em círculo, e sacerdotes lideram o que parece ser um festival ou ritual importante.""",
        "choices": [
            {
                "text": "Observar o ritual de longe, analisando seus elementos",
                "test": "mental",
                "difficulty": 10,
                "success_node": "observe_ritual",
                "failure_node": "spotted_hiding"
            },
            {
                "text": "Aproximar-se com o amuleto visível, mostrando sua conexão",
                "next_node": "approach_with_amulet"
            }
        ]
    },

    "observe_ritual": {
        "title": "Ritual de Invocação",
        "text": """De seu esconderijo, você observa com atenção o que acontece na aldeia.

Este não é um simples festival - é um ritual religioso elaborado. Os dançarinos se movem em padrões específicos, e os sacerdotes fazem oferendas diante de estátuas de madeira ornamentadas.

Você reconhece elementos que estudou: estão realizando um ritual de invocação para Sango, o poderoso Òrìṣà do trovão e da justiça. As roupas vermelhas e brancas, os tambores batendo em padrões que imitam trovão, as oferendas de frutas e carneiro - tudo indica uma cerimônia importante.

No centro do círculo, um homem mais velho com vestes elaboradas parece entrar em transe, sua voz mudando para um tom grave e poderoso.""",
        "choices": [
            {
                "text": "Continuar observando discretamente",
                "next_node": "ritual_climax"
            },
            {
                "text": "Aproximar-se para ouvir melhor o que o homem em transe está dizendo",
                "test": "physical",
                "difficulty": 12,
                "success_node": "hear_prophecy",
                "failure_node": "spotted_ritual"
            }
        ]
    },

    "forest_path": {
        "title": "Trilha na Floresta",
        "text": """Você deixa a aldeia para trás e segue por uma trilha estreita na floresta. O caminho é irregular e parcialmente coberto por vegetação, mas é claramente utilizado com frequência.

Enquanto se afasta do som dos tambores, outros sons da floresta começam a se destacar: o canto de pássaros exóticos, o zumbido de insetos e o ocasional rugido distante de algum animal.

Após cerca de meia hora de caminhada, você chega a uma bifurcação. O caminho à esquerda parece descer em direção a um vale, onde você consegue vislumbrar o brilho de água entre as árvores - provavelmente um rio. O caminho à direita sobe uma colina, e você pode ver o que parece ser uma estrutura de pedra no topo.""",
        "choices": [
            {
                "text": "Seguir o caminho à esquerda, em direção ao rio",
                "next_node": "river_shrine"
            },
            {
                "text": "Seguir o caminho à direita, em direção à estrutura de pedra",
                "next_node": "stone_structure"
            },
            {
                "text": "Esperar e observar a área em busca de sinais de perigo",
                "test": "mental",
                "difficulty": 10,
                "success_node": "path_observation_success",
                "failure_node": "path_observation_failure"
            }
        ]
    },

    "river_shrine": {
        "title": "O Santuário do Rio",
        "text": """Você segue a trilha que desce em direção ao vale. À medida que se aproxima, o som da água corrente se torna mais claro. Finalmente, a floresta se abre e revela um rio largo e calmo.

Nas margens do rio, uma pequena estrutura chamou sua atenção. É um santuário dedicado a Yemoja, a deusa dos rios e oceanos. Pequenas oferendas - flores, conchas e pedras coloridas - foram cuidadosamente dispostas ao redor de uma estátua feminina que parece emergir das águas.

O local tem uma atmosfera serena, e você sente uma presença reconfortante, como se estivesse sendo observado por olhos benevolentes.""",
        "choices": [
            {
                "text": "Fazer uma oferenda improvisada a Yemoja",
                "next_node": "yemoja_offering"
            },
            {
                "text": "Examinar os símbolos e artefatos no santuário",
                "test": "mental",
                "difficulty": 12,
                "success_node": "yemoja_symbols_success",
                "failure_node": "yemoja_symbols_failure"
            },
            {
                "text": "Beber água do rio para matar a sede",
                "next_node": "river_water"
            }
        ]
    },

    "stone_structure": {
        "title": "O Templo Antigo",
        "text": """Seguindo o caminho à direita, você sobe pela colina. A vegetação vai ficando mais esparsa, e logo você avista claramente a estrutura de pedra.

É um pequeno templo, construído com blocos de pedra cuidadosamente encaixados. A entrada é adornada com colunas entalhadas com símbolos que você reconhece vagamente como relacionados à cultura Yorùbá. Apesar de sua aparente antiguidade, o templo está em boas condições.

Ao se aproximar da entrada, você nota uma estátua de pedra representando uma figura masculina segurando um machado duplo - o símbolo de Sango, o Òrìṣà do trovão e da justiça.""",
        "choices": [
            {
                "text": "Entrar no templo para explorar",
                "next_node": "temple_interior"
            },
            {
                "text": "Examinar os entalhes nas colunas mais de perto",
                "test": "mental",
                "difficulty": 12,
                "success_node": "decipher_temple_symbols",
                "failure_node": "partial_temple_understanding"
            },
            {
                "text": "Voltar para a bifurcação e seguir outro caminho",
                "next_node": "forest_path"
            }
        ]
    },

    "temple_interior": {
        "title": "Dentro do Templo de Sango",
        "text": """Você respira fundo e entra no templo. O interior é espaçoso e fresco comparado ao calor externo. Feixes de luz entram por pequenas aberturas no teto, iluminando o ambiente com um brilho dourado.

No centro da sala principal há um altar de pedra, sobre o qual repousa um machado duplo cerimonial, feito de metal brilhante. Nas paredes, murais elaborados retratam a história de Sango - sua ascensão como rei, seu domínio sobre o trovão e sua eventual deificação.

O local tem uma atmosfera de poder concentrado, e você sente uma presença imponente, como se estivesse sendo julgado por olhos invisíveis.""",
        "choices": [
            {
                "text": "Aproximar-se do altar para examinar o machado",
                "next_node": "examine_axe"
            },
            {
                "text": "Estudar os murais nas paredes",
                "test": "mental",
                "difficulty": 10,
                "success_node": "study_murals_success",
                "failure_node": "study_murals_failure"
            },
            {
                "text": "Fazer uma reverência respeitosa e recuar",
                "next_node": "temple_respect"
            }
        ]
    },

    "decipher_temple_symbols": {
        "title": "Símbolos Revelados",
        "text": """Você examina cuidadosamente os entalhes nas colunas, e seu conhecimento acadêmico permite que você decifre parte do seu significado.

Os símbolos contam a história da fundação deste templo: foi construído após uma grande tempestade que quase destruiu a aldeia próxima. O povo, acreditando que Sango demonstrava sua ira, ergueu este santuário para apaziguá-lo.

Você também descobre que este é um local de julgamento, onde disputas importantes eram resolvidas sob o olhar de Sango, que favorecia a verdade e a justiça acima de tudo. Aqueles que mentissem dentro do templo atrairiam sua ira na forma de um raio.""",
        "choices": [
            {
                "text": "Entrar no templo com o novo conhecimento",
                "next_node": "temple_interior_informed"
            },
            {
                "text": "Voltar pelo caminho e seguir para o rio",
                "next_node": "river_shrine"
            }
        ]
    },

    "partial_temple_understanding": {
        "title": "Pistas Parciais",
        "text": """Você estuda os entalhes nas colunas, mas muitos dos símbolos são complexos demais para sua compreensão atual.

Consegue discernir que este é um templo dedicado a Sango, e que tem algo a ver com justiça e julgamento, mas os detalhes específicos escapam ao seu entendimento.

Uma coisa fica clara: este é um local de grande poder e significado para o povo local.""",
        "choices": [
            {
                "text": "Entrar no templo para explorar mais",
                "next_node": "temple_interior"
            },
            {
                "text": "Voltar pelo caminho e seguir para o rio",
                "next_node": "river_shrine"
            }
        ]
    },

    "temple_interior_informed": {
        "title": "Templo da Justiça",
        "text": """Com seu conhecimento aprimorado sobre o propósito deste templo, você entra com maior confiança.

O interior é como esperava: uma câmara ampla com um altar central, iluminada por feixes de luz natural. O que não esperava era encontrar outra pessoa ali.

Um homem idoso usando vestes elaboradas está de pé junto ao altar. Ele se vira ao ouvir seus passos e o observa com um olhar penetrante. 'Você não é deste lugar,' ele diz em uma língua que, surpreendentemente, você consegue entender. 'No entanto, Sango permitiu sua entrada. Isso é... interessante.'""",
        "choices": [
            {
                "text": "Explicar honestamente sua situação",
                "next_node": "honest_explanation"
            },
            {
                "text": "Inventar uma história sobre ser um viajante de terras distantes",
                "next_node": "false_explanation"
            },
            {
                "text": "Perguntar quem ele é e qual seu papel neste templo",
                "next_node": "ask_about_priest"
            }
        ]
    },

    "approach_village": {
        "title": "Aproximação à Aldeia",
        "text": """Você decide que esconder-se não é a melhor abordagem e caminha abertamente em direção à aldeia. Enquanto se aproxima, várias pessoas notam sua presença e param o que estavam fazendo para observá-lo.

Sua aparência e roupas claramente o marcam como um estranho, e você percebe expressões de surpresa e desconfiança. Alguns homens pegam lanças, embora não as apontem para você - ainda.

Um homem de meia-idade, usando vestes elaboradas e um colar de contas coloridas, dá um passo à frente. 'Quem é você e de onde vem?' ele pergunta em uma língua que, para sua surpresa, você consegue entender perfeitamente.""",
        "choices": [
            {
                "text": "Explicar honestamente que você é um viajante de outro tempo",
                "test": "mental",
                "difficulty": 15,
                "success_node": "honest_explanation_success",
                "failure_node": "honest_explanation_fail"
            },
            {
                "text": "Dizer que é um viajante de terras distantes",
                "next_node": "traveler_story"
            },
            {
                "text": "Mostrar o amuleto em seu pescoço",
                "next_node": "show_amulet_village"
            }
        ]
    },

    "approach_with_amulet": {
        "title": "O Amuleto Revelado",
        "text": """Com o conhecimento adquirido, você caminha confiante em direção à aldeia, o amuleto brilhando visivelmente em seu peito.

O efeito é imediato e surpreendente. Pessoas param de dançar e olham em sua direção. Murmúrios se espalham pela multidão. Alguns parecem temerosos, outros curiosos, e alguns se prostram no chão.

Um homem idoso com vestes elaboradas e um cajado ornamentado se aproxima de você, olhando fixamente para o amuleto. 'O Amuleto de Ashe,' ele diz com voz trêmula. 'O artefato perdido retornou.' Ele ergue os olhos para seu rosto. 'E quem é você, que o traz de volta para nós?'""",
        "choices": [
            {
                "text": "Dizer a verdade sobre sua origem",
                "next_node": "truth_to_babalawo"
            },
            {
                "text": "Afirmar que foi enviado pelos Òrìṣà",
                "test": "spiritual",
                "difficulty": 14,
                "success_node": "claim_orisha_messenger",
                "failure_node": "false_claim_exposed"
            },
            {
                "text": "Perguntar sobre o significado do amuleto",
                "next_node": "ask_about_amulet"
            }
        ]
    },

    "examine_axe": {
        "title": "O Machado Sagrado",
        "text": """Você se aproxima do altar e examina cuidadosamente o machado cerimonial. É uma peça de artesanato extraordinária - um machado duplo de bronze polido com cabo ornamentado em madeira escura e detalhes em contas coloridas.

As lâminas têm símbolos gravados que você reconhece parcialmente como relâmpagos estilizados e padrões geométricos representando justiça e poder. O metal emite um suave zumbido quando você se aproxima, como se carregado com eletricidade estática.

Um arrepio percorre sua espinha enquanto contempla o objeto. Este não é apenas um símbolo de culto - você sente instintivamente que possui poderes reais.""",
        "choices": [
            {
                "text": "Tocar o machado com cuidado",
                "test": "spiritual",
                "difficulty": 15,
                "success_node": "axe_touch_success",
                "failure_node": "axe_touch_failure" 
            },
            {
                "text": "Recuar respeitosamente sem tocar",
                "next_node": "temple_respect"
            },
            {
                "text": "Examinar as oferendas no altar",
                "next_node": "examine_offerings"
            }
        ]
    },

    "study_murals_success": {
        "title": "Revelações nas Paredes",
        "text": """Você estuda atentamente os murais nas paredes e seu conhecimento cultural permite que você interprete a narrativa visual.

As pinturas contam a história de Sango, que começou como o quarto rei de Oyo. Dotado de temperamento forte e habilidades mágicas relacionadas ao trovão, ele governou com mão firme. Uma tragédia ocorreu quando sua magia saiu de controle e destruiu parte de seu palácio.

Envergonhado, Sango se exilou e eventualmente ascendeu aos céus, tornando-se um Òrìṣà. O templo foi construído para honrá-lo e pedir sua proteção e justiça.

Um painel específico chama sua atenção - mostra Sango empunhando seu machado duplo contra seres sombrios que parecem emergir de uma fenda entre mundos. Abaixo, há uma inscrição que você decifra como: "Quando as tempestades cruzam os reinos, apenas o justiceiro pode restaurar o equilíbrio.".""",
        "choices": [
            {
                "text": "Examinar o machado no altar",
                "next_node": "examine_axe"
            },
            {
                "text": "Procurar por passagens secretas no templo",
                "test": "mental",
                "difficulty": 14,
                "success_node": "find_secret_chamber",
                "failure_node": "no_secret_found"
            },
            {
                "text": "Sair do templo",
                "next_node": "temple_exit"
            }
        ]
    },

    "study_murals_failure": {
        "title": "Imagens Enigmáticas",
        "text": """Você observa os murais nas paredes, mas os símbolos e cenas são complexos demais para interpretar completamente com seu conhecimento atual.

Reconhece que as pinturas parecem contar a história de um homem que se torna uma divindade, e há várias cenas de tempestades, julgamentos e batalhas. O uso frequente da cor vermelha e de símbolos de raios sugere poder e fúria divina.

Uma imagem recorrente é a de um homem segurando um machado duplo, semelhante ao que está no altar. Este deve ser Sango, mas os detalhes específicos de sua história permanecem obscuros para você.""",
        "choices": [
            {
                "text": "Examinar o machado no altar",
                "next_node": "examine_axe"
            },
            {
                "text": "Sair do templo",
                "next_node": "temple_exit"
            }
        ]
    },

    "temple_respect": {
        "title": "Respeitando os Deuses",
        "text": """Sentindo a atmosfera sagrada do local, você decide mostrar respeito. Curva-se diante do altar e recua alguns passos.

A ação parece apropriada, pois você sente uma sutil mudança no ambiente - como se sua reverência tivesse sido notada e aprovada. O ar vibra levemente e você ouve um distante som de trovão, apesar do céu claro que viu ao entrar.

Enquanto medita sobre a sensação, percebe uma presença atrás de você. Virando-se, encontra um homem idoso com vestes elaboradas, observando-o com interesse.""",
        "choices": [
            {
                "text": "Apresentar-se ao homem",
                "next_node": "meet_priest"
            },
            {
                "text": "Perguntar sobre o templo e seu significado",
                "next_node": "ask_about_temple"
            },
            {
                "text": "Perguntar sobre o machado no altar",
                "next_node": "ask_about_axe"
            }
        ]
    },

    "temple_exit": {
        "title": "Saindo do Templo",
        "text": """Você decide que já viu o suficiente e caminha em direção à saída do templo. À medida que se aproxima da entrada, ouve o som de passos atrás de você.

"Espere, viajante," diz uma voz. Virando-se, você vê um homem idoso com vestes ornamentadas. "Poucos estrangeiros visitam este templo. O que o traz aqui?"

O homem o observa atentamente, como se pudesse ver além de sua aparência física.""",
        "choices": [
            {
                "text": "Dizer a verdade sobre sua situação",
                "next_node": "honest_explanation"
            },
            {
                "text": "Dizer que é apenas um viajante curioso",
                "next_node": "traveler_story"
            },
            {
                "text": "Perguntar quem ele é antes de responder",
                "next_node": "ask_about_priest"
            }
        ]
    },

    "axe_touch_success": {
        "title": "Conexão com o Trovão",
        "text": """Com determinação, você estende a mão e toca o machado cerimonial. No instante em que seus dedos entram em contato com o metal, uma sensação eletrizante percorre seu corpo.

Visões relâmpago inundam sua mente: tempestades rugindo sobre planícies, uma cidade ancestral com torres douradas, um rei empunhando o machado contra inimigos, e finalmente uma figura majestosa observando a Terra de um trono entre as nuvens.

Quando a visão termina, você percebe que entende instintivamente mais sobre Sango e seu papel no panteão Yorùbá. O machado transmitiu conhecimento diretamente à sua mente.

Algo também mudou dentro de você - uma conexão foi estabelecida. Você sente uma nova confiança e força interior, como se tivesse recebido a bênção do próprio Sango.""",
        "choices": [
            {
                "text": "Agradecer em voz alta a Sango pela visão",
                "next_node": "thank_sango"
            },
            {
                "text": "Procurar por alguém no templo para compartilhar sua experiência",
                "next_node": "meet_priest"
            },
            {
                "text": "Deixar o templo com seu novo conhecimento",
                "next_node": "temple_exit_enlightened"
            }
        ]
    },

    "axe_touch_failure": {
        "title": "A Ira do Trovão",
        "text": """Ao tocar o machado cerimonial, você sente imediatamente que cometeu um erro. Uma forte descarga elétrica percorre seu braço, lançando-o para trás com força. Você cai no chão, atordoado, com a visão embaçada.

O ar no templo fica pesado e carregado, como antes de uma tempestade. Você ouve o som de trovão distante, apesar de estar dentro do templo, e as sombras parecem se adensar.

Lutando para se levantar, você percebe que o machado continua intacto no altar, mas agora parece irradiar uma aura de advertência. É claro que você foi considerado indigno de tocá-lo.""",
        "battle": "temple_guardian",
        "victory_node": "guardian_defeated",
        "defeat_node": "temple_expulsion"
    },

    "examine_offerings": {
        "title": "Oferendas Sagradas",
        "text": """Você examina cuidadosamente as oferendas dispostas no altar. Há frutas frescas, principalmente maçãs vermelhas e bananas; pequenas esculturas de madeira representando animais e pessoas; tigelas contendo o que parece ser mel, azeite de dendê e um tipo de bebida alcoólica.

Também há itens mais incomuns: um pequeno martelo, uma pedra com forma de ovo, e várias contas vermelhas e brancas arranjadas em padrões específicos.

Você reconhece estes como símbolos e itens tradicionais associados a Sango - o alimento e bebida para nutrir sua força, as representações de seus devotos, e os objetos que simbolizam seu domínio sobre o trovão e a justiça.""",
        "choices": [
            {
                "text": "Fazer sua própria oferenda improvisada",
                "next_node": "make_offering"
            },
            {
                "text": "Examinar o machado no altar",
                "next_node": "examine_axe"
            },
            {
                "text": "Deixar o altar e explorar o resto do templo",
                "test": "physical",
                "difficulty": 8,
                "success_node": "find_hidden_area",
                "failure_node": "meet_priest"
            }
        ]
    },

    "make_offering": {
        "title": "Oferenda Pessoal",
        "text": """Você procura entre seus pertences algo que possa servir como oferenda. De sua mochila, retira um pequeno item pessoal - talvez uma moeda de seu país, um lenço, ou outro objeto significativo.

Com reverência, coloca-o junto às outras oferendas e faz um breve momento de silêncio respeitoso. O gesto, embora simples, parece apropriado.

Após alguns instantes, você percebe uma mudança sutil no ambiente. O ar parece vibrar levemente e você ouve um som distante de trovão, apesar de estar dentro do templo. Sua oferenda foi aceita.""",
        "choices": [
            {
                "text": "Examinar o machado cerimonial agora",
                "next_node": "examine_axe_blessed"
            },
            {
                "text": "Explorar mais o templo",
                "next_node": "temple_exploration"
            }
        ]
    },

    "examine_axe_blessed": {
        "title": "O Machado e a Bênção",
        "text": """Após sua oferenda ter sido aceita, você se aproxima do machado cerimonial com nova confiança. O objeto parece diferente agora - o metal brilha mais intensamente e o zumbido elétrico que emana dele é mais forte, mas não ameaçador.

Quando estende a mão para o machado, não há hesitação. Seus dedos tocam o metal e, em vez da descarga dolorosa que muitos intrusos receberiam, você sente uma energia revigorante fluir para seu corpo.

Visões breves, mas nítidas, passam por sua mente: você vê padrões de tempestades, rituais antigos, e figuras poderosas que devem ser os Òrìṣà. O conhecimento flui diretamente para sua consciência.""",
        "choices": [
            {
                "text": "Absorver o conhecimento e aceitar a bênção",
                "next_node": "receive_blessing"
            },
            {
                "text": "Retirar a mão, temendo consequências desconhecidas",
                "next_node": "reject_power"
            }
        ]
    },

    "temple_exploration": {
        "title": "Explorando o Templo",
        "text": """Você decide explorar mais o templo de Sango. Além da sala principal com o altar, há diversos corredores e câmaras menores.

Em uma das paredes da sala principal, você nota uma porta parcialmente oculta por tecidos decorativos. Curioso, você afasta os tecidos e encontra uma passagem para uma câmara interior, iluminada por tochas.

Ao entrar, descobre uma sala circular onde as paredes são cobertas por mapas estrelares e símbolos astronômicos. No centro, há uma mesa baixa com um modelo em escala do que parece ser um sistema cosmológico yorùbá - representando a Terra, o céu, e os reinos dos Òrìṣà.""",
        "choices": [
            {
                "text": "Estudar os mapas e símbolos astronômicos",
                "test": "mental",
                "difficulty": 14,
                "success_node": "cosmic_knowledge",
                "failure_node": "partial_understanding"
            },
            {
                "text": "Examinar o modelo cosmológico",
                "next_node": "examine_cosmology"
            },
            {
                "text": "Voltar para a sala principal do templo",
                "next_node": "return_to_main_hall"
            }
        ]
    },

    "find_hidden_area": {
        "title": "A Câmara Secreta",
        "text": """Seu instinto o leva a investigar as paredes do templo. Observando atentamente, você nota uma sutil diferença na textura de uma seção da parede atrás de uma tapeçaria. Afastando o tecido, encontra uma pequena porta secreta.

Com cuidado, você abre a porta e encontra uma escada estreita que desce para uma câmara subterrânea. Descendo lentamente, chega a uma sala circular iluminada por cristais estranhos que emitem um brilho azulado.

A sala contém estantes com papiros e objetos antigos, e no centro há uma mesa com um grande mapa entalhado na pedra, mostrando toda a região de Yorùbáland com marcações em locais específicos.""",
        "choices": [
            {
                "text": "Examinar os papiros e objetos",
                "test": "mental",
                "difficulty": 12,
                "success_node": "ancient_knowledge",
                "failure_node": "confusing_documents"
            },
            {
                "text": "Estudar o mapa com atenção",
                "next_node": "sacred_map"
            },
            {
                "text": "Retornar ao templo principal",
                "next_node": "temple_respect"
            }
        ]
    },

    "meet_priest": {
        "title": "O Sacerdote de Sango",
        "text": """O homem idoso se aproxima de você com passos deliberados. Suas vestes elaboradas são predominantemente vermelhas e brancas, decoradas com símbolos que representam raios e trovões. Ao redor de seu pescoço pende um colar de contas coloridas, e ele carrega um cajado ornamentado com símbolos esculpidos.

"Eu sou Adewale, sumo sacerdote de Sango neste templo," ele diz, estudando seu rosto. "Poucos estrangeiros encontram este lugar, e menos ainda são permitidos entrar por Sango. Você deve ter um propósito especial aqui."

Seus olhos são perspicazes e parecem enxergar além de sua aparência física, como se avaliasse sua essência.""",
        "choices": [
            {
                "text": "Contar a verdade sobre sua situação e o amuleto",
                "next_node": "truth_to_priest"
            },
            {
                "text": "Perguntar sobre o templo e seu significado",
                "next_node": "ask_about_temple"
            },
            {
                "text": "Perguntar sobre os estranhos eventos que tem testemunhado",
                "next_node": "ask_about_events"
            }
        ]
    },

    "truth_to_priest": {
        "title": "Revelações ao Sacerdote",
        "text": """Você decide que a honestidade é o melhor caminho e conta sua história completa a Adewale - como você veio de outro tempo através do amuleto que tocou em uma escavação arqueológica.

O sacerdote ouve atentamente, sem interromper. Seus olhos se arregalam quando você menciona o amuleto, e ele pede para vê-lo. Quando você mostra o objeto, Adewale solta uma exclamação de surpresa.

"O Amuleto de Ashe," ele sussurra. "Uma relíquia sagrada perdida há gerações. Ele permite que seu portador canalize o ashe - a energia vital que flui entre todos os reinos." Ele levanta os olhos para você. "Você foi trazido aqui por um propósito. Os Òrìṣà não fazem nada sem razão."

Ele parece considerar algo por um momento antes de tomar uma decisão.""",
        "choices": [
            {
                "text": "Perguntar qual seria esse propósito",
                "next_node": "ask_about_purpose"
            },
            {
                "text": "Pedir ajuda para voltar ao seu próprio tempo",
                "next_node": "ask_help_return"
            },
            {
                "text": "Perguntar sobre o Amuleto de Ashe e seus poderes",
                "next_node": "ask_about_amulet_powers"
            }
        ]
    },

    "ask_about_temple": {
        "title": "O Templo de Sango",
        "text": """Você pergunta a Adewale sobre o templo e seu significado. O sacerdote sorri, aparentemente satisfeito com seu interesse.

"Este é o Templo Principal de Sango na região," ele explica. "Foi construído há sete gerações, após uma grande tempestade devastar nossa aldeia. O povo interpretou a tempestade como um sinal da ira de Sango e ergueu este templo para apaziguá-lo."

"Sango é o Òrìṣà do trovão, do fogo e da justiça. Era o quarto rei de Oyo antes de sua ascensão divina. Aqui realizamos rituais para pedir sua proteção, sua justiça e sua orientação." Ele faz um gesto em direção ao altar. "O machado de bronze é seu símbolo principal, representando o poder do trovão e o julgamento implacável sobre os injustos."

Adewale o observa com curiosidade. "Mas você não é daqui. Como veio parar em nosso templo?".""",
        "choices": [
            {
                "text": "Contar a verdade sobre sua origem e o amuleto",
                "next_node": "truth_to_priest"
            },
            {
                "text": "Dizer que é apenas um viajante curioso",
                "test": "mental",
                "difficulty": 12,
                "success_node": "convince_priest_traveler",
                "failure_node": "priest_suspicious"
            },
            {
                "text": "Perguntar sobre os outros Òrìṣà",
                "next_node": "ask_about_orishas"
            }
        ]
    },

    "ask_about_events": {
        "title": "Eventos Misteriosos",
        "text": """Você pergunta a Adewale sobre os estranhos eventos que tem testemunhado desde sua chegada - o portal, o amuleto, as visões, a capacidade de entender um idioma que nunca estudou.

O sacerdote ouve com atenção crescente, e seu rosto se torna mais sério a cada detalhe que você compartilha. Quando você termina, ele permanece em silêncio por alguns momentos.

"Os sinais são claros," ele finalmente diz. "Os Òrìṣà trouxeram você aqui. Não é coincidência que você possa entender nossa língua ou que o templo o tenha admitido. E este amuleto..." Ele faz um gesto para que você o mostre. Quando você revela o objeto, ele assente gravemente.

"O Amuleto de Ashe, um artefato sagrado que se acreditava perdido. Ele conecta os reinos dos homens e dos Òrìṣà. Sua chegada aqui, com este amuleto, sugere que uma grande perturbação está ocorrendo - ou irá ocorrer - no equilíbrio entre os mundos."

Ele se aproxima mais de você. "Você deve me contar exatamente como chegou aqui.".""",
        "choices": [
            {
                "text": "Contar detalhadamente sobre a escavação arqueológica e o portal",
                "next_node": "explain_arrival"
            },
            {
                "text": "Perguntar que tipo de perturbação poderia estar ocorrendo",
                "next_node": "ask_about_disturbance"
            },
            {
                "text": "Perguntar como voltar para casa",
                "next_node": "ask_help_return"
            }
        ]
    },

    "ask_about_purpose": {
        "title": "O Propósito Divino",
        "text": """Você pergunta a Adewale qual poderia ser o propósito dos Òrìṣà ao trazê-lo para este tempo e lugar.

O sacerdote caminha lentamente até uma parede do templo onde há um mural elaborado. Ele aponta para uma seção que mostra figuras sombrias emergindo de uma fenda no céu, enquanto as divindades Yorùbá formam uma barreira protetora.

"Existe uma antiga profecia," ele explica, "que fala de um tempo em que as barreiras entre os mundos ficariam enfraquecidas. Quando isso acontecesse, forças do caos tentariam invadir nosso reino." Ele toca o mural onde uma figura segura um objeto que se parece notavelmente com seu amuleto.

"A profecia também menciona um viajante de terras além do conhecimento, que carregaria o Amuleto de Ashe e ajudaria a restaurar o equilíbrio." Ele se vira para você com um olhar penetrante. "Recentemente, temos observado sinais preocupantes. Tempestades anormais. Avistamentos de criaturas estranhas nas florestas. E agora, você chega."

"Acredito que você foi trazido para nos ajudar a prevenir uma catástrofe."
""",
        "choices": [
            {
                "text": "Perguntar como poderia ajudar a prevenir essa catástrofe",
                "next_node": "hero_mission"
            },
            {
                "text": "Expressar ceticismo quanto a ser um escolhido de uma profecia",
                "next_node": "skeptical_response"
            },
            {
                "text": "Perguntar mais detalhes sobre as forças do caos mencionadas",
                "next_node": "chaos_forces"
            }
        ]
    },

    "ask_help_return": {
        "title": "O Caminho de Volta",
        "text": """Você pergunta a Adewale se ele pode ajudá-lo a retornar ao seu próprio tempo. O sacerdote considera sua pergunta com seriedade.

"O Amuleto de Ashe abriu o caminho que o trouxe até aqui," ele diz após alguns momentos. "Em teoria, ele poderia levá-lo de volta. Mas tais viagens não são simples nem sem propósito."

Ele toca levemente o amuleto em seu pescoço. "Este artefato é uma relíquia sagrada de Orunmila, o Òrìṣà da sabedoria e da adivinhação. Ele não o teria trazido aqui sem um motivo importante."

O olhar de Adewale se torna distante, como se contemplasse algo além das paredes do templo. "Há perturbações no equilíbrio entre os reinos. Sinais que os sacerdotes de todos os quatro grandes Òrìṣà têm observado com preocupação." Ele volta a focar em você.

"Acredito que você só poderá retornar ao seu tempo quando cumprir o propósito pelo qual foi trazido."
""",
        "choices": [
            {
                "text": "Perguntar qual seria esse propósito",
                "next_node": "ask_about_purpose"
            },
            {
                "text": "Pedir para aprender mais sobre o amuleto e como usá-lo",
                "next_node": "learn_about_amulet"
            },
            {
                "text": "Oferecer sua ajuda para resolver as perturbações mencionadas",
                "next_node": "offer_help"
            }
        ]
    },

    "learn_about_amulet": {
        "title": "Os Segredos do Amuleto",
        "text": """Você pede a Adewale para lhe ensinar mais sobre o Amuleto de Ashe e como utilizá-lo. O sacerdote faz um gesto para que você o siga até uma sala adjacente do templo.

A sala é menor e iluminada por velas de óleo que emitem uma luz dourada. Nas paredes há diversos símbolos e diagramas pintados que parecem mapear conexões entre diferentes reinos ou dimensões.

"O Amuleto de Ashe é um dos quatro grandes artefatos criados pelos primeiros sacerdotes de Yorùbáland," explica Adewale, indicando um desenho na parede que mostra quatro objetos dispostos em um círculo. "Cada um está conectado a um dos principais Òrìṣà: Sango, Ogun, Yemoja e Osun."

Ele toca suavemente o amuleto em seu pescoço. "Este, em particular, serve como um condutor do ashe – a força vital universal. Em mãos treinadas, pode abrir portais entre mundos, conceder visões do futuro e do passado, e até mesmo amplificar os dons naturais de seu portador."

Adewale se senta em uma esteira no chão e indica para que você faça o mesmo. "Posso ensiná-lo a canalizar o poder do amuleto, mas deve entender que tal conhecimento vem com responsabilidade. Os Òrìṣà não concedem tais dons sem expectativa de que sejam usados com sabedoria."
""",
        "choices": [
            {
                "text": "Aceitar o treinamento para usar o amuleto",
                "next_node": "amulet_training"
            },
            {
                "text": "Perguntar sobre os outros três artefatos",
                "next_node": "four_artifacts"
            },
            {
                "text": "Perguntar sobre os perigos de usar tal poder",
                "next_node": "amulet_dangers"
            }
        ]
    },

    "offer_help": {
        "title": "Oferecendo Assistência",
        "text": """Você diz a Adewale que está disposto a ajudar a resolver as perturbações mencionadas. O rosto do sacerdote se ilumina com um sorriso.

"Eu sabia que os Òrìṣà escolheram bem," ele diz com aprovação. "Sua disposição honra seus ancestrais, mesmo que eles ainda não tenham nascido em seu tempo."

Adewale caminha até um baú ornamentado no canto da sala e retira um pergaminho envelhecido. Desenrolando-o sobre uma mesa baixa, revela um mapa da região de Yorùbáland, com quatro locais marcados em símbolos diferentes.

"Estes são os quatro templos principais, cada um dedicado a um dos grandes Òrìṣà," explica ele, apontando para os símbolos. "Estamos aqui, no Templo de Sango. Os outros são o Templo de Ogun nas montanhas de ferro, o Templo de Yemoja junto ao grande rio, e o Templo de Osun na floresta sagrada."

Seu dedo traça uma linha entre os quatro pontos, formando um quadrado. "Juntos, eles mantêm o equilíbrio espiritual de nossa terra. Mas recebi notícias perturbadoras dos outros templos. Artefatos sagrados foram roubados de cada um, enfraquecendo a barreira entre os mundos."

Ele olha gravemente para você. "Acredito que você foi enviado para nos ajudar a recuperá-los antes que seja tarde demais."
""",
        "choices": [
            {
                "text": "Perguntar quem poderia estar roubando os artefatos",
                "next_node": "ask_about_thief"
            },
            {
                "text": "Oferecer-se para recuperar os artefatos",
                "next_node": "accept_quest"
            },
            {
                "text": "Perguntar como os artefatos mantêm o equilíbrio",
                "next_node": "artifacts_purpose"
            }
        ]
    },

    "hero_mission": {
        "title": "A Missão do Herói",
        "text": """Você pergunta a Adewale como poderia ajudar a prevenir a catástrofe que ele teme estar se aproximando.

O sacerdote o conduz para uma câmara interna do templo, onde um grande mapa de Yorùbáland está pintado em uma mesa de pedra. Ele indica quatro locais marcados com símbolos distintos.

"Estes são os quatro templos principais de nossa terra, cada um guardião de um artefato sagrado que, juntos, mantêm a barreira entre os mundos," explica ele. "O Machado de Sango, a Espada de Ogun, o Cálice de Yemoja e o Espelho de Osun."

Seu rosto se torna sombrio quando continua: "Nas últimas luas, três desses artefatos foram roubados por Adigun, um sacerdote exilado que busca romper a barreira e liberar poderes caóticos em nosso mundo. Apenas o Machado de Sango permanece seguro, aqui neste templo."

Adewale toca o amuleto em seu pescoço. "Seu Amuleto de Ashe pode detectar os outros artefatos e, em mãos dignas, neutralizar o ritual que Adigun pretende realizar. Você deve recuperar os artefatos roubados antes que ele colete o último e complete seu plano."

Uma responsabilidade enorme pesa sobre seus ombros enquanto você considera as palavras do sacerdote.""",
        "choices": [
            {
                "text": "Aceitar a missão para salvar Yorùbáland",
                "next_node": "accept_hero_role"
            },
            {
                "text": "Pedir mais informações sobre Adigun e seus motivos",
                "next_node": "about_adigun"
            },
            {
                "text": "Perguntar se haverá alguém para ajudá-lo nesta missão",
                "next_node": "ask_about_allies"
            }
        ]
    },

    "skeptical_response": {
        "title": "Dúvidas Razoáveis",
        "text": """Você expressa seu ceticismo quanto a ser algum tipo de escolhido profético. Afinal, você é apenas um pesquisador que tocou um artefato estranho e acabou em outro tempo - não um herói de lendas.

Adewale não parece ofendido com sua hesitação. Ao contrário, ele assente compreensivamente.

"A dúvida é natural, e talvez até saudável," ele diz. "Os maiores heróis de nossas histórias raramente começaram acreditando em seu próprio destino. Foi sua disposição para agir, apesar das dúvidas, que os definiu."

Ele caminha até uma pequena mesa e pega um objeto coberto por um pano. Ao remover o tecido, revela um pequeno dispositivo circular com engrenagens e símbolos entalhados.

"Este é um oráculo de Ifa, usado para comunicação com Orunmila, o Òrìṣà da sabedoria e adivinhação." Ele manipula o dispositivo, que emite um suave brilho azulado. "Permita-me consultar os oráculos sobre sua chegada."

Adewale realiza um breve ritual, lançando pequenas conchas sobre o dispositivo. Os padrões formados parecem significativos para ele, pois seu rosto se torna sério enquanto os estuda.""",
        "choices": [
            {
                "text": "Perguntar o que os oráculos revelaram",
                "next_node": "oracle_revelation"
            },
            {
                "text": "Admitir que talvez haja algo maior acontecendo",
                "next_node": "accepting_destiny"
            },
            {
                "text": "Manter o ceticismo, mas oferecer ajuda de qualquer forma",
                "next_node": "skeptical_helper"
            }
        ]
    },

    "chaos_forces": {
        "title": "As Forças do Caos",
        "text": """Você pede a Adewale que explique mais sobre as forças do caos mencionadas na profecia. O sacerdote olha ao redor, como se verificando que estão sozinhos, antes de falar em voz mais baixa.

"Além do mundo dos homens e do reino dos Òrìṣà, existe um terceiro domínio," ele começa. "Um lugar de energia bruta e caótica, habitado por entidades que não são nem mortais nem divinas. Nós as chamamos de Ajoguns - forças de destruição, doença e desordem."

Adewale conduz você a uma seção do templo onde as pinturas murais mostram criaturas perturbadoras - figuras distorcidas com múltiplos membros, olhos em lugares errados, e corpos que parecem violar as leis da natureza.

"Os Ajoguns invejam tanto a ordem do mundo dos Òrìṣà quanto a liberdade do mundo mortal. Eles constantemente buscam brechas na barreira que separa os reinos." Ele aponta para uma pintura mostrando quatro objetos formando um círculo protetor. "Por milênios, os quatro artefatos sagrados mantiveram essa barreira intacta."

O sacerdote se vira para encará-lo com expressão grave. "Mas agora, três dos artefatos foram roubados. A barreira enfraquece a cada dia. Se o último for tomado... os Ajoguns invadir
ão nosso mundo, trazendo caos e sofrimento imensuráveis.""",
        "choices": [
            {
                "text": "Perguntar quem roubou os artefatos",
                "next_node": "artifacts_thief"
            },
            {
                "text": "Perguntar como você pode ajudar a recuperá-los",
                "next_node": "recover_artifacts"
            },
            {
                "text": "Perguntar se os Ajoguns podem ser combatidos diretamente",
                "next_node": "fighting_ajoguns"
            }
        ]
    },

    "artifacts_thief": {
        "title": "O Ladrão de Artefatos",
        "text": """Você pergunta a Adewale quem poderia estar roubando os artefatos sagrados. O sacerdote suspira profundamente, seu rosto mostrando uma mistura de raiva e tristeza.

"Seu nome é Adigun," ele responde. "Um dos nossos, outrora. Foi um sacerdote promissor, talentoso em rituais e na comunicação com os Òrìṣà. Ele serviu no Templo de Yemoja por muitos anos."

Adewale caminha até um pequeno baú, de onde retira um pedaço de pano dobrado. Ao abri-lo, revela um desenho de um homem jovem com marcas rituais no rosto e um olhar intenso.

"Adigun acreditava que os Òrìṣà haviam se tornado distantes demais de nosso povo. Ele começou a estudar rituais proibidos, buscando formas de convocar os deuses à força, em vez de reverenciá-los propriamente." O sacerdote dobra o pano novamente. "Quando foi descoberto, o Conselho dos Sacerdotes o exilou para as terras do norte."

"Agora ele retornou, não para adorar os Òrìṣà, mas para liberar os Ajoguns. Ele acredita que o caos purificará nosso mundo e forçará os Òrìṣà a intervir diretamente. Uma loucura perigosa."

O rosto de Adewale se endurece. "Ele já roubou a Espada de Ogun, o Cálice de Yemoja e o Espelho de Osun. Apenas o Machado de Sango permanece, protegido neste templo."
""",
        "choices": [
            {
                "text": "Perguntar onde Adigun poderia estar escondido",
                "next_node": "adigun_hideout"
            },
            {
                "text": "Oferecer-se para ajudar a recuperar os artefatos",
                "next_node": "accept_quest"
            },
            {
                "text": "Perguntar se há outros que seguem Adigun",
                "next_node": "adigun_followers"
            }
        ]
    },

    "recover_artifacts": {
        "title": "A Recuperação dos Artefatos",
        "text": """Você pergunta a Adewale como poderia ajudar a recuperar os artefatos roubados. O sacerdote parece aliviado com sua disposição.

"Os três artefatos roubados estão sendo mantidos em locais diferentes," explica ele, desenrolando um mapa sobre uma mesa. "Adigun é astuto - escondeu cada um em um lugar onde sua energia seria mascarada por energias naturais semelhantes."

Ele aponta para três locais no mapa. "A Espada de Ogun está escondida nas Montanhas de Ferro ao norte, onde os depósitos minerais confundem sua presença. O Cálice de Yemoja está submerso no Lago da Lua a leste, suas águas protegidas por criaturas encantadas. E o Espelho de Osun foi levado para a Floresta dos Sussurros ao sul, onde ilusões e encantos protegem seus segredos."

Adewale olha para você com seriedade. "Recuperar todos os três antes do próximo eclipse lunar - daqui a sete dias - é essencial. Nessa noite, Adigun pretenderá vir até este templo para roubar o Machado de Sango e completar seu ritual."

"Seu Amuleto de Ashe será fundamental nesta missão. Ele pode sentir a presença dos artefatos e neutralizar algumas das proteções mágicas que Adigun colocou ao seu redor."
""",
        "choices": [
            {
                "text": "Perguntar qual artefato deve ser recuperado primeiro",
                "next_node": "quest_priority"
            },
            {
                "text": "Perguntar se haverá alguém para ajudá-lo",
                "next_node": "ask_about_allies"
            },
            {
                "text": "Pedir informações específicas sobre as defesas de cada local",
                "next_node": "artifacts_defenses"
            }
        ]
    },

    "fighting_ajoguns": {
        "title": "Combatendo as Entidades do Caos",
        "text": """Você pergunta se os Ajoguns podem ser combatidos diretamente, caso consigam invadir Yorùbáland. A expressão de Adewale se torna sombria.

"Teoricamente, sim," ele responde com hesitação. "Mas não seria como lutar contra inimigos mortais. Os Ajoguns são manifestações de conceitos - doença, loucura, destruição. Eles não seguem as leis físicas como nós."

O sacerdote caminha até um armário trancado e o abre com uma pequena chave que carrega ao pescoço. De dentro, retira uma pequena adaga com lâmina ondulada e inscrições brilhantes.

"Armas comuns têm pouco efeito sobre eles. Apenas instrumentos infundidos com ashe - a energia vital dos Òrìṣà - podem realmente feri-los." Ele segura a adaga com reverência. "Esta é uma das poucas armas assim que possuímos, forjada com a bênção de Ogun."

Adewale guarda a adaga novamente. "Mas mesmo com tais armas, o combate direto seria desastroso. Sua presença física no nosso mundo causaria distorções na realidade. Plantas murchariam, animais enlouqueceriam, pessoas adoeceriam apenas por estarem próximas."

"É por isso que devemos a todo custo impedir que a barreira entre os mundos seja rompida. A prevenção é nossa única esperança real."
""",
        "choices": [
            {
                "text": "Perguntar se há outros métodos de defesa além das armas",
                "next_node": "spiritual_defenses"
            },
            {
                "text": "Oferecer sua ajuda para impedir Adigun",
                "next_node": "accept_quest"
            },
            {
                "text": "Perguntar se há registros de invasões anteriores dos Ajoguns",
                "next_node": "previous_incursions"
            }
        ]
    },

    "ask_about_thief": {
        "title": "O Inimigo Revelado",
        "text": """Você pergunta a Adewale quem poderia estar roubando os artefatos sagrados. O sacerdote fecha os olhos brevemente, como se a resposta lhe causasse dor.

"Seu nome é Adigun," ele diz finalmente. "Foi um de nós, um sacerdote altamente talentoso do Templo de Yemoja. Era considerado um prodígio, com habilidade rara para comungar com os Òrìṣà."

Adewale se levanta e caminha até um pequeno nicho na parede, de onde retira um pequeno medalhão. Abrindo-o, mostra a você um retrato miniatura de um homem jovem com traços severos e olhos penetrantes.

"Adigun acreditava que nossa conexão com os Òrìṣà estava enfraquecendo por seguirmos tradições muito rígidas. Ele buscava meios mais diretos de comunicação com o divino." O sacerdote fecha o medalhão. "Com o tempo, suas ideias se tornaram cada vez mais extremas. Ele começou a experimentar com rituais proibidos, buscando forçar manifestações dos Òrìṣà."

"Quando descobrimos seus experimentos, ele já havia se corrompido. O Conselho dos Sacerdotes o exilou. Juramos que ele nunca mais seria aceito em nenhum templo." Adewale suspira profundamente. "Acreditávamos que ele havia partido para terras distantes, mas agora retornou com um propósito terrível."

"Adigun não busca mais comungar com os Òrìṣà - ele pretende romper completamente a barreira entre os mundos, permitindo que os Ajoguns, entidades do caos, invadam Yorùbáland."
""",
        "choices": [
            {
                "text": "Perguntar onde Adigun poderia estar escondido",
                "next_node": "adigun_location"
            },
            {
                "text": "Perguntar por que ele quer liberar os Ajoguns",
                "next_node": "adigun_motives"
            },
            {
                "text": "Oferecer-se para recuperar os artefatos roubados",
                "next_node": "accept_quest"
            }
        ]
    },

    "accept_quest": {
        "title": "O Chamado da Aventura",
        "text": """Você toma sua decisão e diz a Adewale que está disposto a ajudar a recuperar os artefatos sagrados. O sacerdote sorri com aprovação.

"Seu coração é valoroso," ele diz. "Talvez seja este o motivo pelo qual os Òrìṣà o trouxeram até nós." 

Ele se dirige a um baú ornamentado no canto da sala e retira alguns itens: um pequeno saco de couro contendo ervas e pós coloridos, um colar com contas vermelhas e brancas, e uma pequena adaga cerimonial.

"Estes itens o ajudarão em sua jornada," explica, entregando-os a você. "As ervas têm propriedades curativas e podem ser usadas em rituais de proteção. O colar é uma benção de Sango e o protegerá de alguns perigos espirituais. A adaga foi consagrada para afetar entidades que armas comuns não conseguem tocar."

Adewale desenrola um mapa antigo sobre uma mesa baixa. "Sugiro que comece pelo Templo de Ogun nas Montanhas de Ferro. A Espada sagrada pode ser a mais fácil de recuperar, e lhe dará força para os desafios seguintes."

Ele marca três locais no mapa com símbolos diferentes. "Não tenho como saber exatamente quais perigos você enfrentará. Adigun tem seguidores e, provavelmente, proteções mágicas guardando os artefatos. Use o Amuleto de Ashe para guiá-lo - ele responderá à presença dos outros artefatos."
""",
        "choices": [
            {
                "text": "Pedir mais orientações sobre como usar o amuleto",
                "next_node": "amulet_guidance"
            },
            {
                "text": "Perguntar sobre possíveis aliados na jornada",
                "next_node": "ask_about_allies"
            },
            {
                "text": "Partir imediatamente para as Montanhas de Ferro",
                "next_node": "iron_mountains_journey"
            }
        ]
    },

    "adigun_location": {
        "title": "O Esconderijo do Inimigo",
        "text": """Você pergunta a Adewale se ele sabe onde Adigun poderia estar escondido. O sacerdote franze a testa, pensativo.

"Não temos certeza da localização exata," ele admite. "Mas nossos batedores relataram atividades estranhas nas ruínas do antigo templo abandonado, no centro da Floresta Proibida."

Ele se aproxima do mapa na parede e indica um ponto distante, marcado com um símbolo obscurecido. "Este local foi um grande templo há séculos, dedicado a todos os Òrìṣà. Foi abandonado após um terrível desastre - dizem que um ritual falhou e abriu brevemente um portal para o reino dos Ajoguns."

Adewale traça um círculo ao redor da área com seu dedo. "A floresta ao redor se tornou corrupta, com plantas estranhas e criaturas anormais. Poucos ousam se aventurar lá. Seria o esconderijo perfeito para Adigun - um local já imbuído com energia caótica que mascara seus rituais."

"Acreditamos que ele só deixará seu esconderijo na noite do eclipse lunar, para tentar roubar o Machado de Sango. É quando a barreira entre os mundos estará naturalmente mais fina, facilitando seu ritual final."

Ele olha para você com seriedade. "Confrontá-lo diretamente seria extremamente perigoso. Nossa melhor esperança é recuperar os artefatos antes que ele complete seu plano."
""",
        "choices": [
            {
                "text": "Oferecer-se para recuperar os artefatos",
                "next_node": "accept_quest"
            },
            {
                "text": "Perguntar sobre as defesas que Adigun pode ter",
                "next_node": "adigun_defenses"
            },
            {
                "text": "Sugerir um ataque ao esconderijo de Adigun",
                "next_node": "attack_suggestion"
            }
        ]
    },

    "adigun_motives": {
        "title": "O Plano Sinistro",
        "text": """Você pergunta a Adewale por que Adigun desejaria liberar os Ajoguns, forças de destruição, em Yorùbáland. O sacerdote fecha os olhos brevemente, como se organizando pensamentos dolorosos.

"É uma mistura de amargura, orgulho ferido e uma visão distorcida de salvação," ele explica. "Quando Adigun foi exilado, jurou que provaria estar certo - que nossos métodos de adoração eram insuficientes."

Adewale caminha até uma janela e olha para o céu. "Durante seu exílio, encontrou textos antigos que falavam dos Ajoguns não apenas como forças de destruição, mas como catalisadores de renovação." 

"Ele passou a acreditar que nosso mundo se tornou estagnado e corrupto. Que os Òrìṣà se afastaram por estarmos muito confortáveis em nossas tradições." O sacerdote se vira para você com expressão grave. "Adigun acredita que liberando os Ajoguns, forçará os Òrìṣà a intervir diretamente no mundo mortal."

"Em sua mente perturbada, ele se vê como um salvador, não como um destruidor. Acredita que das cinzas do caos surgirá um mundo novo, onde os Òrìṣà caminharão entre os mortais novamente."

"É claro que está enganado. Os Ajoguns não são forças de renovação controlável - são manifestações de princípios caóticos que destruiriam tudo, sem discriminação ou propósito."
""",
        "choices": [
            {
                "text": "Perguntar se há chances de fazer Adigun mudar de ideia",
                "next_node": "redemption_possibility"
            },
            {
                "text": "Oferecer-se para recuperar os artefatos",
                "next_node": "accept_quest"
            },
            {
                "text": "Perguntar como Adigun planeja realizar seu ritual",
                "next_node": "ritual_details"
            }
        ]
    },

    "iron_mountains_journey": {
        "title": "Jornada às Montanhas de Ferro",
        "text": """Você decide partir imediatamente para as Montanhas de Ferro. Adewale providencia mantimentos para sua jornada e um guia para levá-lo até os pés das montanhas.

A viagem leva dois dias. No primeiro, atravessam vastas planícies de savana, com grama dourada ondulando ao vento. No segundo, a paisagem gradualmente muda para colinas pedregosas que anunciam a proximidade das montanhas.

Seu guia, um homem chamado Babatunde, é quieto mas observador. Ao fim do segundo dia, ele para em uma pequena aldeia aos pés das montanhas. "Daqui em diante você deve seguir sozinho," ele explica. "O Templo de Ogun está no coração das montanhas, e apenas aqueles chamados a enfrentar seu desafio podem encontrar o caminho."

Ele aponta para uma trilha que serpenteia montanha acima. "Siga este caminho até encontrar dois pilares de pedra. A partir dali, deixe que o amuleto o guie - ele responderá à presença da Espada de Ogun."

Antes de partir, Babatunde lhe entrega um pequeno martelo de ferreiro. "Um símbolo de Ogun, o senhor do ferro e da forja. Mostre-o com respeito quando entrar em seu domínio."

Na manhã seguinte, você inicia sua subida pelas Montanhas de Ferro, cujos picos avermelhados parecem tingidos pelo metal que lhes dá o nome.""",
        "choices": [
            {
                "text": "Seguir a trilha em direção aos pilares de pedra",
                "next_node": "iron_pillars"
            },
            {
                "text": "Tentar usar o amuleto para sentir a direção da Espada",
                "test": "spiritual",
                "difficulty": 12,
                "success_node": "amulet_guidance_success",
                "failure_node": "amulet_guidance_failure"
            },
            {
                "text": "Observar cuidadosamente os arredores em busca de perigos",
                "test": "mental",
                "difficulty": 10,
                "success_node": "notice_followers",
                "failure_node": "continue_unaware"
            }
        ]
    },

    "ask_about_allies": {
        "title": "Possíveis Aliados",
        "text": """Você pergunta a Adewale se haverá alguém para ajudá-lo em sua perigosa missão. O sacerdote considera a questão por um momento.

"Não posso deixar o templo desprotegido, especialmente agora que o Machado de Sango é o último artefato restante," ele explica. "Mas há outros que podem auxiliá-lo."

Adewale escreve algumas notas em pequenos pedaços de pergaminho e os sela com cera vermelha. "Em cada local que você visitar, haverá aliados em potencial. Em Ife, próximo às Montanhas de Ferro, procure por Babajide, um ferreiro e devoto de Ogun. Ele conhece bem as montanhas e respeita a Espada."

Ele entrega outro pergaminho. "Próximo ao Lago da Lua, na aldeia de pescadores, procure por Folami. Ela é uma sacerdotisa de Yemoja e sentiu a perturbação quando o Cálice foi roubado."

Um terceiro pergaminho é selado com cuidado especial. "Na floresta dos Sussurros, será mais difícil. Há um eremita chamado Tunde que habita lá. Ele é... peculiar, mas conhece cada árvore e cada espírito daquela floresta. Estas cartas identificarão você como meu emissário."

Adewale coloca uma mão em seu ombro. "Lembre-se: mesmo com aliados, a responsabilidade principal é sua. O Amuleto de Ashe respondeu a você, não a eles."
""",
        "choices": [
            {
                "text": "Agradecer e partir para as Montanhas de Ferro",
                "next_node": "iron_mountains_journey"
            },
            {
                "text": "Perguntar se há outros sacerdotes que poderiam ajudar",
                "next_node": "other_priests"
            },
            {
                "text": "Pedir mais detalhes sobre os perigos específicos de cada local",
                "next_node": "location_dangers"
            }
        ]
    },

    "other_priests": {
        "title": "Os Sacerdotes dos Quatro Templos",
        "text": """Você pergunta a Adewale se outros sacerdotes dos templos principais poderiam ajudar na missão. Seu rosto se entristece com a pergunta.

"Os sumos sacerdotes de Ogun, Yemoja e Osun foram capturados por Adigun quando ele roubou os artefatos," ele explica. "Acreditamos que estejam mantidos prisioneiros, forçados a auxiliar em seus rituais por seu conhecimento único."

Adewale caminha até uma prateleira e retira três amuletos diferentes: um machado miniatura, uma concha prateada e um espelho do tamanho de sua palma. "Estes são símbolos de nossos irmãos desaparecidos. Se você os encontrar, mostre-lhes estes símbolos. Eles saberão que você vem em nome do Conselho dos Sacerdotes."

"Quase todos os outros sacerdotes estão em seus respectivos templos, reforçando as proteções espirituais que ainda restam. Se abandonassem seus postos, as barreiras entre os mundos ficariam ainda mais fracas." Ele guarda os amuletos em uma pequena bolsa e a entrega a você.

"Esta é uma das razões pelas quais sua chegada é tão significativa. Um estrangeiro, não vinculado à proteção de nenhum templo específico, mas capaz de manejar o Amuleto de Ashe... os Òrìṣà certamente guiaram sua vinda."
""",
        "choices": [
            {
                "text": "Prometer encontrar e libertar os sacerdotes capturados",
                "next_node": "promise_rescue"
            },
            {
                "text": "Perguntar como reconhecerá os sacerdotes cativos",
                "next_node": "identify_priests"
            },
            {
                "text": "Agradecer pela informação e partir para as Montanhas de Ferro",
                "next_node": "iron_mountains_journey"
            }
        ]
    },

    "location_dangers": {
        "title": "Perigos nos Três Locais",
        "text": """Você pede a Adewale que detalhe os perigos específicos que poderá encontrar em cada um dos três locais. O sacerdote assente gravemente.

"As Montanhas de Ferro são habitadas por espíritos de mineradores ancestrais," ele começa. "Eles testam qualquer um que busque as bênçãos de Ogun. Além disso, há criaturas feitas de metal vivo - guardiões forjados pelo próprio Ogun para proteger seu santuário. Desde que Adigun roubou a Espada, esses guardiões se tornaram hostis a todos os visitantes."

Adewale desenha um símbolo no ar. "No Lago da Lua, as águas são habitadas por sereias que servem a Yemoja. Normalmente, elas guiam os viajantes dignos, mas com o roubo do Cálice, estão enfurecidas e desconfiadas. O próprio lago agora é perigoso - suas águas podem induzir visões e pesadelos que consomem a mente dos incautos."

"A Floresta dos Sussurros é talvez o mais perigoso dos três," ele continua com voz baixa. "É o domínio de Osun, onde a linha entre realidade e ilusão é tênue. Há árvores que se movem, caminhos que mudam, e espíritos que assumem formas familiares para enganar viajantes. Desde o roubo do Espelho, a floresta se tornou particularmente traiçoeira - as ilusões agora podem ser mortais."

Ele faz uma pausa. "E, claro, em todos os três locais, Adigun provavelmente deixou seguidores e proteções mágicas para impedir que os artefatos sejam recuperados."
""",
        "choices": [
            {
                "text": "Perguntar como superar esses perigos específicos",
                "next_node": "danger_solutions"
            },
            {
                "text": "Pedir itens ou proteções adicionais para cada lugar",
                "next_node": "request_protections"
            },
            {
                "text": "Agradecer pelo aviso e partir para as Montanhas de Ferro",
                "next_node": "iron_mountains_journey"
            }
        ]
    },

    "iron_pillars": {
        "title": "Os Pilares de Ferro",
        "text": """Após algumas horas de subida íngreme pela trilha montanhosa, você finalmente avista os dois pilares de pedra mencionados por Babatunde. São estruturas imponentes, com cerca de quatro metros de altura, esculpidas diretamente da rocha da montanha.

Os pilares estão cobertos de símbolos antigos e, à medida que você se aproxima, percebe que não são de pedra comum - veios de metal brilhante permeiam a rocha, formando padrões que lembram ferramentas e armas. Entre os pilares, a trilha se divide em três caminhos diferentes.

O caminho da esquerda desce por um vale rochoso, com o som distante de marteladas ecoando. O caminho do meio segue por uma passagem estreita entre formações rochosas que se assemelham a fornalhas. O caminho da direita sobe ainda mais, em direção a uma área onde fumaça escura parece emanar do próprio solo.

Enquanto contempla qual direção seguir, você nota que o amuleto em seu pescoço começou a emitir um suave calor. Tocando-o, sente vibrações diferentes quando o aponta para cada um dos três caminhos.""",
        "choices": [
            {
                "text": "Seguir o caminho da esquerda, em direção ao som de marteladas",
                "next_node": "blacksmith_valley"
            },
            {
                "text": "Tomar o caminho do meio, através das formações rochosas",
                "next_node": "furnace_passage"
            },
            {
                "text": "Subir pelo caminho da direita, em direção à fumaça",
                "next_node": "smoking_peaks"
            }
        ]
    },

    "amulet_guidance_success": {
        "title": "A Orientação do Amuleto",
        "text": """Você para na trilha e segura o Amuleto de Ashe entre as mãos, concentrando-se em sua energia. Como Adewale explicou, você visualiza a Espada de Ogun, tentando estabelecer uma conexão mística entre os dois artefatos.

Por um momento, nada acontece. Então, lentamente, o amuleto começa a aquecer em suas mãos. A pedra azul em seu centro emite um brilho suave que pulsa como um batimento cardíaco. Você sente uma suave atração - o amuleto parece querer puxá-lo em uma direção específica.

Quando você se move ligeiramente para a direita da trilha, o pulsar se intensifica. Seguindo essa indicação, você descobre um caminho quase imperceptível entre as rochas, muito mais direto que a trilha principal.

O novo caminho é íngreme e desafiador, mas à medida que avança, o amuleto pulsa com mais força. Após cerca de uma hora de caminhada por este atalho, você chega a uma clareira onde dois enormes pilares de pedra se erguem, marcando a entrada para o coração das Montanhas de Ferro.

Com essa orientação sobrenatural, você poupou horas de caminhada e evitou possíveis perigos na trilha principal.""",
        "choices": [
            {
                "text": "Examinar os pilares de pedra",
                "next_node": "iron_pillars"
            },
            {
                "text": "Continuar seguindo a orientação do amuleto além dos pilares",
                "next_node": "direct_to_temple"
            },
            {
                "text": "Parar para descansar e meditar sobre a conexão com o amuleto",
                "next_node": "amulet_meditation"
            }
        ]
    },

    "amulet_guidance_failure": {
        "title": "A Conexão Incerta",
        "text": """Você segura o Amuleto de Ashe e tenta se concentrar, buscando estabelecer uma conexão com a Espada de Ogun. Fecha os olhos e visualiza o artefato perdido, tentando sentir sua presença nas montanhas.

Infelizmente, nada parece acontecer. O amuleto permanece frio e inerte em suas mãos. Você tenta diferentes abordagens - mudar sua posição, ajustar seu foco mental, até mesmo murmurar palavras de respeito aos Òrìṣà - mas a conexão não se estabelece.

Após várias tentativas frustradas, você percebe que pode não estar pronto para usar o amuleto dessa forma. Talvez seja necessário mais treinamento ou um vínculo mais profundo com o artefato. Ou talvez haja alguma interferência nas montanhas que dificulte a comunicação mística.

Com um suspiro de resignação, você guarda o amuleto e decide seguir pelo caminho convencional. A trilha serpenteia montanha acima, tornando-se cada vez mais íngreme e rochosa. Após várias horas de caminhada exaustiva, você finalmente avista dois grandes pilares de pedra marcando uma encruzilhada.""",
        "choices": [
            {
                "text": "Examinar os pilares de pedra",
                "next_node": "iron_pillars"
            },
            {
                "text": "Tentar novamente usar o amuleto agora que está mais próximo",
                "test": "spiritual",
                "difficulty": 10,
                "success_node": "second_attempt_success",
                "failure_node": "still_no_connection"
            },
            {
                "text": "Procurar sinais ou marcações no caminho que possam indicar a direção",
                "test": "mental",
                "difficulty": 12,
                "success_node": "find_hidden_markers",
                "failure_node": "no_visible_signs"
            }
        ]
    },

    "blacksmith_valley": {
        "title": "O Vale dos Ferreiros",
        "text": """Você segue o caminho da esquerda, descendo por um vale rochoso de onde vem o som rítmico de marteladas. À medida que avança, o som se torna mais claro e variado - dezenas de martelos batendo em diferentes ritmos, criando uma estranha música metálica.

O vale se abre em uma área ampla, pontilhada por forjas a céu aberto. Para sua surpresa, nenhuma delas é operada por seres humanos. Figuras humanoides feitas inteiramente de metal - algumas de ferro bruto, outras de aço polido - trabalham incansavelmente, martelando, moldando e temperando metal.

Os ferreiros metálicos parecem ignorar sua presença inicialmente. Você observa, fascinado, enquanto eles criam ferramentas, armas e objetos decorativos com habilidade sobre-humana. Alguns deles têm expressões faciais rudimentares forjadas em suas faces metálicas.

Quando você dá mais alguns passos para dentro do vale, porém, todos param simultaneamente. Dezenas de cabeças metálicas se viram em sua direção, olhos vazios fixos em você. Um silêncio tenso substitui a sinfonia de marteladas.

Uma figura mais alta que as outras, com elaborados detalhes decorativos em seu corpo metálico, se aproxima. "Quem ousa entrar no Vale de Ogun?" pergunta com uma voz que soa como metal raspando em metal.""",
        "choices": [
            {
                "text": "Mostrar o pequeno martelo de ferreiro que recebeu como símbolo",
                "next_node": "show_hammer_symbol"
            },
            {
                "text": "Explicar que busca a Espada de Ogun roubada",
                "next_node": "explain_quest"
            },
            {
                "text": "Tentar impressionar o ferreiro metálico com seu conhecimento de metalurgia",
                "test": "mental",
                "difficulty": 14,
                "success_node": "impress_smiths",
                "failure_node": "fail_to_impress"
            }
        ]
    },

    "furnace_passage": {
        "title": "A Passagem das Fornalhas",
        "text": """Você escolhe o caminho do meio, seguindo por uma passagem estreita entre formações rochosas que lembram enormes fornalhas. O ar fica mais quente à medida que você avança, e logo gotas de suor escorrem por seu rosto.

As paredes de rocha ao seu redor parecem pulsar com um brilho alaranjado, como se magma corresse por veias ocultas. O chão sob seus pés torna-se desconfortavelmente quente, e você precisa andar mais rápido para evitar que suas sandálias comecem a fumegar.

A passagem se estreita ainda mais, forçando-o a virar de lado em alguns pontos para conseguir passar. O calor se torna quase insuportável, e você começa a questionar sua escolha de caminho.

Finalmente, a passagem se abre em uma caverna circular onde o ar é surpreendentemente respirável, embora ainda quente. No centro da caverna há uma fonte de lava que jorra de uma fissura no chão, subindo alguns metros antes de cair de volta em um poço perfeitamente circular.

Ao redor da fonte, três figuras humanoides compostas inteiramente de lava se movem em um padrão circular, como se executassem uma dança lenta. A cada movimento, gotas de lava caem de seus corpos e solidificam no chão, formando padrões complexos.""",
        "choices": [
            {
                "text": "Observar a dança à distância para entender seu significado",
                "test": "mental",
                "difficulty": 12,
                "success_node": "understand_fire_dance",
                "failure_node": "miss_dance_meaning"
            },
            {
                "text": "Aproximar-se cuidadosamente da fonte de lava",
                "next_node": "approach_lava_font"
            },
            {
                "text": "Tentar comunicar-se com as criaturas de lava",
                "next_node": "address_lava_beings"
            }
        ]
    },

    "mountain_cave": {
        "title": "A Caverna Misteriosa",
        "text": """Durante sua exploração das Montanhas de Ferro, você encontra uma caverna cuja entrada é decorada com símbolos antigos. O ar que sai dela é surpreendentemente quente, e você ouve o som distante de marteladas.""",
        "choices": [
            {
                "text": "Entrar na caverna",
                "next_node": "forge_entrance"
            },
            {
                "text": "Examinar os símbolos na entrada",
                "test": "mental",
                "difficulty": 12,
                "success_node": "decipher_cave_symbols",
                "failure_node": "mysterious_symbols"
            }
        ]
    },

    "forge_entrance": {
        "title": "A Forja Ancestral",
        "text": """A caverna se abre em uma câmara impressionante. Uma forja antiga ocupa o centro do espaço, suas chamas ardendo com um brilho sobrenatural. Ferramentas e armas inacabadas cobrem as paredes.""",
        "choices": [
            {
                "text": "Aproximar-se da forja",
                "next_node": "approach_forge"
            },
            {
                "text": "Procurar por pistas da Espada",
                "test": "mental",
                "difficulty": 13,
                "success_node": "find_sword_clues",
                "failure_node": "dead_end"
            }
        ]
    },

    "decipher_cave_symbols": {
        "title": "Revelações Antigas",
        "text": """Você consegue decifrar os símbolos. Eles contam a história da forja onde Ogun criou suas primeiras ferramentas. Também mencionam uma passagem secreta que leva ao coração da montanha.""",
        "choices": [
            {
                "text": "Procurar a passagem secreta",
                "next_node": "secret_passage"
            },
            {
                "text": "Entrar pela entrada principal",
                "next_node": "forge_entrance"
            }
        ]
    },

    "mysterious_symbols": {
        "title": "Símbolos Enigmáticos",
        "text": """Os símbolos são complexos demais para seu entendimento atual. Você reconhece apenas que estão relacionados a Ogun e metalurgia.""",
        "next_node": "forge_entrance"
    },

    "smoking_peaks": {
        "title": "Os Picos Fumegantes",
        "text": """Você segue o caminho da direita, subindo ainda mais alto nas Montanhas de Ferro, em direção à área onde fumaça escura emana do solo. A trilha se torna mais íngreme e irregular, com pedras soltas que tornam cada passo um potencial perigo.

O ar fica mais rarefeito com a altitude, e a respiração se torna um pouco mais difícil. Misturado ao ar já escasso está um cheiro forte de enxofre que emana das fissuras no solo. Pequenas nuvens de fumaça cinza-escura escapam destas rachaduras, formando padrões fantasmagóricos no ar.

Após quase uma hora de subida extenuante, você chega a um platô elevado. O chão aqui é coberto por uma fina camada de cinzas, e grandes rachaduras atravessam a superfície. De algumas destas fendas, colunas mais substanciais de fumaça se elevam em direção ao céu.

No centro do platô, uma figura solitária está sentada em posição de meditação. Para sua surpresa, o ser parece ser feito inteiramente de metal escurecido pelo fogo. Seu corpo é coberto por gravuras complexas e símbolos que lembram aqueles que você viu no Templo de Sango.

A figura não se move enquanto você se aproxima, mas você tem a distinta impressão de que está plenamente ciente de sua presença.""",
        "choices": [
            {
                "text": "Aproximar-se respeitosamente e cumprimentar a figura",
                "next_node": "greet_smoking_figure"
            },
            {
                "text": "Observar à distância e estudar os símbolos gravados na figura",
                "test": "mental",
                "difficulty": 13,
                "success_node": "decipher_metal_runes",
                "failure_node": "puzzling_symbols"
            },
            {
                "text": "Perguntar sobre a Espada de Ogun",
                "next_node": "ask_about_sword"
            }
        ]
    },

    "notice_followers": {
        "title": "Olhos nas Sombras",
        "text": """Enquanto segue pela trilha montanhosa, você mantém seus sentidos alertas, constantemente observando o ambiente ao seu redor. O terreno acidentado oferece muitos lugares onde alguém poderia se esconder.

Não demora muito para que seus esforços sejam recompensados. Um movimento sutil entre as rochas - quase imperceptível - atrai sua atenção. Fingindo ajustar seu calçado, você se posiciona para observar melhor sem alertar quem quer que esteja lá.

Com o canto do olho, você percebe ao menos três figuras seguindo seus passos à distância. Eles usam capas escuras que se misturam com as sombras das rochas e se movem com a cautela de predadores. Estão claramente treinados em seguir pessoas sem serem notados.

As figuras parecem manter uma distância constante - próximas o suficiente para não perderem você de vista, mas longe o bastante para reagirem caso sejam descobertas. Seus movimentos são coordenados, sugerindo que trabalham juntos.

Em um breve momento quando o sol emerge entre as nuvens, você vê um símbolo nas capas de um deles - um círculo com uma linha diagonal, o mesmo símbolo que Adewale mencionou como sendo utilizado pelos seguidores de Adigun.""",
        "choices": [
            {
                "text": "Continuar normalmente, fingindo não tê-los notado",
                "next_node": "feign_ignorance"
            },
            {
                "text": "Preparar uma emboscada para seus perseguidores",
                "test": "physical",
                "difficulty": 14,
                "success_node": "successful_ambush",
                "failure_node": "ambush_backfires"
            },
            {
                "text": "Tentar despistá-los usando o terreno montanhoso",
                "test": "mental",
                "difficulty": 12,
                "success_node": "lose_followers",
                "failure_node": "still_following"
            }
        ]
    },

    "continue_unaware": {
        "title": "Uma Jornada Aparentemente Solitária",
        "text": """Você continua sua subida pelas Montanhas de Ferro, focado em encontrar o caminho para o templo. O terreno é desafiador, exigindo sua atenção constante - pedras soltas, passagens estreitas e ocasionais ventos fortes tornam cada passo uma consideração cuidadosa.

O som de pedras ocasionalmente caindo atrás de você parece natural neste ambiente instável. Os pássaros que levantam voo repentinamente das rochas acima provavelmente estão apenas assustados com sua presença. A sensação de ser observado, você atribui ao aspecto místico deste lugar sagrado.

Após algumas horas de caminhada, você finalmente avista os dois pilares de pedra que Babatunde mencionou. Enquanto se aproxima deles, ouve claramente o som de passos atrás de você. Antes que possa se virar, uma voz áspera ordena:

"Não se mova, estrangeiro. E não tente nada estúpido."

Três figuras emergem de trás das rochas, vestindo capas escuras com o símbolo de um círculo cortado por uma linha diagonal - o símbolo dos seguidores de Adigun. Dois deles têm adagas curvas em mãos, enquanto o terceiro segura algo que parece ser um saco de tecido.

"Sabemos por que está aqui," diz um deles. "O mestre Adigun não aprecia intromissões."
""",
        "choices": [
            {
                "text": "Tentar dialogar e descobrir mais informações",
                "next_node": "negotiate_with_followers"
            },
            {
                "text": "Atacar rapidamente antes que eles tomem a iniciativa",
                "battle": "adigun_followers",
                "victory_node": "defeat_followers",
                "defeat_node": "captured_by_followers"
            },
            {
                "text": "Usar o Amuleto de Ashe para intimidá-los",
                "test": "spiritual",
                "difficulty": 13,
                "success_node": "amulet_intimidation",
                "failure_node": "amulet_fails"
            }
        ]
    },

    "end_victory": {
        "title": "A Salvação de Yorùbáland",
        "text": """Com o último artefato recuperado, você retorna triunfante ao Templo de Sango onde os sacerdotes dos quatro Òrìṣà se reuniram. O ritual de selamento é realizado sob a luz da lua cheia.

Os artefatos sagrados são devolvidos aos seus respectivos guardiões, e o equilíbrio é restaurado em Yorùbáland. Como recompensa por seus serviços, os Òrìṣà combinam seus poderes para abrir um portal que o levará de volta ao seu próprio tempo.

Antes de partir, você é honrado como herói e amigo do povo Yorùbá. Babajide lhe entrega o Amuleto de Ashe como presente, explicando que ele servirá como conexão entre os mundos.

"Seu nome será lembrado em nossas histórias por gerações", ele diz. "E sempre que precisar da sabedoria dos Òrìṣà, o amuleto abrirá o caminho."

Você atravessa o portal, retornando exatamente ao momento e local de onde partiu, mas com conhecimentos e experiências que transformaram sua vida para sempre.""",
        "end": True
    },

    "end_emperor": {
        "title": "O Novo Imperador",
        "text": """Depois de derrotar Adigun e salvar Yorùbáland, você decide permanecer no passado. Seu conhecimento do futuro, combinado com a sabedoria que adquiriu em sua jornada, torna você um conselheiro inestimável para o rei.

Anos se passam, e sua reputação cresce. Quando o velho rei falece sem herdeiros, o conselho de sacerdotes e anciãos unanimemente o escolhe como sucessor, apesar de sua origem estrangeira.

Sob seu reinado, Yorùbáland prospera. Você introduz avanços médicos e agrícolas que salvam inúmeras vidas. Sua ligação com os Òrìṣà garante boas colheitas e paz nas fronteiras.

Os historiadores do futuro, séculos depois, encontrarão referências a um governante misterioso e poderoso, que veio de terras distantes e trouxe uma era de ouro para a civilização Yorùbá - sem nunca saber que estavam falando de você.""",
        "end": True
    },

    "moon_lake_entrance": {
        "title": "As Margens do Lago da Lua",
        "text": """Você chega às margens do lendário Lago da Lua. Suas águas são de um azul profundo e sobrenatural, refletindo o céu como um espelho perfeito. Pequenas luzes dançam sobre a superfície.""",
        "choices": [
            {
                "text": "Aproximar-se da água",
                "next_node": "water_edge"
            },
            {
                "text": "Procurar por sinais das sereias",
                "test": "spiritual",
                "difficulty": 12,
                "success_node": "mermaid_contact",
                "failure_node": "no_response"
            }
        ]
    },

    "water_edge": {
        "title": "À Beira d'Água",
        "text": """Ao se aproximar da água, você nota que ela emite um leve brilho próprio. Seu reflexo parece... diferente, como se mostrasse uma versão alternativa de você.""",
        "choices": [
            {
                "text": "Tocar a água",
                "test": "spiritual",
                "difficulty": 11,
                "success_node": "water_vision",
                "failure_node": "water_shock"
            },
            {
                "text": "Chamar pelas sereias",
                "next_node": "call_mermaids"
            }
        ]
    },

    "mermaid_contact": {
        "title": "O Chamado das Sereias",
        "text": """Uma figura graciosa emerge das águas - uma sereia com escamas que brilham como pérolas. Ela o observa com curiosidade. 'Você carrega o Amuleto de Ashe,' ela diz. 'Talvez possa nos ajudar a recuperar o Cálice.'""",
        "choices": [
            {
                "text": "Oferecer ajuda às sereias",
                "next_node": "help_mermaids"
            },
            {
                "text": "Perguntar sobre o Cálice",
                "next_node": "ask_about_chalice"
            }
        ]
    },

    "end_tragic": {
        "title": "O Preço do Fracasso",
        "text": """Apesar de seus esforços, você não consegue impedir Adigun de completar seu ritual. Com os quatro artefatos sagrados, ele abre um portal entre os mundos, permitindo que forças caóticas entrem em Yorùbáland.

O céu escurece com nuvens antinaturais, e criaturas de pesadelo emergem do portal aberto. Os sacerdotes lutam desesperadamente para conter o caos, mas é tarde demais.

Em um último ato de sacrifício, você usa o Amuleto de Ashe para tentar fechar o portal. O poder canalizado é demais para um corpo mortal suportar. Enquanto o portal começa a se fechar, você sente sua própria essência sendo dilacerada.

Seu último pensamento é a esperança de que seu sacrifício não tenha sido em vão. A última coisa que vê é Babajide tentando alcançá-lo, gritando palavras que você não consegue mais ouvir.

Historiadores e arqueólogos do futuro encontrarão registros fragmentados de um cataclismo espiritual que quase destruiu a civilização Yorùbá, e de um herói estrangeiro que deu sua vida para salvar um mundo que não era o seu.""",
        "end": True
    },

    "sacred_grove": {
        "title": "O Bosque Sagrado",
        "text": """Você encontra um pequeno bosque onde árvores antigas formam um círculo perfeito. No centro, uma fonte de água cristalina borbulha suavemente. O ar aqui parece vibrar com energia espiritual.

O amuleto em seu pescoço pulsa com mais intensidade, reagindo à energia do local.""",
        "choices": [
            {
                "text": "Beber da água da fonte",
                "test": "spiritual",
                "difficulty": 12,
                "success_node": "sacred_water_blessing",
                "failure_node": "sacred_water_curse"
            },
            {
                "text": "Meditar no centro do bosque",
                "next_node": "grove_meditation"
            },
            {
                "text": "Procurar por sinais dos Òrìṣà",
                "test": "mental",
                "difficulty": 10,
                "success_node": "find_orisha_signs",
                "failure_node": "miss_signs"
            }
        ]
    },

    "grove_meditation": {
        "title": "Meditação Profunda",
        "text": """Você se senta no centro do bosque e fecha os olhos. A energia do lugar parece fluir através de você, trazendo visões:

Você vê os quatro templos principais conectados por linhas de energia. Percebe como o roubo dos artefatos criou brechas nessa rede mística. Mas também vê algo mais - um quinto ponto de poder, oculto e esquecido.""",
        "choices": [
            {
                "text": "Tentar entender mais sobre o quinto ponto de poder",
                "test": "mental",
                "difficulty": 13,
                "success_node": "discover_fifth_temple",
                "failure_node": "meditation_disturbed"
            },
            {
                "text": "Sair da meditação e continuar sua jornada",
                "next_node": "forest_path"
            }
        ]
    },

    "forest_encounter": {
        "title": "O Encontro na Floresta",
        "text": """Enquanto você caminha pela floresta densa, ouve o som de galhos quebrando próximo. Entre as árvores, você vê uma figura encapuzada se movendo rapidamente. Pela forma como se move, parece estar carregando algo pesado.

O amuleto em seu pescoço começa a pulsar levemente, sugerindo que pode haver algo importante por perto.""",
        "choices": [
            {
                "text": "Seguir a figura silenciosamente",
                "test": "physical",
                "difficulty": 12,
                "success_node": "follow_success",
                "failure_node": "follow_failure"
            },
            {
                "text": "Chamar a atenção da figura",
                "next_node": "confront_stranger"
            },
            {
                "text": "Examinar a área em busca de pistas",
                "test": "mental",
                "difficulty": 10,
                "success_node": "find_clues",
                "failure_node": "no_clues"
            }
        ]
    },

    "follow_success": {
        "title": "Perseguição Bem-sucedida",
        "text": """Você consegue seguir a figura sem ser detectado. Ela leva você até uma pequena clareira onde um acampamento foi montado. Você vê mais duas pessoas vestidas de forma similar, e entre seus pertences, algo brilha com uma luz familiar - parece ser um dos artefatos sagrados!""",
        "choices": [
            {
                "text": "Tentar se aproximar mais para ouvir a conversa",
                "test": "physical",
                "difficulty": 13,
                "success_node": "overhear_conversation",
                "failure_node": "spotted_spying"
            },
            {
                "text": "Marcar o local e voltar para buscar ajuda",
                "next_node": "return_for_help"
            },
            {
                "text": "Confrontar o grupo diretamente",
                "battle": "adigun_followers_camp",
                "victory_node": "camp_victory",
                "defeat_node": "camp_capture"
            }
        ]
    },

    "follow_failure": {
        "title": "Perseguição Fracassada",
        "text": """Você tenta seguir a figura silenciosamente, mas pisa em um galho seco que estala ruidosamente. A figura se vira rapidamente, revelando um dos seguidores de Adigun. Ele imediatamente assume uma postura defensiva.""",
        "battle": "lone_follower",
        "victory_node": "follower_defeated",
        "defeat_node": "follower_captures"
    },

    "confront_stranger": {
        "title": "Confronto Direto",
        "text": """'Pare!' você grita. A figura para abruptamente e se vira. É uma mulher jovem, suas vestes marcadas com o símbolo de Adigun. Ela não parece assustada com sua presença.

'Então você é o viajante de quem meu mestre falou,' ela diz, sua voz calma mas ameaçadora. 'Ele sabia que você viria.'""",
        "choices": [
            {
                "text": "Tentar conversar e entender seus motivos",
                "next_node": "dialogue_with_follower"
            },
            {
                "text": "Exigir que ela entregue o artefato",
                "battle": "female_follower",
                "victory_node": "follower_surrender",
                "defeat_node": "follower_escapes"
            },
            {
                "text": "Usar o Amuleto de Ashe para tentar uma conexão espiritual",
                "test": "spiritual",
                "difficulty": 14,
                "success_node": "spiritual_connection",
                "failure_node": "connection_rejected"
            }
        ]
    }
}