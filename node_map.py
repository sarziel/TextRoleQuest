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
        "title": "Interior do Templo",
        "text": """Você entra no templo com cautela. O interior é fresco e parcialmente iluminado por aberturas estratégicas no teto que criam feixes de luz natural. O ar cheira a incenso e ervas secas.

As paredes internas estão cobertas de relevos e pinturas representando Sango e seus feitos: controlando tempestades, empunhando seu machado duplo, e julgando disputas com sua justiça severa mas justa.

No centro da sala principal, um altar de pedra polida ostenta oferendas: frutas, pequenas esculturas de madeira e tigelas com substâncias desconhecidas. Acima do altar, preso à parede, está um objeto que imediatamente atrai sua atenção: um pequeno machado cerimonial de bronze com inscrições místicas.""",
        "choices": [
            {
                "text": "Examinar o machado cerimonial mais de perto",
                "next_node": "examine_axe"
            },
            {
                "text": "Estudar os relevos e pinturas nas paredes",
                "test": "mental",
                "difficulty": 12,
                "success_node": "temple_paintings_insight",
                "failure_node": "temple_paintings_confusion"
            },
            {
                "text": "Fazer uma pequena oferenda no altar",
                "next_node": "temple_offering"
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
    
    "end_tragic": {
        "title": "O Preço do Fracasso",
        "text": """Apesar de seus esforços, você não consegue impedir Adigun de completar seu ritual. Com os quatro artefatos sagrados, ele abre um portal entre os mundos, permitindo que forças caóticas entrem em Yorùbáland.

O céu escurece com nuvens antinaturais, e criaturas de pesadelo emergem do portal aberto. Os sacerdotes lutam desesperadamente para conter o caos, mas é tarde demais.

Em um último ato de sacrifício, você usa o Amuleto de Ashe para tentar fechar o portal. O poder canalizado é demais para um corpo mortal suportar. Enquanto o portal começa a se fechar, você sente sua própria essência sendo dilacerada.

Seu último pensamento é a esperança de que seu sacrifício não tenha sido em vão. A última coisa que vê é Babajide tentando alcançá-lo, gritando palavras que você não consegue mais ouvir.

Historiadores e arqueólogos do futuro encontrarão registros fragmentados de um cataclismo espiritual que quase destruiu a civilização Yorùbá, e de um herói estrangeiro que deu sua vida para salvar um mundo que não era o seu.""",
        "end": True
    }
}