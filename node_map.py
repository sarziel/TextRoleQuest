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