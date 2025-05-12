"""
Game Data Module - Contains game constants, enemies, and other static data
"""

# Òrìṣà information
ORISHA = {
    "Yemoja": {
        "domain": "Águas, Rios, Maternidade",
        "symbols": "Conchas marinhas, Prata, Azul",
        "personality": "Nutridora, Protetora, Compassiva",
        "offerings": "Peixe, Melão, Flores brancas"
    },
    "Sango": {
        "domain": "Trovão, Fogo, Justiça",
        "symbols": "Machado duplo, Vermelho e Branco",
        "personality": "Poderoso, Justo, Temperamental",
        "offerings": "Carneiro, Quiabo, Banana"
    },
    "Ogun": {
        "domain": "Ferro, Guerra, Tecnologia",
        "symbols": "Ferramentas de metal, Verde e Preto",
        "personality": "Direto, Forte, Trabalhador",
        "offerings": "Inhame, Feijão, Cachaça"
    },
    "Eshu": {
        "domain": "Comunicação, Encruzilhadas, Destino",
        "symbols": "Cajado, Preto e Vermelho",
        "personality": "Astuto, Imprevisível, Mensageiro",
        "offerings": "Milho, Pimenta, Cachaça"
    },
    "Osun": {
        "domain": "Amor, Beleza, Fertilidade, Rios",
        "symbols": "Leque, Amarelo dourado",
        "personality": "Graciosa, Amorosa, Vaidosa",
        "offerings": "Mel, Frutas, Joias"
    },
    "Obatala": {
        "domain": "Criação, Pureza, Sabedoria",
        "symbols": "Pano branco, Prata",
        "personality": "Calmo, Sábio, Ponderado",
        "offerings": "Inhame, Frutas brancas, Água pura"
    },
    "Oya": {
        "domain": "Ventos, Tempestades, Transformação",
        "symbols": "Espada, Roxo/Marrom",
        "personality": "Guerreira, Impetuosa, Protetora",
        "offerings": "Berinjela, Vinho tinto, Akara"
    },
    "Orunmila": {
        "domain": "Sabedoria, Adivinhação, Destino",
        "symbols": "Tabuleiro de Ifá, Verde e Amarelo",
        "personality": "Sábio, Vidente, Conselheiro",
        "offerings": "Kola nuts, Inhame, Mel"
    }
}

# Enemies
ENEMIES = {
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
    },
    "warrior": {
        "name": "Guerreiro de Elite",
        "description": "Um guerreiro treinado nas antigas artes marciais yorùbá, leal a Adigun.",
        "health": 22,
        "attack": 7,
        "defense": 10,
        "spirit_resistance": 6,
        "rewards": {
            "attribute": {"type": "physical", "amount": 2},
            "item": "Espada Cerimonial"
        }
    },
    "dark_priest": {
        "name": "Sacerdote das Sombras",
        "description": "Um acólito de Adigun, corrompido por magias proibidas.",
        "health": 16,
        "attack": 5,
        "defense": 7,
        "spirit_resistance": 14,
        "rewards": {
            "attribute": {"type": "spiritual", "amount": 2},
            "item": "Grimório Obscuro"
        }
    },
    "adigun": {
        "name": "Adigun",
        "description": "O sacerdote renegado, seus olhos brilham com poder proibido enquanto ele prepara o ritual final.",
        "health": 30,
        "attack": 8,
        "defense": 12,
        "spirit_resistance": 16,
        "rewards": {
            "attribute": {"type": "mental", "amount": 2},
            "attribute": {"type": "spiritual", "amount": 2},
            "attribute": {"type": "physical", "amount": 2}
        }
    }
}

# Character classes and starting attributes
CHARACTER_CLASSES = {
    "Cientista": {
        "description": "Especialista em conhecimento científico e análise racional.",
        "base_attributes": {
            "mental": 10,
            "physical": 6,
            "spiritual": 5
        },
        "gender_mods": {
            "Homem": {"physical": 1},
            "Mulher": {"mental": 1, "physical": -1}
        }
    },
    "Arqueólogo": {
        "description": "Especialista em culturas antigas e artefatos históricos.",
        "base_attributes": {
            "mental": 8,
            "physical": 7,
            "spiritual": 6
        },
        "gender_mods": {
            "Homem": {"physical": 1},
            "Mulher": {"spiritual": 1}
        }
    }
}

# Yoruba phrases with translations
YORUBA_PHRASES = {
    "E ku aro": "Bom dia",
    "E ku osan": "Boa tarde",
    "E ku ale": "Boa noite",
    "E se": "Obrigado",
    "Mo dupe": "Sou grato",
    "Bawo ni": "Como vai?",
    "Jowo": "Por favor",
    "Kilo": "O que é isso?",
    "E wa": "Venha",
    "Ko si wahala": "Sem problemas",
    "Orisha": "Divindade",
    "Omo": "Filho/Criança",
    "Ife": "Amor",
    "Agbo": "Remédio",
    "Ase": "Que assim seja/Amém"
}

# Items that can be found or earned
ITEMS = {
    "Amuleto de Proteção": {
        "description": "Um pequeno amuleto que oferece proteção contra danos físicos.",
        "effect": "Reduz dano recebido em combate.",
        "value": 10
    },
    "Ervas Medicinais": {
        "description": "Um conjunto de ervas com propriedades curativas quando preparadas corretamente.",
        "effect": "Restaura 5 pontos de vida quando usado.",
        "value": 15
    },
    "Símbolo Sagrado": {
        "description": "Um símbolo religioso que fortalece sua conexão com os Òrìṣà.",
        "effect": "Aumenta temporariamente o atributo Espiritual em 2 pontos.",
        "value": 20
    },
    "Espada Cerimonial": {
        "description": "Uma espada ornamentada usada em rituais, mas também eficaz em combate.",
        "effect": "Aumenta o dano físico em batalhas.",
        "value": 25
    },
    "Grimório Obscuro": {
        "description": "Um livro contendo conhecimentos proibidos e feitiços poderosos.",
        "effect": "Permite lançar um ataque espiritual poderoso uma vez por batalha.",
        "value": 30
    },
    "Fragmento do Cetro": {
        "description": "Um pedaço do lendário Cetro de Orunmila, pulsando com energia ancestral.",
        "effect": "Parte do item necessário para completar a missão principal.",
        "value": 100
    }
}

# Locations in the game world
LOCATIONS = {
    "Ife": {
        "description": "A cidade sagrada, centro espiritual de Yorùbáland.",
        "notable_npcs": ["Babatunde", "Rei Odùduà"],
        "quests": ["A Busca pelo Conhecimento", "Audiência Real"]
    },
    "Bosque de Osun": {
        "description": "Uma floresta sagrada onde o rio de Osun corre entre árvores antigas.",
        "notable_npcs": ["Sacerdotisa de Osun", "Guardião da Floresta"],
        "quests": ["Purificação nas Águas", "O Primeiro Fragmento"]
    },
    "Cavernas de Ogun": {
        "description": "Cavernas escuras onde o ferro é extraído e forjado sob a bênção de Ogun.",
        "notable_npcs": ["Mestre Ferreiro", "Espírito da Forja"],
        "quests": ["Prova de Força", "O Segundo Fragmento"]
    },
    "Pico de Sango": {
        "description": "Uma montanha alta onde tempestades se formam e o trovão ecoa constantemente.",
        "notable_npcs": ["Oráculo do Trovão", "Dançarinos da Tempestade"],
        "quests": ["Enfrentando a Tempestade", "O Terceiro Fragmento"]
    },
    "Lago de Olokun": {
        "description": "Um lago profundo e misterioso, portal para o reino submarino de Olokun.",
        "notable_npcs": ["Guardião das Profundezas", "Mensageiro de Yemoja"],
        "quests": ["Mergulho nas Profundezas", "O Quarto Fragmento"]
    },
    "Templo das Sombras": {
        "description": "O templo oculto onde Adigun prepara seu ritual profano.",
        "notable_npcs": ["Adigun", "Sacerdotes das Sombras"],
        "quests": ["Confronto Final", "Restauração do Equilíbrio"]
    }
}

# Common difficulty levels for tests
DIFFICULTY_LEVELS = {
    "muito_facil": 5,
    "facil": 8,
    "medio": 12,
    "dificil": 15,
    "muito_dificil": 18,
    "quase_impossivel": 22
}
