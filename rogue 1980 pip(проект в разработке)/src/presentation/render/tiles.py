"""
Символы и цветовые пары для отображения сущностей.
"""

ENEMY_CHAR_TO_COLOR_PAIR_ID: dict[str, int] = {
    "z": 1,  # Zombie -> green
    "v": 2,  # Vampire -> red
    "g": 3,  # Ghost -> white
    "O": 4,  # Ogre -> yellow
    "s": 3,  # Snake-mage -> white
}


ENEMY_TILES: dict[str, tuple[str, int]] = {
    "ZOMBIE": ("z", 1),
    "VAMPIRE": ("v", 2),
    "GHOST": ("g", 3),
    "OGRE": ("O", 4),
    "SNAKE_MAGE": ("s", 3),
}

ITEMS_TILES: dict[str, str] = {
    "potion": "!",
    "gold" : "$",
    "food" : "%",
    "scroll" : "?",
}
