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

# This is a simplified implementation for demonstration purposes
# A full implementation would have hundreds of nodes
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
    
    "spotted_hiding": {
        "title": "Descoberto!",
        "text": """Enquanto tenta observar o ritual, você acidentalmente pisa em um galho seco. O estalo ressoa na quietude da floresta ao redor da clareira.

Imediatamente, várias cabeças se viram em sua direção. O ritual para, e dois homens fortes empunhando lanças começam a caminhar em sua direção.

— *Tani ni eleyi?* — um deles grita em uma língua que você não entende, mas o tom ameaçador é claro.""",
        "choices": [
            {
                "text": "Levantar as mãos em sinal de paz e sair do esconderijo",
                "next_node": "peaceful_approach"
            },
            {
                "text": "Tentar fugir para a floresta",
                "test": "physical",
                "difficulty": 13,
                "success_node": "escape_to_forest",
                "failure_node": "failed_escape"
            },
            {
                "text": "Mostrar o amuleto, esperando que ele ofereça alguma proteção",
                "next_node": "show_amulet_guards"
            }
        ]
    },
    
    "approach_village": {
        "title": "Encontro na Aldeia",
        "text": """Respirando fundo, você sai de seu esconderijo e caminha abertamente em direção à aldeia.

O efeito é imediato. Os tambores param, a dança é interrompida, e todos os olhares se voltam para você. Murmúrios se espalham entre as pessoas enquanto avaliam sua aparência estranha.

Três homens com lanças avançam, formando uma barreira entre você e o resto da aldeia. O mais velho deles fala:

— *Tani ni eleyi? Kíni iwọ fẹ́?* (Quem é você? O que deseja?)

Você não entende as palavras, mas o tom é de suspeita cautelosa, não de hostilidade aberta.""",
        "choices": [
            {
                "text": "Gesticular indicando paz e amizade",
                "next_node": "peaceful_gestures"
            },
            {
                "text": "Mostrar o amuleto que está no seu pescoço",
                "next_node": "show_amulet_village"
            },
            {
                "text": "Tentar comunicar com palavras simples e gestos que está perdido",
                "test": "mental",
                "difficulty": 11,
                "success_node": "basic_communication",
                "failure_node": "misunderstanding"
            }
        ]
    },
    
    "forest_path": {
        "title": "Caminho na Floresta",
        "text": """Decidindo evitar o contato imediato com os habitantes da aldeia, você contorna a clareira e segue por um caminho estreito na floresta.

A vegetação se torna mais densa, e os sons da aldeia lentamente diminuem atrás de você. O ar é pesado com umidade, e insetos zumbem ao seu redor enquanto avança.

Após caminhar por cerca de meia hora, você encontra uma bifurcação: o caminho à esquerda desce em direção ao que parece ser um rio, enquanto o da direita sobe por uma colina onde você consegue ver o que parece ser uma estrutura de pedra.""",
        "choices": [
            {
                "text": "Seguir o caminho à esquerda, em direção ao rio",
                "next_node": "river_encounter"
            },
            {
                "text": "Tomar o caminho à direita, rumo à estrutura de pedra",
                "next_node": "stone_structure"
            },
            {
                "text": "Voltar para a aldeia, reconsiderando sua decisão",
                "next_node": "approach_village"
            }
        ]
    },
    
    "river_encounter": {
        "title": "Encontro no Rio",
        "text": """O caminho desce suavemente até revelar um rio largo e tranquilo. A água clara corre sobre pedras lisas, e a vegetação é exuberante nas margens.

Chegando mais perto, você percebe que não está sozinho. Uma mulher jovem está ajoelhada à beira d'água, enchendo um pote de barro. Ela veste um pano azul enrolado como vestido e tem contas coloridas no pescoço e nos pulsos.

Ela ainda não notou sua presença.""",
        "choices": [
            {
                "text": "Aproximar-se cuidadosamente e cumprimentá-la",
                "next_node": "meet_river_woman"
            },
            {
                "text": "Observá-la discretamente antes de decidir o que fazer",
                "test": "mental",
                "difficulty": 10,
                "success_node": "observe_river_ritual",
                "failure_node": "startle_river_woman"
            },
            {
                "text": "Evitá-la e continuar seguindo o rio",
                "next_node": "downstream_path"
            }
        ]
    },
    
    "stone_structure": {
        "title": "O Templo nas Colinas",
        "text": """Subindo a colina, você se aproxima do que agora pode identificar claramente como um templo de pedra. A construção não é grande, mas é impressionante: blocos de pedra cinza perfeitamente encaixados formam um edifício retangular com uma entrada ornamentada.

Pilares esculpidos ladeiam a entrada, decorados com padrões geométricos complexos e figuras que lembram os símbolos do seu amuleto. No topo do templo, uma estátua de pedra representa uma figura feminina com braços erguidos para o céu.

O lugar parece deserto, mas você sente uma estranha energia emanando de dentro.""",
        "battle": "snake",
        "victory_node": "temple_entrance_after_battle",
        "defeat_node": "snake_defeat"
    },
    
    "temple_entrance_after_battle": {
        "title": "Após a Batalha",
        "text": """Com a serpente gigante derrotada, você respira aliviado. Seu coração ainda bate acelerado pela intensa confrontação.

Olhando mais atentamente para o animal caído, você nota um padrão de escamas incomum, que forma símbolos semelhantes aos do seu amuleto. Talvez não fosse uma serpente comum, mas um guardião designado para proteger o templo.

O caminho para a entrada agora está livre. As portas de pedra do templo estão entreabertas, com uma escuridão misteriosa além delas.""",
        "choices": [
            {
                "text": "Entrar no templo e explorar seu interior",
                "next_node": "temple_interior"
            },
            {
                "text": "Examinar mais detalhadamente a serpente derrotada",
                "test": "mental",
                "difficulty": 12,
                "success_node": "snake_revelation",
                "failure_node": "snake_nothing"
            },
            {
                "text": "Voltar à bifurcação e seguir para o rio",
                "next_node": "river_encounter"
            }
        ]
    },
    
    "snake_defeat": {
        "title": "Derrota Pela Serpente",
        "text": """A serpente gigante é rápida demais. Antes que você possa reagir adequadamente, ela te atinge com força, e você cai no chão, ferido e desorientado.

A dor é intensa, e sua visão começa a escurecer nas bordas. Você espera pelo golpe final, mas ele não vem.

Em vez disso, a serpente se afasta, deslizando de volta para as sombras do templo. No limiar da consciência, você ouve passos se aproximando...""",
        "next_node": "rescued_by_priestess"
    },
    
    "rescued_by_priestess": {
        "title": "Resgate Inesperado",
        "text": """Você acorda com o toque suave de mãos em seu rosto. Abrindo os olhos, vê uma mulher idosa debruçada sobre você. Ela usa vestes azuis decoradas com contas e conchas, e seus olhos transmitem sabedoria e poder.

— *O wo le ji*. Você acordou. — ela diz, para sua surpresa, em uma mistura de yorùbá e sua língua. — A serpente de Oxumaré testou você e o achou digno de viver, mas não de entrar. Ainda não.

Ela ajuda você a se sentar. Você percebe que está em uma pequena cabana, iluminada por lamparina a óleo. Seus ferimentos foram tratados com ervas e unguentos.""",
        "choices": [
            {
                "text": "Perguntar quem ela é",
                "next_node": "priestess_identity"
            },
            {
                "text": "Questionar sobre a serpente e o templo",
                "next_node": "priestess_explanation"
            },
            {
                "text": "Mostrar o amuleto e perguntar sobre ele",
                "next_node": "priestess_amulet"
            }
        ]
    },
    
    "temple_interior": {
        "title": "Dentro do Templo",
        "text": """Você empurra as pesadas portas de pedra e entra no templo. No início, a escuridão é quase completa, mas seus olhos lentamente se ajustam à pouca luz que entra por pequenas aberturas no teto.

O interior é um único salão amplo, com paredes cobertas de entalhes e pinturas. Pilares esculpidos sustentam o teto alto, cada um representando uma figura diferente - os Òrìṣà, você percebe.

No centro do salão há um altar de pedra circular, e sobre ele repousa uma estátua pequena feita de um metal dourado. A estátua representa uma mulher com braços abertos, usando uma coroa elaborada.""",
        "choices": [
            {
                "text": "Aproximar-se do altar para examinar a estátua",
                "next_node": "examine_statue"
            },
            {
                "text": "Estudar as pinturas e entalhes nas paredes",
                "test": "mental",
                "difficulty": 13,
                "success_node": "decipher_murals",
                "failure_node": "partial_understanding"
            },
            {
                "text": "Procurar por outras passagens ou salas ocultas",
                "test": "mental",
                "difficulty": 14,
                "success_node": "find_hidden_chamber",
                "failure_node": "no_hidden_areas"
            }
        ]
    },
    
    "examine_statue": {
        "title": "A Estátua de Yemoja",
        "text": """Você se aproxima do altar e examina a estátua dourada. É uma peça belíssima, criada com incrível atenção aos detalhes. A figura feminina tem feições serenas e usa vestes que parecem fluir como água.

Seu amuleto começa a brilhar mais intensamente à medida que você se aproxima da estátua. Quando está a apenas alguns centímetros, ambos os objetos emitem um pulso de luz azulada.

Uma voz feminina, suave como água corrente, preenche sua mente:

— *Filho(a) de terras distantes, você encontrou meu santuário. Eu sou Yemoja, mãe das águas, protetora da vida. Seu coração é puro, mas sua jornada apenas começou...*""",
        "orisha": True,
        "choices": [
            {
                "text": "Perguntar a Yemoja sobre como voltar para seu tempo",
                "next_node": "yemoja_return"
            },
            {
                "text": "Perguntar sobre o propósito da sua vinda a este tempo",
                "next_node": "yemoja_purpose"
            },
            {
                "text": "Pedir a bênção e proteção de Yemoja",
                "test": "spiritual",
                "difficulty": 12,
                "success_node": "yemoja_blessing",
                "failure_node": "yemoja_trial"
            }
        ]
    },
    
    "yemoja_return": {
        "title": "O Caminho de Volta",
        "orisha": True,
        "text": """— *Voltar?* — a voz de Yemoja ressoa com um tom de leve diversão. — *Você mal chegou, e já deseja partir? Os caminhos do tempo não são estradas simples que se percorre na direção desejada.*

A estátua brilha mais intensamente enquanto a deusa continua:

— *O portal que o trouxe foi aberto por uma confluência de forças, pela vontade dos Òrìṣà e pelo chamado da terra. Para retornar, você precisa completar o propósito pelo qual foi trazido.*

A voz se torna mais séria:

— *Há uma perturbação no tecido do mundo. Uma ameaça que ecoa através do tempo, afetando tanto este era quanto a sua. Você foi escolhido para intervir, para restaurar o equilíbrio que está se desfazendo.*""",
        "choices": [
            {
                "text": "Perguntar sobre a natureza desta ameaça",
                "next_node": "yemoja_threat"
            },
            {
                "text": "Aceitar a missão e pedir orientação",
                "next_node": "yemoja_guidance"
            },
            {
                "text": "Questionar por que você foi o escolhido",
                "next_node": "yemoja_chosen"
            }
        ]
    },
    
    "yemoja_purpose": {
        "title": "Seu Propósito",
        "orisha": True,
        "text": """— *Seu propósito...* — a voz de Yemoja flui como água profunda. — *Você foi trazido porque as cordas do tempo estão tensas, ameaçando romper o tecido que separa as eras.*

A luz emanando da estátua forma padrões ondulantes nas paredes do templo enquanto ela continua:

— *Um usurpador busca poder proibido. Ele pretende subjugar os Òrìṣà, rompendo o equilíbrio entre os mundos. Seu nome é Adigun, um sacerdote que abandonou o caminho da luz, seduzido por forças das sombras.*

A voz de Yemoja se torna mais firme:

— *Você carrega o Amuleto de Equilíbrio, um artefato criado pelos primeiros sacerdotes para momentos como este. Com ele, e com a ajuda dos Òrìṣà leais, você deve impedir Adigun antes que ele complete seu ritual na próxima lua cheia.*""",
        "choices": [
            {
                "text": "Perguntar onde encontrar Adigun",
                "next_node": "yemoja_location"
            },
            {
                "text": "Questionar como você, um estrangeiro, pode enfrentar tal ameaça",
                "next_node": "yemoja_power"
            },
            {
                "text": "Aceitar a missão e pedir a bênção de Yemoja",
                "test": "spiritual",
                "difficulty": 12,
                "success_node": "yemoja_blessing",
                "failure_node": "yemoja_trial"
            }
        ]
    },
    
    "yemoja_blessing": {
        "title": "A Bênção das Águas",
        "orisha": True,
        "text": """À medida que você pede a bênção de Yemoja, a estátua emite um brilho azul intenso que envolve seu corpo. Você sente uma sensação refrescante, como mergulhar em águas cristalinas.

— *Eu concedo minha bênção a você, viajante do tempo* — declara Yemoja, sua voz como ondas gentis. — *Que minhas águas fluam em seu sangue, trazendo vida, cura e intuição.*

Você sente uma mudança sutil em seu ser. Uma conexão com as águas do mundo, com o fluxo da vida. Sua percepção parece ampliada, como se pudesse sentir vibrações e energias antes invisíveis.

— *Quando estiver próximo de águas - rios, lagos, chuva ou mar - meu poder estará mais forte em você. Use-o com sabedoria e respeito.*

O brilho se intensifica uma última vez antes de diminuir gradualmente.""",
        "next_node": "yemoja_quest"
    },
    
    "yemoja_trial": {
        "title": "O Teste de Yemoja",
        "orisha": True,
        "text": """Você pede a bênção de Yemoja, mas a estátua escurece levemente, e a voz da deusa fica mais grave:

— *Sua intenção é pura, mas seu espírito ainda não está pronto para receber minha bênção completa. Você deve provar seu valor e compromisso com o equilíbrio.*

Uma névoa azulada sai da estátua e forma um círculo ao seu redor.

— *Enfrente meu teste. Mostre que tem a coragem e a sabedoria necessárias para a jornada à sua frente.*

A névoa se condensa, tomando a forma de uma figura feminina translúcida - um espírito guardião de Yemoja.""",
        "battle": "spirit",
        "victory_node": "yemoja_trial_success",
        "defeat_node": "yemoja_trial_failure"
    },
    
    "yemoja_trial_success": {
        "title": "Provação Superada",
        "orisha": True,
        "text": """O espírito guardião se dissipa em névoa azul após sua vitória, retornando à estátua de Yemoja. O templo vibra com uma energia renovada, e a voz da deusa ressurge, agora carregada de aprovação:

— *Você enfrentou minha guardiã com coragem e respeito. Não buscou apenas destruí-la, mas compreendê-la, e isso demonstra sabedoria.*

A estátua emite um brilho suave que envolve seu corpo. Você sente uma sensação refrescante, como mergulhar em águas cristalinas.

— *Receba agora minha bênção parcial. À medida que provar seu valor em sua jornada, mais de meu poder será revelado a você.*

Você sente uma mudança sutil em seu ser. Uma conexão com as águas do mundo, com o fluxo da vida.""",
        "next_node": "yemoja_quest"
    },
    
    "yemoja_trial_failure": {
        "title": "Teste Incompleto",
        "orisha": True,
        "text": """Você cai de joelhos, exausto pela batalha contra o espírito guardião. Embora não tenha sido derrotado completamente, também não conseguiu superar o teste.

A figura espiritual recua, retornando à estátua de Yemoja. A voz da deusa ressurge, nem decepcionada nem satisfeita:

— *Você demonstrou coragem, mas ainda lhe falta algo. O equilíbrio entre força e sabedoria, entre ação e contemplação, ainda precisa ser encontrado em seu coração.*

A estátua brilha suavemente, e você sente uma leve energia curativa que alivia suas feridas, mas não as cura completamente.

— *Não posso conceder minha bênção completa agora, mas não o deixarei sem ajuda. Busque as águas sagradas na aldeia de Omi-Odo, onde meus sacerdotes poderão guiá-lo no caminho do equilíbrio.*""",
        "next_node": "yemoja_alternative_path"
    },
    
    "yemoja_quest": {
        "title": "A Missão de Yemoja",
        "orisha": True,
        "text": """Yemoja continua, sua voz fluindo como um rio tranquilo:

— *Sua jornada deve começar na aldeia de Ife, o centro sagrado de nossa terra. Lá, você deve procurar o sacerdote Babatunde, que guarda conhecimentos antigos sobre o Amuleto que você porta.*

A água que parece emanar da estátua forma imagens no ar - um mapa translúcido mostrando o caminho até Ife.

— *De Ife, você deverá buscar os quatro fragmentos do Cetro de Orunmila, dispersos para impedir que caíssem em mãos erradas. Apenas com o Cetro completo você poderá confrontar Adigun e impedir o ritual profano.*

As imagens mudam, mostrando quatro locais diferentes:

— *Os fragmentos estão guardados no Bosque de Osun, nas Cavernas de Ogun, no Pico de Sango e nas profundezas do Lago de Olokun. Cada guardião exigirá prova de seu valor.*

A luz começa a diminuir lentamente.

— *Vá agora. Minha bênção o acompanha, mas seja cauteloso. Adigun tem muitos olhos e ouvidos. Confie apenas naqueles cujos corações você puder sentir verdadeiramente.*""",
        "choices": [
            {
                "text": "Agradecer a Yemoja e partir para Ife",
                "next_node": "leave_temple"
            },
            {
                "text": "Perguntar sobre perigos no caminho para Ife",
                "next_node": "yemoja_warnings"
            },
            {
                "text": "Pedir mais informações sobre o Cetro de Orunmila",
                "next_node": "yemoja_scepter"
            }
        ]
    },
    
    "find_portal_success": {
        "title": "Vestígios do Portal",
        "text": """Com olhar treinado, você examina cuidadosamente a área. Sua experiência científica permite identificar sutis anomalias: folhas que parecem vibrar em uma frequência diferente, padrões estranhos no musgo das árvores, pequenas partículas luminosas flutuando no ar.

Seguindo esses sinais, você encontra o local exato por onde chegou. Há um círculo perfeito onde a vegetação parece mais vibrante, quase brilhante.

Agachando-se, você nota símbolos sutis gravados em algumas pedras semienterradas. Eles formam um padrão circular - claramente os restos de algum tipo de portal ritual.""",
        "choices": [
            {
                "text": "Tentar ativar o portal tocando nos símbolos",
                "test": "spiritual",
                "difficulty": 15,
                "success_node": "portal_activation",
                "failure_node": "portal_failure"
            },
            {
                "text": "Memorizar a localização e os símbolos para retornar depois",
                "next_node": "follow_drums"
            },
            {
                "text": "Examinar mais detalhadamente os símbolos nas pedras",
                "test": "mental",
                "difficulty": 12,
                "success_node": "portal_knowledge",
                "failure_node": "portal_confusion"
            }
        ]
    },
    
    "find_portal_failure": {
        "title": "Buscando em Vão",
        "text": """Você examina a área cuidadosamente, procurando por qualquer sinal do portal que o trouxe aqui. Infelizmente, a densa vegetação e o terreno acidentado tornam a busca difícil.

Após vinte minutos frustrantes, você não encontra nada que pareça remotamente com um portal, ou qualquer tecnologia ou estrutura que poderia explicar sua viagem no tempo.

Talvez o portal seja invisível, ou talvez tenha se fechado completamente após sua passagem. De qualquer forma, está claro que voltar para seu tempo não será tão simples quanto encontrar o caminho de entrada.""",
        "next_node": "follow_drums"
    },
    
    "portal_activation": {
        "title": "Portal Instável",
        "text": """Guiado por uma intuição que não compreende totalmente, você coloca as mãos sobre os símbolos nas pedras e fecha os olhos, concentrando-se.

Para sua surpresa, os símbolos começam a brilhar com uma luz azulada. O ar no centro do círculo ondula, como o calor sobre asfalto quente, e uma pequena abertura começa a se formar - uma janela translúcida através da qual você consegue ver o local da escavação que deixou para trás.

Seu coração acelera ao ver Ademola, seu colega, examinando ansiosamente o local onde você desapareceu. Você tenta chamá-lo, mas não há som. A abertura é instável, tremulando e diminuindo rapidamente.

Você percebe que poderia tentar atravessar, mas o portal está fraco e instável.""",
        "choices": [
            {
                "text": "Tentar atravessar o portal de volta para seu tempo",
                "test": "physical",
                "difficulty": 16,
                "success_node": "early_return",
                "failure_node": "portal_collapse"
            },
            {
                "text": "Deixar o portal se fechar e seguir com sua jornada neste tempo",
                "next_node": "follow_drums"
            }
        ]
    },
    
    "portal_failure": {
        "title": "Energia Insuficiente",
        "text": """Você toca os símbolos nas pedras e tenta se concentrar, buscando ativar qualquer mecanismo místico que possa existir.

As pedras vibram levemente sob seus dedos, e por um momento você sente uma estranha energia percorrendo seu corpo. Os símbolos emitem um brilho tênue, mas após alguns segundos, a luz se apaga.

Você tenta novamente, repetindo o processo de diferentes maneiras, mas obtém apenas breves pulsos de energia que logo se dissipam. Parece que o portal requer algo mais - talvez conhecimento específico, uma fonte de poder, ou simplesmente não está destinado a ser reaberto agora.""",
        "next_node": "follow_drums"
    },
    
    "portal_collapse": {
        "title": "Entre Mundos",
        "text": """Você se lança em direção ao portal instável, tentando atravessá-lo de volta para seu tempo. No momento em que seu corpo toca a abertura ondulante, você sente uma resistência incomum, como nadar contra uma corrente poderosa.

Metade do seu corpo consegue passar, e por um instante surreal, você existe em dois tempos simultaneamente. Seus olhos veem tanto a floresta antiga quanto o sítio de escavação moderno. Você consegue ver Ademola gritando algo, seus olhos arregalados de surpresa.

Então, sem aviso, o portal colapsa. Uma onda de energia o arremessa para trás, e você cai violentamente no chão da floresta. Seu corpo inteiro formiga com uma sensação estranha, e sua cabeça gira.

Quando a tontura passa, você percebe que está completamente de volta ao passado, mas algo mudou. Sua conexão com este lugar parece mais forte, como se parte de você agora pertencesse aqui.""",
        "next_node": "follow_drums_after_portal"
    },
    
    "early_return": {
        "title": "Retorno Prematuro",
        "text": """Com um esforço tremendo, você consegue atravessar o portal instável, sentindo seu corpo ser comprimido e esticado enquanto passa entre os tempos.

Em um instante, você está de volta ao local da escavação. Ademola grita de surpresa quando você aparece do nada, exatamente onde havia desaparecido minutos antes.

— Meu Deus! O que aconteceu? Você simplesmente... sumiu! — ele exclama, ajudando-o a se levantar.

Você olha para suas mãos e percebe que ainda segura o amuleto. De alguma forma, ele veio com você. Mas enquanto tenta explicar o que aconteceu, o amuleto começa a pulsar com luz intensa.

Antes que possa reagir, uma voz ressoa em sua mente: "Sua jornada não está completa. O equilíbrio ainda está em risco..."

Uma luz brilhante o envolve novamente.""",
        "next_node": "return_to_past",
        "end": True
    },
    
    "return_to_past": {
        "title": "De Volta à Missão",
        "text": """A luz do amuleto o envolve completamente, e você sente novamente a sensação de ser transportado através do tempo. Dessa vez, a transição é mais suave, quase como se o caminho já estivesse preparado.

Você reaparece na floresta de Yorùbáland, exatamente onde estava antes. O portal nas pedras está agora completamente inativo, sem o menor sinal de energia.

Uma compreensão intuitiva surge em sua mente: você não poderá retornar ao seu tempo até completar a missão para a qual foi trazido. O breve vislumbre de seu mundo moderno apenas confirmou o que os Òrìṣà já sabiam - seu destino está ligado a este lugar, a este tempo.

Com nova determinação, você decide seguir o som dos tambores. É hora de descobrir por que você realmente foi trazido aqui.""",
        "next_node": "follow_drums"
    },
    
    # More story nodes would continue here...
    
    # Example ending nodes
    "ending_tragic": {
        "title": "Um Destino Trágico",
        "text": """As escolhas que você fez e os desafios que enfrentou culminaram em um momento fatídico. Ferido e enfraquecido, você não consegue impedir Adigun de completar seu ritual profano.

O céu escurece enquanto energias malignas são liberadas. Você sente o tecido da realidade se rasgando ao seu redor, e sabe que falhou em sua missão.

Em seus últimos momentos, você vê imagens do futuro - seu tempo, seu mundo - sendo transformado por ondas de caos que emanam deste ponto no passado. A história que você conhecia será reescrita na escuridão.

Os Òrìṣà, enfraquecidos pelo ritual corrompido de Adigun, não podem mais proteger a terra nem os caminhos do tempo. Sua consciência se desvanece enquanto o mundo ao seu redor desmorona...

[FIM TRÁGICO: Você falhou em proteger o equilíbrio entre os mundos]""",
        "end": True
    },
    
    "ending_emperor": {
        "title": "O Novo Imperador",
        "text": """Sua jornada por Yorùbáland mudou você profundamente. Suas habilidades, conhecimento e conexão com os Òrìṣà o transformaram em uma figura lendária entre o povo.

Após derrotar Adigun e restaurar o equilíbrio, você é levado ao grande palácio de Ife. Lá, diante de uma multidão de sacerdotes, guerreiros e cidadãos comuns, o velho imperador anuncia sua decisão:

— *Este estrangeiro salvou nossa terra e foi abençoado pelos próprios Òrìṣà. Quando eu partir para a terra dos ancestrais, será ele quem usará a coroa de Ife.*

Nos anos que se seguem, você aprende os costumes, a língua e as tradições completas do povo Yorùbá. Quando finalmente ascende ao trono, você une os reinos fragmentados sob uma liderança sábia, inspirada tanto pelo conhecimento do futuro quanto pelo respeito às tradições antigas.

O portal para seu tempo de origem aparece ocasionalmente em seus sonhos, mas você fez sua escolha. Este é seu lar agora, e seu legado perdurará por milênios.

[FIM IMPERIAL: Você se tornou governante de um poderoso império]""",
        "end": True
    },
    
    "ending_orisha": {
        "title": "Ascensão",
        "text": """Enquanto completa sua missão final e derrota as forças que ameaçavam o equilíbrio, algo extraordinário acontece. O amuleto que carregou por toda a jornada se funde com seu peito, e uma luz radiante emana de seu corpo.

Você sente sua consciência se expandindo, transcendendo os limites da carne e do tempo. Os Òrìṣà aparecem ao seu redor em um círculo de luz, cada um oferecendo um gesto de bênção.

Yemoja se aproxima com um sorriso sereno:

— *Sua jornada como mortal termina aqui. Seu sacrifício, sabedoria e compaixão provaram que você é digno de ascender. De agora em diante, você existirá além do tempo, como guardião do equilíbrio entre os mundos.*

Sua forma física se dissolve em luz pura, e você sente uma conexão com toda a existência. Parte de você permanecerá em Yorùbáland, recebendo orações e oferendas. Outra parte retornará ao futuro, inspirando outros silenciosamente.

Como um Òrìṣà, você transcendeu a história para se tornar parte da eternidade.

[FIM DIVINO: Você ascendeu como um novo Òrìṣà]""",
        "end": True
    }
}
